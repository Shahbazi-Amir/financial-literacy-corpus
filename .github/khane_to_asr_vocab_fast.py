from pathlib import Path
import re, unicodedata
from collections import Counter,defaultdict
from wordfreq import zipf_frequency
from rapidfuzz import process
from rapidfuzz.distance import Levenshtein

ROOT=Path('.'); OUT=ROOT/'outputs/khane_to/review/md'; REF=ROOT/'متن ها/khane-to'; REPORT=ROOT/'reports/khane_to_asr_vocab_fast.md'
rx=re.compile(r"[\u0600-\u06FF\u200c]+")
def norm(s): return unicodedata.normalize('NFKC',s).replace('ي','ی').replace('ك','ک').replace('\u200c','').lower()
def words(t): return rx.findall(t)
def zf(w): return zipf_frequency(norm(w),'fa')

ref_words=[]
for p in sorted(REF.glob('episode-*.md')): ref_words += words(p.read_text(encoding='utf-8'))
ref_count=Counter(norm(w) for w in ref_words); canon={}
for w in ref_words: canon.setdefault(norm(w),w)
buckets=defaultdict(list)
for w in ref_count: buckets[len(w)].append(w)

VALID_SUFFIX=('تون','مون','شون','هام','هات','هاش','هامون','هاتون','هاشون')
VALID_EXACT={norm(x) for x in ['می‌خوام','می‌خوایم','می‌تونم','می‌تونیم','می‌گم','می‌گن','می‌شه','میاد','همون','اینه','یه','اگه','رو','واسه','چجوری','دیگه','بکنم','بکنیم','باشه','می‌ذاریم','می‌ذاره','خدمتتون','درآمدشون','مالیمون','زندگی‌مون','دارایی‌هام']}
def exempt(w):
    n=norm(w); return n in VALID_EXACT or any(n.endswith(s) for s in VALID_SUFFIX)

def nearest(n):
    L=len(n); maxd=1 if L<=4 else 2 if L<=8 else 3
    choices=[]
    for ln in range(max(1,L-maxd),L+maxd+1): choices.extend(buckets.get(ln,()))
    if not choices: return None
    hit=process.extractOne(n,choices,scorer=Levenshtein.normalized_similarity,score_cutoff=0.45)
    if not hit: return None
    r=hit[0]; d=Levenshtein.distance(n,r)
    if d>maxd: return None
    # among same minimal-distance candidates prefer higher language frequency
    near=[x for x in choices if abs(len(x)-L)<=maxd and Levenshtein.distance(n,x)==d]
    if near: r=max(near,key=lambda x:(zf(x),ref_count[x]))
    return d,r

lines=['# کاندیدهای واژگانی سریع — خانه تو','', '> فقط کاندیدهای ASR؛ هیچ Outputی هنوز تغییر نکرده.','']
for ep in range(1,14):
    text=(OUT/f'{ep}.md').read_text(encoding='utf-8'); ws=words(text); cnt=Counter(norm(w) for w in ws); surf={}
    for w in ws: surf.setdefault(norm(w),w)
    cs=[]
    for n,c in cnt.items():
        w=surf[n]
        if n in ref_count or exempt(w) or len(n)<3: continue
        fa=zf(w)
        if fa>=4.25: continue
        q=nearest(n)
        if not q: continue
        d,r=q; b=canon[r]; fb=zf(b)
        if fb<3.2 or fb-fa<0.7: continue
        if n.startswith('می') and r.startswith('می') and fa>2.7: continue
        cs.append((w,b,d,fa,fb,c,ref_count[r]))
    cs.sort(key=lambda x:(-(x[4]-x[3]),x[2],x[0]))
    lines += [f'## قسمت {ep}',f'- کاندید: **{len(cs)}**','']
    for a,b,d,fa,fb,c,rc in cs:
        lines.append(f'- `{a}` → `{b}` | edit={d} | freq {fa:.2f}→{fb:.2f} | output×{c} ref×{rc}')
    lines.append('')
REPORT.write_text('\n'.join(lines),encoding='utf-8'); print(REPORT)

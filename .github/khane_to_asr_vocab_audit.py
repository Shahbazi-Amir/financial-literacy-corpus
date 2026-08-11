from pathlib import Path
import re, unicodedata
from collections import Counter
from wordfreq import zipf_frequency

ROOT=Path('.')
OUT=ROOT/'outputs/khane_to/review/md'
REF=ROOT/'متن ها/khane-to'
REPORT=ROOT/'reports/khane_to_asr_vocab_candidates.md'
rx=re.compile(r"[\u0600-\u06FF\u200c]+")
def norm(s): return unicodedata.normalize('NFKC',s).replace('ي','ی').replace('ك','ک').replace('\u200c','').lower()
def words(t): return rx.findall(t)
def lev(a,b):
    a,b=norm(a),norm(b); n=len(b); dp=list(range(n+1))
    for i,ca in enumerate(a,1):
        nd=[i]+[0]*n
        for j,cb in enumerate(b,1): nd[j]=min(dp[j]+1,nd[j-1]+1,dp[j-1]+(ca!=cb))
        dp=nd
    return dp[n]
def zf(w): return zipf_frequency(norm(w),'fa')

# global curated vocabulary
ref_words=[]
for p in sorted(REF.glob('episode-*.md')): ref_words += words(p.read_text(encoding='utf-8'))
ref_count=Counter(norm(w) for w in ref_words)
# canonical surface form: most frequent occurrence first
canon={}
for w in ref_words: canon.setdefault(norm(w),w)
rv=list(ref_count)

# Style/colloquial endings that are valid and must not be normalized
VALID_SUFFIX=('تون','مون','شون','هام','هات','هاش','هامون','هاتون','هاشون')
VALID_EXACT={norm(x) for x in ['می‌خوام','می‌خوایم','می‌تونم','می‌تونیم','می‌گم','می‌گن','می‌شه','میاد','همون','اینه','یه','اگه','رو','واسه','چجوری','دیگه','بکنم','بکنیم','باشه','می‌ذاریم','می‌ذاره']}

def exempt(w):
    n=norm(w)
    return n in VALID_EXACT or any(n.endswith(s) for s in VALID_SUFFIX)

def nearest(w):
    n=norm(w); L=len(n)
    maxd=1 if L<=4 else 2 if L<=8 else 3
    best=[]; bd=maxd+1
    # length bucket
    for r in rv:
        if abs(len(r)-L)>maxd: continue
        d=lev(n,r)
        if d<bd: bd=d; best=[r]
        elif d==bd: best.append(r)
    if bd>maxd: return None
    # prefer high language frequency + reference count
    best.sort(key=lambda r:(zf(r),ref_count[r]),reverse=True)
    return bd,best[0]

lines=['# کاندیدهای واژگانی اصلاح ASR — خانه تو','',
'> واژه‌های نادر/نامعتبر Output در برابر واژگان کل ۱۳ متن تمیز سنجیده شده‌اند. این گزارش هم فقط کاندید است.','']
for ep in range(1,14):
    text=(OUT/f'{ep}.md').read_text(encoding='utf-8')
    ws=words(text); cnt=Counter(norm(w) for w in ws); surf={}
    for w in ws: surf.setdefault(norm(w),w)
    cs=[]
    for n,c in cnt.items():
        w=surf[n]
        if n in ref_count or exempt(w) or len(n)<3: continue
        fa=zf(w)
        # only suspicious/rare-ish output words; keep ordinary spoken words
        if fa>=4.35: continue
        q=nearest(w)
        if not q: continue
        d,r=q; b=canon[r]; fb=zf(b)
        if fb < 3.2 or fb-fa < 0.65: continue
        # avoid likely grammatical/style suffix rewrites
        if norm(w).startswith('می') and norm(b).startswith('می') and fa>2.8: continue
        cs.append((w,b,d,fa,fb,c,ref_count[r]))
    cs.sort(key=lambda x:(-(x[4]-x[3]),x[2],x[0]))
    lines += [f'## قسمت {ep}',f'- کاندید واژگانی: **{len(cs)}**','']
    for a,b,d,fa,fb,c,rc in cs:
        lines.append(f'- `{a}` → `{b}` | edit={d} | freq {fa:.2f}→{fb:.2f} | output×{c} ref×{rc}')
    # adjacent two-word fusion candidates: only if second token very rare and combined close to one curated word
    fusion=[]
    for i in range(len(ws)-1):
        a,b=ws[i],ws[i+1]; na,nb=norm(a),norm(b)
        if zf(b)>3.0 or len(nb)<2: continue
        joined=na+nb; L=len(joined); maxd=2 if L>=5 else 1
        best=None
        for r in rv:
            if abs(len(r)-L)>maxd: continue
            d=lev(joined,r)
            if d<=maxd and (best is None or (d,-zf(r))<(best[0],-zf(best[1]))): best=(d,r)
        if best and zf(best[1])>=3.3:
            fusion.append((a+' '+b,canon[best[1]],best[0]))
    seen=set()
    for a,b,d in fusion:
        k=(norm(a),norm(b))
        if k in seen: continue
        seen.add(k); lines.append(f'- [دوواژه‌ای] `{a}` → `{b}` | edit={d}')
    lines.append('')
REPORT.write_text('\n'.join(lines),encoding='utf-8')
print(REPORT)

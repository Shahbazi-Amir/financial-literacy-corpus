from pathlib import Path
import re, unicodedata
from collections import Counter,defaultdict
from wordfreq import zipf_frequency
from rapidfuzz import process
from rapidfuzz.distance import Levenshtein

ROOT=Path('.'); OUT=ROOT/'outputs/khane_to/review/md'; REF=ROOT/'متن ها/khane-to'; REPORT=ROOT/'reports/khane_to_asr_severe.md'
rx=re.compile(r"[\u0600-\u06FF\u200c]+")
def norm(s): return unicodedata.normalize('NFKC',s).replace('ي','ی').replace('ك','ک').replace('\u200c','').lower().strip('،؛؟!:.')
def words(t): return rx.findall(t)
def zf(w): return zipf_frequency(norm(w),'fa')
ref=[]
for p in REF.glob('episode-*.md'): ref += words(p.read_text(encoding='utf-8'))
rc=Counter(norm(w) for w in ref); canon={}
for w in ref: canon.setdefault(norm(w),w)
b=defaultdict(list)
for w in rc: b[len(w)].append(w)
SUF=('ها','های','هایی','هام','هات','هاش','مون','تون','شون','ام','ات','اش','مان','تان','شان','م','ت','ش','یم','ید','ند','ن','و','ه','ست')
VALID={norm(x) for x in ['ناسلامتی','خانواده‌ست','صبح‌ها','دیگه‌ای','تعریفش','آینده‌تو','ارتباط‌ها','تمرینه','اعتباره','همگانیه','حرفه‌ایه','بازپرداختش','متعالیه','درش','همینی','اونچه','زندگیه','دومش','دردم','کمکت','طبیعیه','راحت‌تر','خدایی','بتونن','بپرسی','نزدیک‌تر','مالیه','قدرتی','سؤالات','آن‌چنان','منطبق','خیلی‌ها','به‌فرض','مدیریتش','پاسخش','درآمدت','عرضم','کیفیتش','دینیه','اعتبارت','راجع‌به','هرجوری','بی‌دغدغه','بدهیه','دولت‌هایی','پیشنهادم','مطرحه','جمعش','یک‌سری']}
def derived(a,r):
    a,r=norm(a),norm(r)
    if a==r or a.startswith(r) or r.startswith(a): return True
    for s in SUF:
        if a.endswith(s) and a[:-len(s)]==r: return True
        if r.endswith(s) and r[:-len(s)]==a: return True
    return False

def nearest(n):
    L=len(n); md=1 if L<=4 else 2
    choices=[]
    for ln in range(max(1,L-md),L+md+1): choices.extend(b.get(ln,()))
    hit=process.extractOne(n,choices,scorer=Levenshtein.normalized_similarity,score_cutoff=.55)
    if not hit:return None
    d=Levenshtein.distance(n,hit[0])
    if d>md:return None
    near=[x for x in choices if Levenshtein.distance(n,x)==d]
    r=max(near,key=lambda x:(zf(x),rc[x])) if near else hit[0]
    return d,r

lines=['# کاندیدهای شدید ASR — خانه تو','', '> هدف: فقط کلمات واقعاً مشکوک، با بافت خط.','']
for ep in range(1,14):
    text=(OUT/f'{ep}.md').read_text(encoding='utf-8'); ls=text.splitlines(); seen=set(); cs=[]
    for li,line in enumerate(ls,1):
        for w in words(line):
            n=norm(w)
            if len(n)<3 or n in rc or n in VALID or zf(w)>2.7: continue
            q=nearest(n)
            if not q: continue
            d,r=q; target=canon[r]
            if derived(w,target): continue
            if zf(target)<3.7 or zf(target)-zf(w)<1.0: continue
            key=(n,r)
            if key in seen: continue
            seen.add(key); cs.append((w,target,d,zf(w),zf(target),li,line.strip()))
    lines += [f'## قسمت {ep}',f'- موارد شدید: **{len(cs)}**','']
    for a,t,d,fa,fb,li,line in cs:
        lines.append(f'- L{li}: `{a}` → `{t}` | edit={d} | {fa:.2f}→{fb:.2f} | {line}')
    lines.append('')
REPORT.write_text('\n'.join(lines),encoding='utf-8'); print(REPORT)

from pathlib import Path
import re, math
from collections import Counter
try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
except Exception as e:
    raise SystemExit(f'sklearn required: {e}')

ROOT=Path('.')
OUT=ROOT/'outputs/khane_to/review/md'
REF=ROOT/'متن ها/khane-to'
REPORT=ROOT/'reports/khane_to_semantic_reconciliation.md'

STOP=set('و در به از که را با برای این آن یک می ما شما من تو او هم یا اما اگر چون تا روی توی خیلی فقط شده شود شده‌است هست است بود باشد یعنی خب حالا دیگه بعد قبل هر چه چه‌قدر وقتی کردن کرد کنه میشه می‌شه داره داریم دارند'.split())
AR2FA=str.maketrans({'ي':'ی','ى':'ی','ك':'ک','ۀ':'ه','ة':'ه','ؤ':'و','إ':'ا','أ':'ا'})

def norm(s):
    s=s.translate(AR2FA)
    s=re.sub(r'https?://\S+',' ',s)
    s=re.sub(r'\*\*[^*]+\*\*',' ',s)
    s=re.sub(r'[`#>*_\[\]()]',' ',s)
    s=re.sub(r'[^0-9A-Za-z\u0600-\u06ff]+',' ',s)
    return re.sub(r'\s+',' ',s).strip().lower()

def substantive_paras(text):
    chunks=[x.strip() for x in re.split(r'\n\s*\n',text) if x.strip()]
    out=[]
    for c in chunks:
        if re.fullmatch(r'\*\*[^*]+\*\*',c): continue
        if c.startswith('#') or c.startswith('>'): continue
        if c.startswith('برنامه «') or c.startswith('مدت:') or c.startswith('منبع:'): continue
        n=norm(c)
        if len(n.split())>=10: out.append(c)
    return out

def metadata(text):
    title=''
    for ln in text.splitlines():
        if ln.startswith('# '): title=ln[2:].strip(); break
    dur=re.search(r'مدت:\s*([^\n]+)',text)
    src=re.search(r'منبع:\s*(https?://\S+)',text)
    return title, (dur.group(1).strip() if dur else ''), (src.group(1) if src else '')

def tokens(s): return [w for w in norm(s).split() if w not in STOP and len(w)>1]

lines=['# تطبیق معنایی Output و متن‌ها — خانه تو','',
       'این گزارش برای یافتن اختلاف‌های واقعی ساخته شده است؛ Output متن مادر است و متن دوم فقط مرجع اصلاح/بازیابی است.','']
summary=[]
for ep in range(1,14):
    op=(OUT/f'{ep}.md').read_text(encoding='utf-8')
    rp=(REF/f'episode-{ep:02d}.md').read_text(encoding='utf-8')
    opars=substantive_paras(op); rpars=substantive_paras(rp)
    docs=[norm(x) for x in opars+rpars]
    vec=TfidfVectorizer(analyzer='word',ngram_range=(1,2),min_df=1,sublinear_tf=True)
    X=vec.fit_transform(docs)
    O=X[:len(opars)]; R=X[len(opars):]
    sims=cosine_similarity(R,O) if len(opars) and len(rpars) else []
    lows=[]; meds=[]; highs=[]
    for i,p in enumerate(rpars):
        if len(opars):
            j=int(sims[i].argmax()); sc=float(sims[i,j]); best=opars[j]
        else: j=-1; sc=0; best=''
        rec=(sc,p,best)
        if sc<0.16: lows.append(rec)
        elif sc<0.30: meds.append(rec)
        else: highs.append(rec)
    title,dur,src=metadata(rp)
    ow=len(tokens(op)); rw=len(tokens(rp))
    summary.append((ep,ow,rw,len(rpars),len(highs),len(meds),len(lows)))
    lines += [f'## قسمت {ep} — {title}',f'- مدت مرجع: {dur}',f'- منبع: {src}',f'- حجم واژگانی: Output={ow} | متن‌ها={rw} | نسبت={rw/ow:.2f}×',f'- پاراگراف‌های مرجع: قوی={len(highs)} | متوسط={len(meds)} | ضعیف={len(lows)}','']
    if lows:
        lines.append('### کاندیدهای نیازمند بررسی دستی')
        for k,(sc,p,best) in enumerate(sorted(lows,key=lambda x:x[0])[:12],1):
            p1=re.sub(r'\s+',' ',p)[:700]
            b1=re.sub(r'\s+',' ',best)[:700]
            lines += [f'**{k}. امتیاز {sc:.2f}**',f'- متن‌ها: {p1}',f'- نزدیک‌ترین Output: {b1}','']
    # Distinct numbers/latin tokens from reference absent in output
    nums=sorted(set(re.findall(r'(?<!\w)[0-9۰-۹]+(?:[./٪%][0-9۰-۹]+)?',rp)))
    latin=sorted(set(re.findall(r'\b[A-Za-z][A-Za-z0-9-]{2,}\b',rp,re.I)))
    miss_nums=[x for x in nums if x not in op]
    miss_lat=[x for x in latin if x.lower() not in op.lower()]
    if miss_nums or miss_lat:
        lines.append('### نشانگرهای دقیقِ مرجع که عیناً در Output نیستند')
        if miss_nums: lines.append('- اعداد/نشان‌ها: '+', '.join(miss_nums[:30]))
        if miss_lat: lines.append('- لاتین: '+', '.join(miss_lat[:30]))
        lines.append('')

lines += ['# جمع‌بندی عددی','', '| قسمت | Output | متن‌ها | پاراگراف مرجع | قوی | متوسط | ضعیف |','|---:|---:|---:|---:|---:|---:|---:|']
for row in summary:
    lines.append('| '+' | '.join(map(str,row))+' |')
REPORT.write_text('\n'.join(lines),encoding='utf-8')
print('wrote',REPORT)

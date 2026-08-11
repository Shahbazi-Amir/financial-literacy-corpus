from pathlib import Path
import re, math
from collections import Counter

ROOT=Path('.')
OUT=ROOT/'outputs/khane_to/review/md'
REF=ROOT/'متن ها/khane-to'
REPORT=ROOT/'reports/khane_to_output_vs_texts_audit.md'

AR2FA=str.maketrans({'ي':'ی','ى':'ی','ك':'ک','ۀ':'ه','ة':'ه','ؤ':'و','إ':'ا','أ':'ا'})

def norm(s):
    s=s.translate(AR2FA)
    s=re.sub(r'\*\*[^*]+\*\*',' ',s)
    s=re.sub(r'https?://\S+',' ',s)
    s=re.sub(r'[`#>*_\[\]()]',' ',s)
    s=re.sub(r'[^\w\u0600-\u06ff]+',' ',s)
    s=re.sub(r'\s+',' ',s).strip().lower()
    return s

def words(s): return norm(s).split()
def shingles(ws,n=3): return set(tuple(ws[i:i+n]) for i in range(max(0,len(ws)-n+1)))

def coverage(a,b):
    A=shingles(words(a)); B=shingles(words(b))
    if not A: return 0.0
    return len(A&B)/len(A)

def paras(s):
    # discard markdown speaker-only labels and short headings; keep substantive paragraphs
    chunks=[x.strip() for x in re.split(r'\n\s*\n',s) if x.strip()]
    out=[]
    for c in chunks:
        if re.fullmatch(r'\*\*[^*]+\*\*',c): continue
        if c.startswith('#'): continue
        if c.startswith('برنامه «') or c.startswith('مدت:') or c.startswith('منبع:') or c.startswith('>'): continue
        if len(words(c))>=8: out.append(c)
    return out

def best_cov(p, others):
    if not others: return 0.0
    return max(coverage(p,o) for o in others)

# 1) remove all remaining [نامفهوم] markers only
removed={}
for ep in range(1,14):
    p=OUT/f'{ep}.md'
    txt=p.read_text(encoding='utf-8')
    cnt=txt.count('[نامفهوم]')
    txt=txt.replace('[نامفهوم]','')
    # only clean spaces caused directly by marker deletion
    txt=re.sub(r' +([،؛؟!,.])',r'\1',txt)
    txt=re.sub(r' {2,}',' ',txt)
    txt=re.sub(r'\n +','\n',txt)
    p.write_text(txt,encoding='utf-8')
    removed[ep]=cnt

lines=['# ممیزی مقایسه Output و متن‌ها — خانه تو','',
       '## قاعده','- Output اصلاح‌شده، متن مادر است.','- `متن ها/khane-to` فقط مرجع تطبیق، تصحیح و بازیابی است.','- این مرحله هیچ محتوایی از مرجع دوم را وارد Output یا Final نمی‌کند.','']
lines.append('## حذف `[نامفهوم]`')
lines.append(f'- مجموع حذف‌شده: **{sum(removed.values())}**')
for ep,c in removed.items(): lines.append(f'- قسمت {ep}: {c}')
lines.append('')
lines.append('## سنجه‌های زوجی')
lines.append('| قسمت | Output words | متن‌ها words | نسبت متن‌ها/Output | پوشش متن‌ها→Output | پوشش Output→متن‌ها |')
lines.append('|---:|---:|---:|---:|---:|---:|')

all_candidates=[]
for ep in range(1,14):
    op=(OUT/f'{ep}.md').read_text(encoding='utf-8')
    rp=(REF/f'episode-{ep:02d}.md').read_text(encoding='utf-8')
    ow=len(words(op)); rw=len(words(rp))
    r2o=coverage(rp,op); o2r=coverage(op,rp)
    ratio=(rw/ow if ow else 0)
    lines.append(f'| {ep} | {ow} | {rw} | {ratio:.2f}× | {r2o:.1%} | {o2r:.1%} |')
    op_par=paras(op); rp_par=paras(rp)
    # paragraphs from ref poorly represented in output = possible correction/unique reference material
    ref_unique=[]
    for p in rp_par:
        bc=best_cov(p,op_par)
        if bc < 0.35:
            ref_unique.append((bc,p))
    # output paragraphs poorly represented in ref = content preserved only by mother
    out_unique=[]
    for p in op_par:
        bc=best_cov(p,rp_par)
        if bc < 0.25:
            out_unique.append((bc,p))
    all_candidates.append((ep,ref_unique,out_unique))

lines += ['','## اختلاف‌های محتوایی کاندید','',
          'این بخش فقط کاندید است؛ اختلاف بیان، خلاصه‌سازی و ادغام گفت‌وگو می‌تواند باعث امتیاز پایین شود.','']
for ep,ru,ou in all_candidates:
    lines.append(f'### قسمت {ep}')
    lines.append(f'- پاراگراف‌های مرجع با پوشش پایین در Output: **{len(ru)}**')
    for score,p in sorted(ru,key=lambda x:x[0])[:8]:
        sample=re.sub(r'\s+',' ',p)[:600]
        lines.append(f'  - پوشش {score:.0%}: {sample}')
    lines.append(f'- پاراگراف‌های Output با پوشش پایین در متن‌ها: **{len(ou)}**')
    for score,p in sorted(ou,key=lambda x:x[0])[:5]:
        sample=re.sub(r'\s+',' ',p)[:500]
        lines.append(f'  - پوشش {score:.0%}: {sample}')
    lines.append('')

lines += ['## نتیجه اولیه','- هر ۱۳ زوج موجود و شماره‌گذاری آن‌ها یک‌به‌یک است.','- تصمیم مادر/مرجع باید بر اساس پوشش و خواندن کاندیدهای بالا انجام شود؛ نسبت حجم به‌تنهایی معیار نهایی نیست.']
REPORT.write_text('\n'.join(lines),encoding='utf-8')
print('removed',sum(removed.values()),'wrote',REPORT)

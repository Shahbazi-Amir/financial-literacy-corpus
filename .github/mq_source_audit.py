from pathlib import Path
import re, difflib

OUT=Path('outputs/mq/review/md')
REF=Path('متن ها/mq/md')
REPORT=Path('reports/mq_source_audit.md')

BAD_PATTERNS=[
 'دقدقه','محارت','دوچار','تلاتوم','ناعتمین','کس با کار','ثواد','اسطلاح','ازترار','زخیره',
 'بورت','سهان','سحام','صحام','قرد','نقض شوند','خیش فرمای','پجوه','ترراحی','نوستان',
 'تشقیص','حدررفت','انترنت','رمزرز','رمزرس','خانابد','معلف','کنترول','مرفع','توصیع',
 'مذیعت','کارگوزار','کارموست','اقصات','روشت','اردش','صود','سانویه','تلاتم','مواژه'
]

def numbered(p):
    return {int(f.stem):f for f in p.glob('*.md') if f.stem.isdigit()}

def norm(s):
    s=s.replace('ي','ی').replace('ك','ک').replace('\u200c',' ')
    s=re.sub(r'[^\w\sآ-ی۰-۹]',' ',s)
    return re.sub(r'\s+',' ',s).strip().lower()

def words(s):
    return re.findall(r'[آ-یA-Za-z0-9۰-۹_]+', norm(s))

def headings(s):
    return re.findall(r'^\*\*([^*\n]+)\*\*\s*$',s,flags=re.M)

def consecutive_dup_heads(s):
    hs=headings(s)
    return sum(a==b for a,b in zip(hs,hs[1:]))

def similarity(a,b):
    return difflib.SequenceMatcher(None,words(a),words(b),autojunk=True).ratio()

def positive_spans(a,b,min_delta=8):
    aw,bw=words(a),words(b)
    sm=difflib.SequenceMatcher(None,aw,bw,autojunk=True)
    spans=[]
    for tag,i1,i2,j1,j2 in sm.get_opcodes():
        alen=i2-i1; blen=j2-j1; delta=blen-alen
        if (tag=='insert' and blen>=min_delta) or (tag=='replace' and delta>=min_delta):
            spans.append((delta,tag,' '.join(aw[max(0,i1-12):min(len(aw),i2+12)]),' '.join(bw[max(0,j1-12):min(len(bw),j2+12)])))
    return sorted(spans,reverse=True,key=lambda x:x[0])

outs=numbered(OUT); refs=numbered(REF); nums=sorted(set(outs)|set(refs))
lines=['# ممیزی منابع MQ','',
'هدف: تعیین متن مادر، کیفیت نسبی ASR، افتادگی‌های احتمالی و نقاط نیازمند بازخوانی انسانی.','',
'## ساختار','',
f'- Output: **{len(outs)}** فایل — `{sorted(outs)}`',
f'- متن مرجع: **{len(refs)}** فایل — `{sorted(refs)}`',
f'- فقط Output: `{sorted(set(outs)-set(refs))}`',
f'- فقط متن مرجع: `{sorted(set(refs)-set(outs))}`','',
'## مقایسه قسمت‌به‌قسمت','',
'| قسمت | کلمات Output | کلمات Ref | O/R | شباهت | نامفهوم O/R | ASR بد O/R | تکرار گوینده O/R | Ref-only ≥8 | Output-only ≥8 |','|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|']
refheavy={}; outheavy={}; susp=[]
for n in nums:
    if n not in outs or n not in refs: continue
    o=outs[n].read_text(encoding='utf-8'); r=refs[n].read_text(encoding='utf-8')
    ow,rw=len(words(o)),len(words(r)); op=[p for p in BAD_PATTERNS if p in o]; rp=[p for p in BAD_PATTERNS if p in r]
    rhs=positive_spans(o,r,8); ohs=positive_spans(r,o,8)
    if rhs: refheavy[n]=rhs
    if ohs: outheavy[n]=ohs
    lines.append(f'| {n} | {ow} | {rw} | {ow/rw:.2f} | {similarity(o,r):.3f} | {o.count("[نامفهوم]")}/{r.count("[نامفهوم]")} | {len(op)}/{len(rp)} | {consecutive_dup_heads(o)}/{consecutive_dup_heads(r)} | {len(rhs)} | {len(ohs)} |')
    for p in op:
        for m in list(re.finditer(re.escape(p),o))[:3]:
            a=max(0,m.start()-120); b=min(len(o),m.end()+180)
            susp.append((n,p,re.sub(r'\s+',' ',o[a:b]).strip()))

lines += ['', '## کاندیدهای ASR باقی‌مانده در Output','']
if susp:
    for n,p,ctx in susp: lines += [f'- **قسمت {n} — `{p}`**: {ctx}']
else: lines += ['- هیچ‌یک از الگوهای شناخته‌شدهٔ بالا در Output پیدا نشد.']

lines += ['', '## بازه‌های Ref که نسبت به Output محتوای بیشتری دارند','',
'این‌ها فقط کاندید هستند؛ تکرار، ASR خراب و تفاوت جمله‌بندی می‌تواند کاندید کاذب بسازد.','']
for n,spans in refheavy.items():
    lines += [f'### قسمت {n} — {len(spans)} کاندید','']
    for delta,tag,oc,rc in spans[:20]:
        lines += [f'- **{tag} / مازاد تقریبی Ref: {delta} واژه**',f'  - Output: `{oc[:700]}`',f'  - Ref: `{rc[:900]}`','']
    if len(spans)>20: lines += [f'- ... {len(spans)-20} مورد کوچک‌تر دیگر.','']

lines += ['', '## بازه‌های Output که نسبت به Ref محتوای بیشتری دارند','']
for n,spans in outheavy.items():
    lines += [f'### قسمت {n} — {len(spans)} کاندید','']
    for delta,tag,rc,oc in spans[:12]:
        lines += [f'- **{tag} / مازاد تقریبی Output: {delta} واژه**',f'  - Ref: `{rc[:700]}`',f'  - Output: `{oc[:900]}`','']
    if len(spans)>12: lines += [f'- ... {len(spans)-12} مورد کوچک‌تر دیگر.','']

lines += ['', '## نتیجهٔ ماشینی','',
'- این گزارش فقط غربال است و اجازهٔ جایگزینی خودکار هیچ متنی را نمی‌دهد.',
'- متن مادر باید با توجه به پوشش محتوا، کیفیت ASR و بازخوانی انسانی تعیین شود.',
'- هر اصلاح باید با شاهد مستقیم از دو منبع یا صوت پشتیبانی شود.','']
REPORT.parent.mkdir(exist_ok=True)
REPORT.write_text('\n'.join(lines),encoding='utf-8')
print('audited',len(outs),len(refs),'refheavy',len(refheavy),'outheavy',len(outheavy),'susp',len(susp))

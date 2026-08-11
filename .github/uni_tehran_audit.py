from pathlib import Path
import re, difflib

OUT=Path('outputs/uni_tehran/review/md')
REF=Path('متن ها/uni_tehran/md')
REVIEW=Path('متن ها/uni_tehran/review/md')
REPORT=Path('reports/uni_tehran_source_audit.md')

BAD_PATTERNS=[
 'دقدقه','محارت','دوچار','تلاتوم','ناعتمین','کس با کار','ثواد','اسطلاح','ازترار','زخیره',
 'بورت','سهان','سحام','صحام','قرد','نقض شوند','خیش فرمای','پجوه','پجوش','ترراحی','نوستان',
 'تشقیص','حدررفت','انترنت','رمزرز','رمزرس','خانابد','ثبتگردان','معلف','جامپستار','جامپسار',
 'گذینه','کنترول','مرفع','بیس سال','دویتر','برارت زمانه','نبو و','نوت درصد','توانگری به سرایی همی روید'
]

def numbered(p):
    d={}
    for f in p.glob('*.md'):
        if f.stem.isdigit(): d[int(f.stem)]=f
    return d

def norm(s):
    s=s.replace('ي','ی').replace('ك','ک').replace('\u200c',' ')
    s=re.sub(r'[^\w\sآ-ی]',' ',s)
    s=re.sub(r'\s+',' ',s).strip().lower()
    return s

def words(s): return re.findall(r'[آ-یA-Za-z0-9_]+', norm(s))

def headings(s): return re.findall(r'^\*\*([^*\n]+)\*\*\s*$',s,flags=re.M)

def consecutive_dup_heads(s):
    hs=headings(s); return sum(a==b for a,b in zip(hs,hs[1:]))

def similarity(a,b): return difflib.SequenceMatcher(None,words(a),words(b),autojunk=True).ratio()

def ref_positive_spans(o,r,min_delta=8):
    ow,rw=words(o),words(r)
    sm=difflib.SequenceMatcher(None,ow,rw,autojunk=True)
    spans=[]
    for tag,i1,i2,j1,j2 in sm.get_opcodes():
        olen=i2-i1; rlen=j2-j1; delta=rlen-olen
        if (tag=='insert' and rlen>=min_delta) or (tag=='replace' and delta>=min_delta):
            spans.append((delta,tag,' '.join(ow[max(0,i1-14):min(len(ow),i2+14)]),' '.join(rw[max(0,j1-14):min(len(rw),j2+14)])))
    spans.sort(reverse=True,key=lambda x:x[0])
    return spans

outs=numbered(OUT); refs=numbered(REF); reviews=numbered(REVIEW)
allnums=sorted(set(outs)|set(refs))
mirror_equal=sum(1 for n in outs if n in reviews and outs[n].read_bytes()==reviews[n].read_bytes())
lines=['# ممیزی منابع دانشگاه تهران','',
'هدف: تعیین هم‌ترازی دو منبع، کیفیت نسبی ASR، و تشخیص اینکه کدام نسخه باید متن مادر باشد.','',
'## ساختار','',
f'- فایل‌های شماره‌دار Output: **{len(outs)}** — {min(outs) if outs else "-"} تا {max(outs) if outs else "-"}',
f'- فایل‌های شماره‌دار متن خام: **{len(refs)}** — {min(refs) if refs else "-"} تا {max(refs) if refs else "-"}',
f'- فایل‌های mirror در `متن ها/uni_tehran/review/md`: **{len(reviews)}**؛ برابر byte-for-byte با Output: **{mirror_equal}/{len(outs)}**',
f'- فقط در Output: `{sorted(set(outs)-set(refs))}`',
f'- فقط در متن خام: `{sorted(set(refs)-set(outs))}`','',
'## مقایسه قسمت‌به‌قسمت','',
'| قسمت | کلمات Output | کلمات متن خام | نسبت O/R | شباهت توکنی | نامفهوم O/R | الگوی ASR بد O/R | تکرار پیاپی گوینده O/R | کاندید ref-only ≥8 |','|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|']

susp=[]; heavy={}
for n in allnums:
    if n not in outs or n not in refs: continue
    o=outs[n].read_text(encoding='utf-8'); r=refs[n].read_text(encoding='utf-8')
    ow,rw=len(words(o)),len(words(r))
    op=[p for p in BAD_PATTERNS if p in o]
    rp=[p for p in BAD_PATTERNS if p in r]
    hs=ref_positive_spans(o,r,8)
    lines.append(f'| {n} | {ow} | {rw} | {ow/rw:.2f} | {similarity(o,r):.3f} | {o.count("[نامفهوم]")}/{r.count("[نامفهوم]")} | {len(op)}/{len(rp)} | {consecutive_dup_heads(o)}/{consecutive_dup_heads(r)} | {len(hs)} |')
    if hs: heavy[n]=hs
    if op:
        for p in op:
            for m in list(re.finditer(re.escape(p),o))[:3]:
                a=max(0,m.start()-130); b=min(len(o),m.end()+180)
                ctx=re.sub(r'\s+',' ',o[a:b]).strip()
                susp.append((n,p,ctx))

lines += ['', '## کاندیدهای ASR باقی‌مانده در Output','']
if susp:
    for n,p,ctx in susp: lines += [f'- **قسمت {n} — `{p}`**: {ctx}']
else:
    lines += ['- هیچ‌کدام از الگوهای شناخته‌شدهٔ ASR خام در Output پیدا نشد.']

lines += ['', '## بازه‌های متن خام با مازاد محتوایی ≥ ۸ واژه نسبت به Output','',
'این بخش غربال اولیه است؛ تفاوت شدید ASR یا تکرار متن می‌تواند کاندید کاذب بسازد.','']
if not heavy:
    lines.append('- کاندید پیدا نشد.')
else:
    for n,spans in heavy.items():
        lines += [f'### قسمت {n} — {len(spans)} کاندید','']
        for delta,tag,oc,rc in spans[:12]:
            lines += [f'- **{tag} / مازاد تقریبی متن خام: {delta} واژه**',f'  - Output: `{oc[:520]}`',f'  - Raw: `{rc[:760]}`','']
        if len(spans)>12: lines += [f'- ... {len(spans)-12} کاندید کوچک‌تر دیگر در غربال ماشینی.','']

lines += ['', '## جمع‌بندی ماشینی','',
'- Output و `متن ها/uni_tehran/review/md` یک نسخه‌اند؛ مرجع مستقل واقعی `متن ها/uni_tehran/md` است.',
'- نسبت حجم و شباهت فقط برای تشخیص ساختار استفاده می‌شود و مجوز جایگزینی خودکار متن نیست.',
'- اگر Output هم‌تراز و پاک‌تر باشد، Output مادر است و متن خام فقط برای بازیابی افتادگی/تصحیح قطعی استفاده می‌شود.','']
REPORT.parent.mkdir(exist_ok=True)
REPORT.write_text('\n'.join(lines),encoding='utf-8')
print('audited',len(outs),len(refs),'mirror',mirror_equal,'suspicious',len(susp),'episodes with candidates',len(heavy))

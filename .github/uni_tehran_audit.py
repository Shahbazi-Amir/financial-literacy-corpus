from pathlib import Path
import re, difflib

OUT=Path('outputs/uni_tehran/review/md')
REF=Path('متن ها/uni_tehran/md')
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

def matcher(a,b): return difflib.SequenceMatcher(None,words(a),words(b),autojunk=True)

def similarity(a,b): return matcher(a,b).ratio()

def ref_heavy_spans(o,r):
    ow,rw=words(o),words(r)
    sm=difflib.SequenceMatcher(None,ow,rw,autojunk=True)
    spans=[]
    for tag,i1,i2,j1,j2 in sm.get_opcodes():
        olen=i2-i1; rlen=j2-j1
        if (tag=='insert' and rlen>=18) or (tag=='replace' and rlen-olen>=18):
            spans.append((rlen-olen,tag,' '.join(ow[max(0,i1-18):min(len(ow),i2+18)]),' '.join(rw[max(0,j1-18):min(len(rw),j2+18)])))
    spans.sort(reverse=True,key=lambda x:x[0])
    return spans[:5]

outs=numbered(OUT); refs=numbered(REF)
allnums=sorted(set(outs)|set(refs))
lines=['# ممیزی منابع دانشگاه تهران','',
'هدف: تعیین هم‌ترازی دو منبع، کیفیت نسبی ASR، و تشخیص اینکه کدام نسخه باید متن مادر باشد.','',
'## ساختار','',
f'- فایل‌های شماره‌دار Output: **{len(outs)}** — {min(outs) if outs else "-"} تا {max(outs) if outs else "-"}',
f'- فایل‌های شماره‌دار متن‌ها: **{len(refs)}** — {min(refs) if refs else "-"} تا {max(refs) if refs else "-"}',
f'- فقط در Output: `{sorted(set(outs)-set(refs))}`',
f'- فقط در متن‌ها: `{sorted(set(refs)-set(outs))}`','',
'## مقایسه قسمت‌به‌قسمت','',
'| قسمت | کلمات Output | کلمات متن‌ها | نسبت O/R | شباهت توکنی | نامفهوم O/R | الگوی ASR بد O/R | تکرار پیاپی گوینده O/R |','|---:|---:|---:|---:|---:|---:|---:|---:|---:|']

susp=[]; heavy={}
for n in allnums:
    if n not in outs or n not in refs: continue
    o=outs[n].read_text(encoding='utf-8'); r=refs[n].read_text(encoding='utf-8')
    ow,rw=len(words(o)),len(words(r))
    op=[p for p in BAD_PATTERNS if p in o]
    rp=[p for p in BAD_PATTERNS if p in r]
    lines.append(f'| {n} | {ow} | {rw} | {ow/rw:.2f} | {similarity(o,r):.3f} | {o.count("[نامفهوم]")}/{r.count("[نامفهوم]")} | {len(op)}/{len(rp)} | {consecutive_dup_heads(o)}/{consecutive_dup_heads(r)} |')
    hs=ref_heavy_spans(o,r)
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

lines += ['', '## بازه‌های بزرگ‌تر در متن‌ها که ممکن است از Output افتاده باشند','',
'این بخش فقط کاندید است؛ تفاوت شدید ASR یا تکرار متن هم می‌تواند چنین بازه‌ای بسازد.','']
if not heavy:
    lines.append('- کاندید بزرگ پیدا نشد.')
else:
    for n,spans in heavy.items():
        lines += [f'### قسمت {n}','']
        for delta,tag,oc,rc in spans:
            lines += [f'- **{tag} / مازاد تقریبی متن‌ها: {delta} واژه**',f'  - Output context: `{oc[:650]}`',f'  - متن‌ها context: `{rc[:900]}`','']

lines += ['', '## جمع‌بندی ماشینی','',
'- نسبت حجم و شباهت فقط برای تشخیص ساختار استفاده می‌شود و مجوز جایگزینی خودکار متن نیست.',
'- فهرست بالا باید پیش از هر اصلاح به‌صورت معنایی/دستی بررسی شود.',
'- اگر Output در همه قسمت‌ها هم‌تراز و از نظر ASR پاک‌تر باشد، Output مادر و `متن ها` مرجع اصلاحی خواهد بود.','']
REPORT.parent.mkdir(exist_ok=True)
REPORT.write_text('\n'.join(lines),encoding='utf-8')
print('audited',len(outs),len(refs),'suspicious output hits',len(susp),'episodes with ref-heavy spans',len(heavy))

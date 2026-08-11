from pathlib import Path
import re, math, difflib

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

def headings(s):
    return re.findall(r'^\*\*([^*\n]+)\*\*\s*$',s,flags=re.M)

def consecutive_dup_heads(s):
    hs=headings(s); return sum(a==b for a,b in zip(hs,hs[1:]))

def similarity(a,b):
    # compact token SequenceMatcher sample
    aw=words(a); bw=words(b)
    return difflib.SequenceMatcher(None,aw,bw,autojunk=True).ratio()

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

susp=[]
for n in allnums:
    if n not in outs or n not in refs: continue
    o=outs[n].read_text(encoding='utf-8'); r=refs[n].read_text(encoding='utf-8')
    ow,rw=len(words(o)),len(words(r))
    op=[p for p in BAD_PATTERNS if p in o]
    rp=[p for p in BAD_PATTERNS if p in r]
    lines.append(f'| {n} | {ow} | {rw} | {ow/rw:.2f} | {similarity(o,r):.3f} | {o.count("[نامفهوم]")}/{r.count("[نامفهوم]")} | {len(op)}/{len(rp)} | {consecutive_dup_heads(o)}/{consecutive_dup_heads(r)} |')
    if op:
        for p in op:
            for m in list(re.finditer(re.escape(p),o))[:3]:
                a=max(0,m.start()-130); b=min(len(o),m.end()+180)
                ctx=re.sub(r'\s+',' ',o[a:b]).strip()
                susp.append((n,p,ctx))

lines += ['', '## کاندیدهای ASR باقی‌مانده در Output','']
if susp:
    for n,p,ctx in susp:
        lines += [f'- **قسمت {n} — `{p}`**: {ctx}']
else:
    lines += ['- هیچ‌کدام از الگوهای شناخته‌شدهٔ ASR خام در Output پیدا نشد.']

# crude exact n-gram containment: detects whether ref is mostly a noisier sibling vs separate content
lines += ['', '## جمع‌بندی ماشینی','',
'- نسبت حجم و شباهت فقط برای تشخیص ساختار استفاده می‌شود و مجوز جایگزینی خودکار متن نیست.',
'- فهرست بالا باید پیش از هر اصلاح به‌صورت معنایی/دستی بررسی شود.',
'- اگر Output در همه قسمت‌ها هم‌تراز و از نظر ASR پاک‌تر باشد، Output مادر و `متن ها` مرجع اصلاحی خواهد بود.','']
REPORT.parent.mkdir(exist_ok=True)
REPORT.write_text('\n'.join(lines),encoding='utf-8')
print('audited',len(outs),len(refs),'suspicious output hits',len(susp))

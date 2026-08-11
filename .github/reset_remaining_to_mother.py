from pathlib import Path
import re, shutil
ROOT=Path('.')
REPORTS=ROOT/'reports'; REPORTS.mkdir(exist_ok=True)
collections=[
 ('khane_to','خانه تو','outputs/khane_to/review/md','متن ها/khane-to','final/khane-to',13),
 ('mq','MQ','outputs/mq/review/md','متن ها/mq/md','final/mq',8),
 ('tarbiat_morabi','تربیت مربی','outputs/tarbiat_morabi/review/md','متن ها/tarbiat_morabi/md','final/tarbiat-morabi',14),
 ('uni_tehran','دانشگاه تهران','outputs/uni_tehran/review/md','متن ها/uni_tehran/md','final/uni-tehran',38),
]
def n(p):
    x=re.findall(r'\d+',p.stem); return int(x[-1]) if x else 9999
def collect(path): return {n(p):p for p in Path(path).glob('*.md') if p.is_file()}
idx=[]
for slug,title,op,rp,fp,expected in collections:
    om,rm=collect(op),collect(rp)
    if len(om)!=expected or len(rm)!=expected or set(om)!=set(rm):
        raise SystemExit(f'PAIRING_FAIL {slug}: output={len(om)} ref={len(rm)}')
    fdir=Path(fp); fdir.mkdir(parents=True,exist_ok=True)
    for p in fdir.glob('*.md'): p.unlink()
    rep=[f'# گزارش نهایی‌سازی — {title}','',
         '## تصمیم نهایی و روش امن',
         '- Output متن مادر و نسخهٔ نهایی پایه است.',
         '- `متن ها` مرجع دوم مقایسه/تصحیح است، اما در Audit مشخص شد بعضی شکل‌های واژگانی آن از Output بدتر است؛ بنابراین هیچ جایگزینی خودکار از Agent وارد Final نشده است.',
         '- Final هر قسمت در این مرحله byte-for-byte از متن مادر Output کپی شده تا هیچ گفت‌وگو، مثال، عدد، ضرب‌المثل یا سبک گفتار از دست نرود.',
         '- مرجع دوم برای جفت‌سازی، کنترل پوشش و بازبینی بعدی نگه داشته می‌شود. هر تصحیح واژه‌ای آینده باید با صوت/ویدئو یا شاهد قطعی انجام شود.',
         '- اجرای قبلیِ جایگزینی خودکار که در Audit نمونه‌های معکوس مثل «سواد→ثواد» نشان داد، کامل برگشت داده شده و جزو Final نهایی نیست.','',
         '## موجودی',f'- Output: {len(om)}',f'- مرجع دوم: {len(rm)}',f'- جفت‌شده: {len(set(om)&set(rm))}','']
    for k in sorted(om):
        src=om[k]; ref=rm[k]; dst=fdir/f'{k:02d}.md'
        shutil.copyfile(src,dst)
        a=src.read_bytes(); b=ref.read_bytes(); c=dst.read_bytes()
        if a!=c: raise SystemExit(f'COPY_MISMATCH {slug} {k}')
        rep += [f'### قسمت {k}',f'- مادر: `{src}` — {len(a)} بایت',f'- مرجع دوم: `{ref}` — {len(b)} بایت',f'- Final: `{dst}` — **عین متن مادر**','']
    rep += ['## نتیجه',f'- {expected} فایل Final ساخته و با متن مادر تطبیق بایتی شدند.', '- منبع‌های `outputs/` و `متن ها/` تغییر نکرده‌اند.','']
    (REPORTS/f'{slug}_finalization.md').write_text('\n'.join(rep),encoding='utf-8')
    idx.append((title,expected,fp))
# Update index
lines=['# فهرست گزارش‌های نهایی‌سازی','', '- `asre_shirin_finalization.md`','- گزارش‌های در جستجوی خوشبختی در همین پوشه باقی مانده‌اند.','- `khane_to_finalization.md`','- `mq_finalization.md`','- `tarbiat_morabi_finalization.md`','- `uni_tehran_finalization.md`','','## وضعیت امن نهایی این مرحله']
for title,count,fp in idx:
    lines.append(f'- **{title}**: {count} Final، Output مادر، Agent مرجع دوم، هیچ جایگزینی خودکار Agent، مسیر=`{fp}/`')
lines += ['','> Audit محافظتی: جایگزینی‌های خودکار اجرای قبلی به دلیل مشاهدهٔ اصلاحات معکوس/نامعتبر کامل rollback شدند.']
(REPORTS/'FINALIZATION_INDEX.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')

from pathlib import Path
import re, shutil, difflib, unicodedata, os

ROOT=Path('.')
REPORTS=ROOT/'reports'; REPORTS.mkdir(exist_ok=True)

# --- helpers ---
def natural(p):
    m=re.findall(r'\d+',p.stem)
    return (int(m[-1]) if m else 10**9,p.name)

def norm_word(s):
    return unicodedata.normalize('NFKC',s).replace('ي','ی').replace('ك','ک')

def words_with_spans(text):
    return [(m.group(),m.start(),m.end()) for m in re.finditer(r'[A-Za-z0-9_\u0600-\u06FF]+',text)]

def editdist(a,b):
    a,b=norm_word(a),norm_word(b)
    if a==b:return 0
    prev=list(range(len(b)+1))
    for i,x in enumerate(a,1):
        cur=[i]
        for j,y in enumerate(b,1):
            cur.append(min(cur[-1]+1,prev[j]+1,prev[j-1]+(x!=y)))
        prev=cur
    return prev[-1]

def reconcile(base,ref):
    """Preserve base wholesale. Only accept a single-token repair when 4-word context
    on each side is identical and spell distance is <=1 (<=2 for words >=7 chars).
    This deliberately misses ambiguous repairs rather than risking content loss."""
    bw=words_with_spans(base); rw=words_with_spans(ref)
    bt=[norm_word(x[0]) for x in bw]; rt=[norm_word(x[0]) for x in rw]
    sm=difflib.SequenceMatcher(a=bt,b=rt,autojunk=False)
    candidates=[]
    for tag,i1,i2,j1,j2 in sm.get_opcodes():
        if tag!='replace' or i2-i1!=1 or j2-j1!=1: continue
        a,b=bt[i1],rt[j1]
        if a==b or len(a)<3 or len(b)<3: continue
        lim=2 if max(len(a),len(b))>=7 else 1
        if editdist(a,b)>lim: continue
        L=4
        if bt[max(0,i1-L):i1] != rt[max(0,j1-L):j1]: continue
        if bt[i2:i2+L] != rt[j2:j2+L]: continue
        # Avoid normal orthographic/style variants and numbers.
        if a.isdigit() or b.isdigit(): continue
        if {a,b} in ({'می','مى'},): continue
        candidates.append((bw[i1][1],bw[i1][2],a,b))
    # Do not allow multiple different replacements of same surface word.
    by={}
    for s,e,a,b in candidates: by.setdefault(a,set()).add(b)
    candidates=[x for x in candidates if len(by[x[2]])==1]
    out=base; changes=[]
    for s,e,a,b in reversed(candidates):
        out=out[:s]+b+out[e:]
        changes.append((a,b))
    changes.reverse()
    return out,changes

def collect(path):
    return sorted([p for p in Path(path).glob('*.md') if p.is_file()],key=natural)

def output_map(path):
    return {natural(p)[0]:p for p in collect(path)}

def ref_map(path):
    return {natural(p)[0]:p for p in collect(path)}

# --- relocate Dar Jostojo extraction under its Final-C ---
src=ROOT/'extracted/dar-jostojo-source3'
dst=ROOT/'final/dar-jostojo-final-C/extracted/source3'
if src.exists():
    dst.parent.mkdir(parents=True,exist_ok=True)
    if dst.exists(): shutil.rmtree(dst)
    shutil.copytree(src,dst)
    shutil.rmtree(src)

collections=[
 ('khane_to','خانه تو','outputs/khane_to/review/md','متن ها/khane-to','final/khane-to'),
 ('mq','MQ','outputs/mq/review/md','متن ها/mq/md','final/mq'),
 ('tarbiat_morabi','تربیت مربی','outputs/tarbiat_morabi/review/md','متن ها/tarbiat_morabi/md','final/tarbiat-morabi'),
 ('uni_tehran','دانشگاه تهران','outputs/uni_tehran/review/md','متن ها/uni_tehran/md','final/uni-tehran'),
]

index=[]
for slug,title,op,rp,fp in collections:
    om,rm=output_map(op),ref_map(rp)
    common=sorted(set(om)&set(rm))
    only_o=sorted(set(om)-set(rm)); only_r=sorted(set(rm)-set(om))
    fdir=Path(fp); fdir.mkdir(parents=True,exist_ok=True)
    for old in fdir.glob('*.md'): old.unlink()
    rep=[f'# گزارش نهایی‌سازی — {title}','',
         '## روش','- Output متن مادر است و بدنهٔ آن حفظ می‌شود.',
         '- `متن ها` فقط مرجع دوم برای تصحیح است.',
         '- هیچ خلاصه‌سازی، رسمی‌سازی، حذف مثال/عدد/گفت‌وگو یا جایگزینی حجمی از Agent انجام نشده است.',
         '- اصلاح خودکار فقط وقتی مجاز بوده که اختلاف یک واژه باشد، ۴ واژه قبل و بعد در هر دو منبع یکسان باشند، و فاصله املایی بسیار کم باشد.',
         '- اختلاف‌های مبهم عمداً دست‌نخورده مانده‌اند تا بعداً با صوت/ویدئو بررسی شوند.','',
         '## موجودی',f'- Output: {len(om)} فایل',f'- مرجع دوم: {len(rm)} فایل',f'- جفت یک‌به‌یک: {len(common)} فایل','']
    allchanges=0
    for n in common:
        b=om[n].read_text(encoding='utf-8',errors='replace')
        r=rm[n].read_text(encoding='utf-8',errors='replace')
        fixed,changes=reconcile(b,r)
        out=fdir/f'{n:02d}.md'; out.write_text(fixed,encoding='utf-8')
        allchanges+=len(changes)
        rep += [f'### قسمت {n}',
                f'- مادر: `{om[n]}` — {len(b)} کاراکتر',
                f'- مرجع دوم: `{rm[n]}` — {len(r)} کاراکتر',
                f'- Final: `{out}` — {len(fixed)} کاراکتر']
        if changes:
            rep.append('- اصلاحات بسیار قطعی: '+ '، '.join(f'`{a}` → `{c}`' for a,c in changes))
        else:
            rep.append('- اصلاح بسیار قطعی قابل‌اعمال: ندارد؛ متن مادر عیناً حفظ شد.')
        rep.append('')
    if only_o: rep += ['## فقط در Output',', '.join(map(str,only_o)),'']
    if only_r: rep += ['## فقط در مرجع دوم',', '.join(map(str,only_r)),'']
    rep += ['## جمع‌بندی',f'- Final ساخته‌شده: {len(common)} فایل',f'- تعداد اصلاحات محافظه‌کارانه: {allchanges}',f'- مسیر: `{fp}/`','']
    (REPORTS/f'{slug}_finalization.md').write_text('\n'.join(rep),encoding='utf-8')
    index.append((title,len(om),len(rm),len(common),allchanges,fp))

# Asre Shirin concise report
asre=list((ROOT/'final/asre_shirin').rglob('episode-*.md'))
(REPORTS/'asre_shirin_finalization.md').write_text(f'''# گزارش نهایی‌سازی — عصر شیرین

## روش
- Output متن مادر بود؛ Agent فقط برای ASR، نام‌ها، اعداد و metadata.
- گفت‌وگو، مثال‌ها، ضرب‌المثل‌ها و سبک دکتر حفظ شدند.
- میان‌برنامه‌های خارج از دانش اصلی حذف شدند.
- قسمت ۱۵ پس از اضافه‌شدن Output تکمیل شد.

## خروجی
- تعداد Finalها: {len(asre)}
- مسیر: `final/asre_shirin/`
''',encoding='utf-8')

idx=['# فهرست گزارش‌های نهایی‌سازی','', '- `asre_shirin_finalization.md`','- گزارش‌های در جستجوی خوشبختی در همین پوشه باقی مانده‌اند.','- `khane_to_finalization.md`','- `mq_finalization.md`','- `tarbiat_morabi_finalization.md`','- `uni_tehran_finalization.md`','','## وضعیت اجرای این مرحله']
for title,a,b,c,d,fp in index:
    idx.append(f'- **{title}**: Output={a}، مرجع دوم={b}، Final={c}، اصلاحات قطعی={d}، مسیر=`{fp}/`')
(REPORTS/'FINALIZATION_INDEX.md').write_text('\n'.join(idx)+'\n',encoding='utf-8')

# Safety: all four must have exact expected pair counts.
expected={'khane_to':13,'mq':8,'tarbiat_morabi':14,'uni_tehran':38}
for slug,title,op,rp,fp in collections:
    if len(output_map(op))!=expected[slug] or len(ref_map(rp))!=expected[slug]:
        raise SystemExit(f'COUNT_MISMATCH {slug}: output={len(output_map(op))} ref={len(ref_map(rp))}')
    if len(list(Path(fp).glob('*.md')))!=expected[slug]:
        raise SystemExit(f'FINAL_COUNT_MISMATCH {slug}')

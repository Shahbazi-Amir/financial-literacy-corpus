from pathlib import Path
from difflib import SequenceMatcher
import re

OUT = Path('outputs/tarbiat_morabi/review/md')
REF = Path('متن ها/tarbiat_morabi/md')
REP = Path('reports/tarbiat_morabi_source_audit.md')
CAND = Path('reports/tarbiat_morabi_merge_candidates.md')

word_re = re.compile(r'[\w\u200c]+', re.UNICODE)
BAD = ['[نامفهوم]', 'زبان تشخیص داده شده', 'نامفهوم', 'صحام', 'سندوق', 'استراری', 'ازتراری', 'قرز', 'پجوهش', 'اسطلاح', 'تلاتم', 'توصیع', 'روشت', 'مواژه', 'صود']

def words(s):
    return word_re.findall(s.replace('ي','ی').replace('ك','ک'))

def ctx(tokens, start, end, n=10):
    return ' '.join(tokens[max(0,start-n):min(len(tokens),end+n)])

rows=[]
candidates=[]
for i in range(1,15):
    op = OUT / f'{i}.md'
    rp = REF / f'{i}.md'
    o = op.read_text(encoding='utf-8')
    r = rp.read_text(encoding='utf-8')
    ow, rw = words(o), words(r)
    sm = SequenceMatcher(None, ow, rw, autojunk=False)
    ratio = sm.ratio()
    bad_o = {b:o.count(b) for b in BAD if b in o}
    bad_r = {b:r.count(b) for b in BAD if b in r}
    rows.append((i, len(o), len(r), len(ow), len(rw), ratio, bad_o, bad_r))

    local=[]
    for tag,a1,a2,b1,b2 in sm.get_opcodes():
        if tag == 'equal':
            continue
        os = ow[a1:a2]
        rs = rw[b1:b2]
        # Keep only material spans: either side >= 8 words, or a clear insertion/deletion >= 5 words.
        if max(len(os),len(rs)) < 8 and not ((not os or not rs) and max(len(os),len(rs)) >= 5):
            continue
        # Skip obvious ASR footer noise.
        joined = ' '.join(rs+os)
        if 'زبان تشخیص داده شده' in joined:
            continue
        local.append((tag,a1,a2,b1,b2,os,rs))
    candidates.append((i, local))

lines=['# ممیزی منبع تربیت مربی','',
       '- مادر از پیش تعیین نشده؛ تصمیم بر اساس مقایسه ۱۴ جفت گرفته می‌شود.',
       '- این گزارش فقط برای Audit است و هیچ ادغام خودکاری مجاز نیست.','',
       '|قسمت|کاراکتر Output|کاراکتر Ref|واژه Output|واژه Ref|شباهت|مشکوک Output|مشکوک Ref|',
       '|---:|---:|---:|---:|---:|---:|---|---|']
for i,oc,rc,owc,rwc,ratio,bo,br in rows:
    lines.append(f'|{i}|{oc}|{rc}|{owc}|{rwc}|{ratio:.4f}|{bo or "—"}|{br or "—"}|')
lines += ['', '## جمع‌بندی ماشینی', '']
for i,oc,rc,owc,rwc,ratio,bo,br in rows:
    delta = owc-rwc
    direction = 'Output بلندتر' if delta>0 else ('Ref بلندتر' if delta<0 else 'برابر')
    lines.append(f'- قسمت {i}: {direction} ({delta:+d} واژه)، شباهت {ratio:.4f}؛ placeholder/ASR مشکوک Output={bo or "صفر"}، Ref={br or "صفر"}.')
REP.write_text('\n'.join(lines)+'\n', encoding='utf-8')

cl=['# کاندیدهای اختلاف تربیت مربی','',
    'فقط بازه‌های مادی برای بازخوانی انسانی. این فایل مجوز جایگزینی خودکار نیست.','']
for i, local in candidates:
    cl += [f'## قسمت {i} — {len(local)} کاندید','']
    for n,(tag,a1,a2,b1,b2,os,rs) in enumerate(local,1):
        cl += [f'### {i}.{n} — {tag} — Output {len(os)} / Ref {len(rs)} واژه',
               f'- Output context: `{ctx(words((OUT/f"{i}.md").read_text(encoding="utf-8")),a1,a2)}`',
               f'- **Output span:** `{" ".join(os)}`',
               f'- Ref context: `{ctx(words((REF/f"{i}.md").read_text(encoding="utf-8")),b1,b2)}`',
               f'- **Ref span:** `{" ".join(rs)}`','']
CAND.write_text('\n'.join(cl)+'\n', encoding='utf-8')

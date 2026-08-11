from pathlib import Path
import re
import hashlib

OUT_DIR = Path('outputs/khane_to/review/md')
REF_DIR = Path('متن ها/khane-to')
FINAL_DIR = Path('final/khane-to')
REPORT = Path('reports/khane_to_finalization.md')

GLOBAL_REPLACEMENTS = {
    'خیش فرمایی': 'خویش‌فرمایی',
    'خیش‌فرمایی': 'خویش‌فرمایی',
    'کس با کار': 'کسب‌وکار',
    'کار فرما': 'کارفرما',
    'حیجانی': 'هیجانی',
    'بورت': 'بورس',
    'نقد شونده': 'نقدشونده',
    'چرخی اقتصاد': 'چرخهٔ اقتصاد',
}

EP_REPLACEMENTS = {
    2: {
        '**فرهاد جم / دکتر کمیل رودی**\n\nآموزش می‌شه؟ نه، نه. نه. نه. نه.': '**فرهاد جم**\n\nآموزش می‌شه؟\n\n**دکتر کمیل رودی**\n\nنه، نه. نه. نه. نه.',
    },
    5: {
        'وردش باید باید بپردازی': 'ورزش باید باید بپردازی',
        'ازولاد توی کشش و قدرت و استقامت تقویت می‌شه': 'عضلات توی کشش و قدرت و استقامت تقویت می‌شه',
    },
    6: {
        'با نهایت تأثیر و تأثیر باید بگم': 'با نهایت تأسف و احتیاط باید بگم',
        'از ازار بدهی': 'از نظر بدهی',
        'پس‌انداز بگیریم': 'قرض بگیریم',
        'تو عوضی مدیریت مالی': 'تو حوزهٔ مدیریت مالی',
    },
    12: {
        'فرمایی رو پر می‌کنید': 'فرم‌هایی رو پر می‌کنید',
    },
    13: {
        'قضاوه کنم': 'قضاوت کنم',
    },
}

MIXED_HEADING = '**فرهاد جم / دکتر کمیل رودی**'
SPEAKERS = ('فرهاد جم', 'دکتر کمیل رودی')


def sha(text: str) -> str:
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def parse_reference_header(text: str):
    lines = text.splitlines()
    title = lines[0].lstrip('#').strip() if lines else ''
    meta = []
    for line in lines[1:12]:
        s = line.strip()
        if not s:
            continue
        if s.startswith('>') or s.startswith('##'):
            break
        if s.startswith('برنامه ') or s.startswith('گفت‌وگوی ') or s.startswith('مدت:') or s.startswith('منبع:'):
            meta.append(s)
    return title, meta


def strip_output_title(text: str) -> str:
    lines = text.splitlines()
    if lines and lines[0].startswith('# '):
        lines = lines[1:]
        while lines and not lines[0].strip():
            lines.pop(0)
    return '\n'.join(lines).rstrip() + '\n'


def normalize_mixed_speakers(text: str):
    lines = text.splitlines()
    out = []
    i = 0
    resolved = 0
    unresolved = 0
    while i < len(lines):
        line = lines[i]
        if line.strip() != MIXED_HEADING:
            out.append(line)
            i += 1
            continue

        i += 1
        chunk = []
        while i < len(lines):
            s = lines[i].strip()
            if s.startswith('**') and s.endswith('**'):
                break
            chunk.append(lines[i])
            i += 1

        converted = []
        had_labeled = False
        ambiguous_nonempty = False
        for c in chunk:
            st = c.strip()
            matched = False
            for speaker in SPEAKERS:
                prefix = speaker + ':'
                if st.startswith(prefix):
                    had_labeled = True
                    matched = True
                    content = st[len(prefix):].strip()
                    if converted and converted[-1] != '':
                        converted.append('')
                    converted.extend([f'**{speaker}**', '', content])
                    resolved += 1
                    break
            if not matched:
                if st:
                    ambiguous_nonempty = True
                converted.append(c)

        if had_labeled and not ambiguous_nonempty:
            while converted and converted[0] == '':
                converted.pop(0)
            out.extend(converted)
        else:
            out.append(MIXED_HEADING)
            out.extend(chunk)
            unresolved += 1
    return '\n'.join(out), resolved, unresolved


def apply_replacements(text: str, ep: int):
    applied = []
    for old, new in {**GLOBAL_REPLACEMENTS, **EP_REPLACEMENTS.get(ep, {})}.items():
        n = text.count(old)
        if n:
            text = text.replace(old, new)
            applied.append((old, new, n))
    return text, applied


FINAL_DIR.mkdir(parents=True, exist_ok=True)
REPORT.parent.mkdir(parents=True, exist_ok=True)

report = [
    '# گزارش نهایی‌سازی مجموعه «خانه تو»',
    '',
    '## قواعد',
    '- متن مادر: `outputs/khane_to/review/md/`.',
    '- مرجع دوم: `متن ها/khane-to/` فقط برای عنوان/متادیتا و اصلاح‌های قطعی.',
    '- هیچ خلاصه‌سازی یا بازنویسی رسمی روی بدنه انجام نشده است.',
    '- هیچ عبارت `[نامفهوم]` وارد Final نمی‌شود.',
    '- برچسب گوینده فقط وقتی شکسته می‌شود که شاهد صریح در همان گفت‌وگو وجود داشته باشد.',
    '- اصلاح‌های بازسازی‌شده فقط در مواردی اعمال می‌شوند که مرجع دوم معنای همان شکست ASR را به‌طور مستقیم تأیید کند.',
    '',
    '## نتیجهٔ قسمت‌ها',
]

unresolved_total = 0
for ep in range(1, 14):
    out_path = OUT_DIR / f'{ep}.md'
    ref_path = REF_DIR / f'episode-{ep:02d}.md'
    assert out_path.exists(), out_path
    assert ref_path.exists(), ref_path

    mother = out_path.read_text(encoding='utf-8')
    ref = ref_path.read_text(encoding='utf-8')
    assert '[نامفهوم]' not in mother, f'episode {ep}: mother still has [نامفهوم]'

    title, meta = parse_reference_header(ref)
    body = strip_output_title(mother)
    body, applied = apply_replacements(body, ep)
    body, resolved, unresolved = normalize_mixed_speakers(body)
    unresolved_total += unresolved

    header = [f'# {title}', '']
    header.extend(meta)
    header.extend(['', '---', ''])
    final_text = '\n'.join(header) + body.lstrip('\n')

    assert '[نامفهوم]' not in final_text
    assert MIXED_HEADING not in final_text, f'episode {ep}: mixed speaker heading remains'
    (FINAL_DIR / f'episode-{ep:02d}.md').write_text(final_text, encoding='utf-8')

    report.append(f'### قسمت {ep:02d} — {title}')
    report.append(f'- SHA-256 متن مادر: `{sha(mother)}`')
    report.append(f'- SHA-256 Final: `{sha(final_text)}`')
    report.append(f'- نوبت‌های گویندهٔ ترکیبی که با شاهد صریح شکسته شدند: **{resolved}**')
    report.append(f'- بلوک‌های گویندهٔ ترکیبیِ حل‌نشده: **{unresolved}**')
    if applied:
        report.append('- اصلاح‌های قطعی اعمال‌شده:')
        for old, new, n in applied:
            report.append(f'  - `{old}` → `{new}` × {n}')
    else:
        report.append('- اصلاح واژگانی قطعی اضافه در این مرحله: ندارد.')
    report.append('')

report.extend([
    '## کنترل نهایی',
    '- تعداد فایل Final: **13**.',
    f'- بلوک‌های گویندهٔ ترکیبیِ باقی‌مانده: **{unresolved_total}**.',
    '- فایل‌های منبع در `outputs/` و `متن ها/` در این مرحله دست‌کاری نشده‌اند.',
    '- متن‌های Final از متن مادر ساخته شده‌اند و مرجع دوم جایگزین بدنه نشده است.',
])
REPORT.write_text('\n'.join(report).rstrip() + '\n', encoding='utf-8')

files = sorted(FINAL_DIR.glob('episode-*.md'))
assert len(files) == 13, len(files)
for p in files:
    t = p.read_text(encoding='utf-8')
    assert '[نامفهوم]' not in t, p
    assert MIXED_HEADING not in t, p
assert unresolved_total == 0, unresolved_total
print('khane-to finalization complete:', len(files), 'files; unresolved mixed blocks:', unresolved_total)

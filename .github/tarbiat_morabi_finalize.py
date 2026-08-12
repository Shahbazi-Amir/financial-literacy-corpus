from pathlib import Path
import hashlib

SRC = Path('outputs/tarbiat_morabi/review/md')
REF = Path('متن ها/tarbiat_morabi/md')
DST = Path('final/tarbiat-morabi')
REPORT = Path('reports/tarbiat_morabi_finalization.md')

REPL = {
    3: [
        ('لخت شستن', 'رخت شستن'),
    ],
    4: [
        ('گفت ما فاتم مذا و ما سیعتی کفعن قوم فقتن ملفورست و بین الادمن',
         'گفت: «ما فات مضى و ما سيأتيك فأين؟ قم فاغتنم الفرصة بين العدمين.»'),
    ],
    5: [
        ('یعنی همیت محبه است بر قصد تعلق محبوب از غیر و غیر از محبوب',
         'یعنی «غیرت، حمیت محب است بر طلب قطع تعلق محبوب از غیر یا تعلق غیر از محبوب.»'),
    ],
    9: [
        ('به سرمویی پسرخاله‌ای یا دوستی', 'به پسرعمویی، پسرخاله‌ای یا دوستی'),
    ],
    11: [
        ('بابا این فرض کن بندازه یه دو هفته پول توجیبی‌ت‌ها',
         'بابا این فرض کن به اندازه‌ی دو هفته پول توجیبی‌ته‌ها'),
        ('ممنونم از اتا', 'ممنونم از توجهتون'),
    ],
    12: [
        ('دختر گلم، به سر گلم، گلم', 'دختر گلم، پسر گلم، گلم'),
        ('در اصطلاح می‌گن گیونه', 'در اصطلاح می‌گن given'),
        ('نگاه اعتراضی و نگاه شکرانه', 'نگاه اعتراضی و نگاه ناشکرانه'),
        ('مثلا فرض به ماهی ۵۰۰ هزار تومن', 'مثلا فرض کن ماهی ۵۰۰ هزار تومن'),
        ('چه بدونم لس‌آنجلس', 'چه می‌دونم لس‌آنجلس'),
    ],
    14: [
        ('یک، مشهوده.\n\nدو، از ارائه‌دهنده جدا نمی‌شه.',
         'یک، نامشهوده.\n\nدو، از ارائه‌دهنده جدا نمی‌شه.'),
    ],
}

UNRESOLVED = {
    3: [
        'ویروسی و عفونتی با سری مزهری توش نیست',
        'تخم‌مرغ می‌دادن، الف می‌گرفتن',
        'به قول این کتاب ما سه کیسه پشت می‌دادن جای اون چیزی که می‌خواستن',
        'شیر می‌گرفتن، الف می‌دادن',
        'از این چیزبازی‌هایی که در قدیم هم وجود داشته',
    ],
    4: [
        'ست سال سیام آینده نیاد',
    ],
    12: [
        'این شهر رو تو چیکار کردی؟',
        'من قبل می‌گیرم و من قبل می‌گیرم',
        'هدیه اوتی نده',
    ],
    13: [
        'والدینی که هم‌سن ماها هستن بیم / یا خب باید دارم بچه هم رو تأمین می‌کنن',
        'بیشتر برای آشنایی جمعه / یه ترویجی ندار / بگیم حتماً برای این کار / مثلاً چما می‌تونی پول دریافت بکنیم',
        'اگر مسواک بزنی / به دنگه پول می‌دن',
        'چون زود نمی‌خواه اینو در اضای عمور مالی انجام بدیم',
    ],
}

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

# Freeze source hashes before writing final files.
before_src = {p.name: sha(p) for p in sorted(SRC.glob('*.md'))}
before_ref = {p.name: sha(p) for p in sorted(REF.glob('*.md'))}
assert len(before_src) == 14 and len(before_ref) == 14

DST.mkdir(parents=True, exist_ok=True)
for p in DST.glob('episode-*.md'):
    p.unlink()

applied = []
for i in range(1, 15):
    text = (SRC / f'{i}.md').read_text(encoding='utf-8')
    for old, new in REPL.get(i, []):
        count = text.count(old)
        if count != 1:
            raise SystemExit(f'episode {i}: expected one occurrence of {old!r}, found {count}')
        text = text.replace(old, new, 1)
        applied.append((i, old, new))
    (DST / f'episode-{i:02d}.md').write_text(text, encoding='utf-8')

# Source isolation.
after_src = {p.name: sha(p) for p in sorted(SRC.glob('*.md'))}
after_ref = {p.name: sha(p) for p in sorted(REF.glob('*.md'))}
assert before_src == after_src
assert before_ref == after_ref

# Final validation.
finals = sorted(DST.glob('episode-*.md'))
assert len(finals) == 14
for p in finals:
    text = p.read_text(encoding='utf-8')
    assert '[نامفهوم]' not in text
    assert 'زبان تشخیص‌داده‌شده' not in text
    assert 'زبان تشخیص داده شده' not in text

for i, old, new in applied:
    text = (DST / f'episode-{i:02d}.md').read_text(encoding='utf-8')
    assert old not in text
    assert new in text

lines = [
    '# گزارش نهایی‌سازی مجموعه تربیت مربی', '',
    '## تصمیم منبع', '',
    '- هر دو منبع ۱۴ قسمت هم‌تراز دارند.',
    '- `outputs/tarbiat_morabi/review/md/` مادر نهایی انتخاب شد: متن خواناتر، کم‌خطاتر و از نظر محتوایی کامل‌تر است.',
    '- `متن ها/tarbiat_morabi/md/` فقط مرجع ثانویه برای تشخیص اختلاف، اعداد و خطاهای ASR بود؛ جایگزینی کور از آن انجام نشد.',
    '- ممیزی افتادگی نشان داد هیچ محتوای مستقل و قابل‌اعتماد چندواژه‌ای از Ref در Output حذف نشده است؛ موارد Ref-only یا نویز ASR، تکرار یا جابه‌جایی همان عبارت بودند.', '',
    '## اصلاحات قطعی اعمال‌شده', ''
]
for i, old, new in applied:
    lines.append(f'- قسمت {i}: `{old}` → `{new}`')

lines += ['', '## موارد نیازمند تطبیق با صوت', '',
          'این عبارت‌ها در هر دو متن مبهم/خراب‌اند و بدون صوت تصحیح نشدند؛ متن مادر در Final دست‌نخورده حفظ شده است.','']
for i in sorted(UNRESOLVED):
    lines.append(f'### قسمت {i}')
    for s in UNRESOLVED[i]:
        lines.append(f'- `{s}`')
    lines.append('')

lines += [
    '## ملاحظات و کنترل نهایی', '',
    '- نقل «ما فات مضى...» در قسمت ۴ با منبع مستقل متنی تطبیق داده شد.',
    '- تعریف «غیرت، حمیت محب...» در قسمت ۵ با منابع لغوی/عرفانی مستقل تطبیق داده شد.',
    '- چارچوب‌ها، اعداد، مثال‌ها، لحن محاوره‌ای و دیدگاه‌های گوینده بازنویسی یا fact-check نشدند.',
    '- Final شامل ۱۴ فایل است.',
    '- `[نامفهوم]`: صفر.',
    '- متادیتای خام ASR: صفر.',
    '- فایل‌های `outputs/tarbiat_morabi/` و `متن ها/tarbiat_morabi/` در فرایند Final تغییر نکردند.',
    f'- تعداد اصلاحات قطعی: {len(applied)}.',
    f'- تعداد عبارت‌های ثبت‌شده برای تطبیق صوتی: {sum(map(len, UNRESOLVED.values()))}.',
]
REPORT.write_text('\n'.join(lines) + '\n', encoding='utf-8')
print(f'finalized 14 episodes; applied={len(applied)} unresolved={sum(map(len, UNRESOLVED.values()))}')

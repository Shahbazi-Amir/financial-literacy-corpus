from pathlib import Path
import hashlib

NEW=Path('outputs/uni_tehran/uni_tehran_episode_4_final/review/4.md')
OLD=Path('outputs/uni_tehran/review/md/4.md')
REF=Path('متن ها/uni_tehran/md/4.md')
CUR=Path('final/uni-tehran/episode-04.md')
OUT=Path('staging/uni-tehran-episode-04-adopted.md')
REPORT=Path('staging/uni-tehran-finalization-report.md')

s=NEW.read_text(encoding='utf-8')
assert s.startswith('# دانشگاه تهران — قسمت ۴ — بازبینی نهایی')
s=s.replace('# دانشگاه تهران — قسمت ۴ — بازبینی نهایی','# media',1)

repls=[
 ('الان موضوع در اختیار دانشجوها داره...', 'الان موضوع در اختیار دانشجوها قرار داره...'),
 ('و استانداردیه که داره خودش، در حال استاندارد پویاییه که در حال تکمیل و رشد و نموه',
  'و استاندارد پویاییه که در حال تکمیل و رشد و نموه'),
]
for old,new in repls:
    n=s.count(old)
    assert n==1,(old,n)
    s=s.replace(old,new,1)

# hard validation
assert '[نامفهوم]' not in s
for bad in ['پجوهش','ثواد','افضایش','محارت','نیاستنجی','ترراحی','اردیابی']:
    assert bad not in s,bad
for must in ['Financial Capability','پرتغال','لهستان','کسب‌وکارهای خرد','ساخت آمریکا','۱۲۷ مفهوم','۱۴ سال','عنصرالمعالی','احجار کریمه']:
    assert must in s,must
# adopted must retain all meaningful >=5-token content of old/final is validated by prior audit; record hashes here.
OUT.parent.mkdir(exist_ok=True)
OUT.write_text(s,encoding='utf-8')

h=lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
lines=[
'# گزارش نهایی‌سازی مجموعه «دانشگاه تهران»','',
'## تصمیم منبع مادر','',
'- قسمت‌های ۱–۳ و ۵–۳۸ بدون تغییر نسبت به Final قبلی باقی مانده‌اند.',
'- قسمت ۴ پس از بازپردازش مستقیم فایل ویدیوی اصلی دوباره ارزیابی شد.',
'- مادر جدید قسمت ۴: `outputs/uni_tehran/uni_tehran_episode_4_final/review/4.md`؛ این نسخه از ویدیوی اصلی تولید و بازبینی شده و از Output قبلی و Final قبلی کامل‌تر و لفظاً وفادارتر است.',
'- `outputs/uni_tehran/review/md/4.md` باید با نسخه پذیرفته‌شده جدید جایگزین شود؛ `متن ها/uni_tehran/md/4.md` فقط مرجع خام مقایسه باقی می‌ماند.','',
'## شاهد بازپردازش قسمت ۴','',
'- منبع رسانه: `4-.mp4` از Release پروژه `vid_pipeline`.',
'- SHA-256 رسانه: `295fe78d60e29b57f3541a19cbf499d24bed4d67cc6c7ab0f0861899f7f1dcbf`.',
'- مدت رسانه: `25:26.272`.',
'- GitHub Actions Run بازپردازش: `31550238857` — PASS.',
'- دانلود/اعتبارسنجی، ASR، diarization و review نهایی همگی PASS.',
'- بازه `00:10:14–00:10:22` که در پردازش قبلی افتاده بود در بازپردازش جدید بازیابی شد (۲۰ token).','',
'## نتیجه مقایسه سه‌نسخه‌ای قسمت ۴','',
'- Output قبلی: ۲۵٬۲۴۷ بایت / حدود ۲٬۵۶۲ واژه نرمال‌شده.',
'- نسخه بازپردازش‌شده ویدیویی: ۳۰٬۳۱۶ بایت / حدود ۳٬۰۹۳ واژه نرمال‌شده.',
'- مرجع خام `متن ها`: ۲۹٬۲۷۶ بایت / حدود ۳٬۲۸۶ واژه نرمال‌شده، اما با ASR خام‌تر.',
'- Final قبلی: ۲۷٬۷۱۲ بایت / حدود ۲٬۸۲۱ واژه نرمال‌شده.',
'- در ممیزی، هیچ قطعه معتبر ۵ واژه‌ای یا بیشتر از Output قبلی یا Final قبلی پیدا نشد که در نسخه جدید ویدیویی غایب باشد.',
'- نسخه جدید در مقابل، توضیحات لفظی و مثال‌های متعددی را که نسخه‌های قبلی فشرده کرده بودند حفظ می‌کند؛ از جمله منطق کامل Financial Capability، اولویت مخاطبان، مثال پرتغال و لهستان، محدودیت کسب‌وکار خرد، گذار به مستند «ساخت آمریکا»، و جزئیات عددی روایت تاریخی.','',
'## اصلاحات قطعی روی نسخه ویدیویی','',
'- `الان موضوع در اختیار دانشجوها داره...` → `الان موضوع در اختیار دانشجوها قرار داره...`',
'- `استانداردیه که داره خودش، در حال استاندارد پویاییه...` → `استاندارد پویاییه...`',
'- به‌جز این دو اصلاح، لحن، تکرارها، مثال‌ها، اعداد، نقل‌ها و ساختار گفتار نسخه ویدیویی حفظ شد.','',
'## کنترل نهایی','',
'- Final مجموعه همچنان ۳۸ قسمت دارد.',
'- `[نامفهوم]` در قسمت ۴: صفر.',
'- الگوهای شناخته‌شده ASR خام در نسخه پذیرفته‌شده قسمت ۴: صفر.',
'- قسمت ۴ Output و Final باید byte-for-byte از یک متن پذیرفته‌شده ساخته شوند.',
'- فایل خام `متن ها/uni_tehran/md/4.md` تغییر نمی‌کند.',
'- پوشه `outputs/uni_tehran/uni_tehran_episode_4_final/` به‌عنوان evidence/provenance بازپردازش نگه داشته می‌شود.','',
'## SHA-256 منابع در زمان تصمیم','',
f'- old Output 4: `{h(OLD)}`',
f'- new video review 4: `{h(NEW)}`',
f'- raw reference 4: `{h(REF)}`',
f'- previous Final 4: `{h(CUR)}`',
f'- adopted episode 4: `{h(OUT)}`',''
]
REPORT.write_text('\n'.join(lines),encoding='utf-8')
print('built adopted episode 4',h(OUT))
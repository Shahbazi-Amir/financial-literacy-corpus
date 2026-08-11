from pathlib import Path
import re, unicodedata
from collections import Counter
from wordfreq import zipf_frequency
ROOT=Path('.'); OUT=ROOT/'outputs/khane_to/review/md'; REF=ROOT/'متن ها/khane-to'; DEST=ROOT/'reports/khane_to_asr_post'
rx=re.compile(r"[\u0600-\u06FF\u200c]+")
def norm(s): return unicodedata.normalize('NFKC',s).replace('ي','ی').replace('ك','ک').replace('\u200c','').lower().strip('،؛؟!:.')
def zf(w): return zipf_frequency(norm(w),'fa')
refset=set()
for p in REF.glob('episode-*.md'):
    refset.update(norm(w) for w in rx.findall(p.read_text(encoding='utf-8')))
VALID={norm(x) for x in ['ناسلامتی','خانواده‌ست','صبح‌ها','دیگه‌ای','تعریفش','آینده‌تو','ارتباط‌ها','تمرینه','اعتباره','همگانیه','حرفه‌ایه','بازپرداختش','متعالیه','درش','همینی','اونچه','زندگیه','دومش','دردم','کمکت','طبیعیه','راحت‌تر','خدایی','بتونن','بپرسی','نزدیک‌تر','مالیه','قدرتی','سؤالات','آن‌چنان','منطبق','خیلی‌ها','به‌فرض','مدیریتش','پاسخش','درآمدت','عرضم','کیفیتش','دینیه','اعتبارت','راجع‌به','هرجوری','بی‌دغدغه','بدهیه','دولت‌هایی','پیشنهادم','مطرحه','جمعش','یک‌سری','همه‌مون','دکترهای','موضوعی‌ست','فرمودی','بدهی‌ام','شغلمه','بپردازن','ششمیه','آمدین','نظام‌های','اقتضا','کنز','نمی‌اومد','می‌آییم','ذهنمونه','ببرنش','نمی‌خواسته','ارزاق','شدنیه','بپیچم','گرون‌تر','تومنه','بخرمش','تمکن','هم‌گروه','نیاریم','به‌خاطر','ترغیبه','به‌راحتی','تندرست','صدمه‌ای','سودت','مکروهه','ریسکو','کناریه','زندگیو','چقدرشو','نمیشین','خسارتشونو','عمرمونه','سلامتمونه','ماشینمونه','اختیاریه']}
SUF=('هامون','هاتون','هاشون','مون','تون','شون','هام','هات','هاش')
def suspicious(w):
    n=norm(w)
    if len(n)<3 or n in refset or n in VALID or any(n.endswith(s) for s in SUF): return False
    return zf(w)<2.35
DEST.mkdir(parents=True,exist_ok=True)
summary=[]
for ep in range(1,14):
    src=(OUT/f'{ep}.md').read_text(encoding='utf-8').splitlines(); rows=[f'# خانه تو {ep} — Post-ASR audit','']; count=0
    for i,line in enumerate(src,1):
        bad=[]
        for w in rx.findall(line):
            if suspicious(w) and w not in bad: bad.append(w)
        if bad or '[نامفهوم]' in line:
            count+=1; rows += [f'## L{i}',f'- مشکوک: {", ".join(f"`{x}`" for x in bad) if bad else "[نامفهوم]"}','',line.strip(),'']
    rows.insert(2,f'- تعداد خطوط مشکوک: **{count}**'); rows.insert(3,'')
    (DEST/f'{ep:02d}.md').write_text('\n'.join(rows),encoding='utf-8'); summary.append((ep,count))
(Path('reports/khane_to_asr_post_summary.md')).write_text('# Post-ASR summary\n\n'+'\n'.join(f'- {e}: {c}' for e,c in summary)+'\n',encoding='utf-8')
print(summary)

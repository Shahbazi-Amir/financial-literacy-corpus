from pathlib import Path
import re, unicodedata
from collections import Counter
from wordfreq import zipf_frequency
ROOT=Path('.'); OUT=ROOT/'outputs/khane_to/review/md'; REF=ROOT/'متن ها/khane-to'; DEST=ROOT/'reports/khane_to_asr_lines'
rx=re.compile(r"[\u0600-\u06FF\u200c]+")
def norm(s): return unicodedata.normalize('NFKC',s).replace('ي','ی').replace('ك','ک').replace('\u200c','').lower().strip('،؛؟!:.')
def zf(w): return zipf_frequency(norm(w),'fa')
refset=set()
for p in REF.glob('episode-*.md'):
  for w in rx.findall(p.read_text(encoding='utf-8')): refset.add(norm(w))
VALID={norm(x) for x in ['ناسلامتی','خانواده‌ست','صبح‌ها','دیگه‌ای','تعریفش','آینده‌تو','ارتباط‌ها','تمرینه','اعتباره','همگانیه','حرفه‌ایه','بازپرداختش','متعالیه','درش','همینی','اونچه','زندگیه','دومش','دردم','کمکت','طبیعیه','راحت‌تر','خدایی','بتونن','بپرسی','نزدیک‌تر','مالیه','قدرتی','سؤالات','آن‌چنان','منطبق','خیلی‌ها','به‌فرض','مدیریتش','پاسخش','درآمدت','عرضم','کیفیتش','دینیه','اعتبارت','راجع‌به','هرجوری','بی‌دغدغه','بدهیه','دولت‌هایی','پیشنهادم','مطرحه','جمعش','یک‌سری','همه‌مون','دکترهای','موضوعی‌ست','فرمودی','بدهی‌ام','شغلمه','بپردازن','ششمیه','آمدین','نظام‌های','اقتضا','کنز','نمی‌اومد','می‌آییم','ذهنمونه','ببرنش','نمی‌خواسته','ارزاق','شدنیه','بپیچم','گرون‌تر','تومنه','بخرمش','تمکن','هم‌گروه','نیاریم','به‌خاطر','ترغیبه','به‌راحتی','تندرست','صدمه‌ای','سودت']}
# very common valid colloquial suffix patterns: don't flag merely for morphology
SUF=('هامون','هاتون','هاشون','مون','تون','شون','هام','هات','هاش')
def suspicious(w):
  n=norm(w)
  if len(n)<3 or n in refset or n in VALID or any(n.endswith(s) for s in SUF): return False
  return zf(w)<2.45
DEST.mkdir(parents=True,exist_ok=True)
for ep in range(1,14):
  src=(OUT/f'{ep}.md').read_text(encoding='utf-8').splitlines()
  rows=[f'# خانه تو {ep} — خطوط مشکوک ASR','']
  count=0
  for i,line in enumerate(src,1):
    ws=rx.findall(line); bad=[]
    for w in ws:
      if suspicious(w) and w not in bad: bad.append(w)
    if bad or '[نامفهوم]' in line:
      count+=1; rows.append(f'## L{i}'); rows.append(f'- مشکوک: {", ".join(f"`{x}`" for x in bad) if bad else "[نامفهوم]"}'); rows.append(''); rows.append(line); rows.append('')
  rows.insert(2,f'- تعداد خطوط: **{count}**'); rows.insert(3,'')
  (DEST/f'{ep:02d}.md').write_text('\n'.join(rows),encoding='utf-8')
print('wrote',DEST)

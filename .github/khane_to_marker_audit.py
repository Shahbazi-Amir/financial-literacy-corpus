from pathlib import Path
import re

OUT = Path('outputs/khane_to/review/md')
REF = Path('متن ها/khane-to')
REPORT = Path('reports/khane_to_reference_marker_audit.md')

MARKERS = {
  1: ['بازنشستگی','تصمیم‌گیری مالی','ورزش همگانی','قاضی اگر کفش'],
  2: ['سوءتدبیر','قهوه لاته','سوره اسراء','بودجه‌بندی'],
  3: ['صد کیلو','دو بار اندازه','۳۶ درصد','فلسفه'],
  4: ['سوره نمل','کم‌رنگ‌ترین جوهر','کسب‌وکار محلی','سه ماه','شش ماه','عصبانی'],
  5: ['بیست‌وپنج میلیون','سفر تفریحی','پنج درصد','پانزده درصد','هرس'],
  6: ['مکمل','صبحانه','ناهار','شام','هفت‌هزار','پنج‌هزار','رودکی','چهار پرسش'],
  7: ['رزومه','کفش','مولانا','از کار، کار زاید','کار داوطلبانه'],
  8: ['نانوایی','نود دقیقه','آزادی‌بخش','شأن اجتماعی','اثرگذاری'],
  9: ['بیل گیتس','مأمورم و معذور','گرافیست','کارشناس حقوقی','امنیت شغلی'],
 10: ['ارز تقلبی','صندوق امانات','عرضه اولیه','انبار ساختمان','نقدشوندگی'],
 11: ['لوازم خانگی','باغ خودمه','شفافیت','صورت‌های مالی','ریسک‌پذیری'],
 12: ['کاغذی','تلفنی','ارزش ذاتی','۹۷ درصد','سجام','تحلیل بنیادی'],
 13: ['بیمه اجباری','فرانشیز','پرسش‌نامه','حد منفعت','حق بیمه','حد ضرر'],
}

def norm(s):
    return (s.replace('ي','ی').replace('ك','ک').replace('\u200c',' ').replace('ۀ','ه').replace('ة','ه').lower())

def find_context(text, marker):
    ntext, nm = norm(text), norm(marker)
    idx = ntext.find(nm)
    if idx < 0:
        return None
    # map approximately by same character positions after mostly length-preserving normalization
    a=max(0, idx-120); b=min(len(text), idx+len(marker)+180)
    return re.sub(r'\s+',' ',text[a:b]).strip()

lines=['# ممیزی نشانگرهای خاص مرجع — خانه تو','',
       'هدف: تشخیص جزئیات مشخصی که در متن مرجع وجود دارند اما ممکن است از Output مادر افتاده باشند. نبودن یک نشانگر به‌تنهایی مجوز ادغام خودکار نیست.','']
for ep, markers in MARKERS.items():
    o=(OUT/f'{ep}.md').read_text(encoding='utf-8')
    r=(REF/f'episode-{ep:02d}.md').read_text(encoding='utf-8')
    lines += [f'## قسمت {ep:02d}','', '| نشانگر | در مرجع | در Output |', '|---|---:|---:|']
    for m in markers:
        inr = norm(m) in norm(r)
        ino = norm(m) in norm(o)
        lines.append(f'| `{m}` | {"✅" if inr else "—"} | {"✅" if ino else "❌"} |')
        if inr and not ino:
            ctx=find_context(r,m)
            lines += ['', f'- **کاندید غایب `{m}`**: {ctx}', '']
    lines.append('')
REPORT.parent.mkdir(exist_ok=True)
REPORT.write_text('\n'.join(lines),encoding='utf-8')

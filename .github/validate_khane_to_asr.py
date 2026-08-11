from pathlib import Path
import subprocess,re
ROOT=Path('.')
OUT=ROOT/'outputs/khane_to/review/md'
REPORT=ROOT/'reports/khane_to_asr_validation.md'
BASE='197d286f7d793266c9e1bb8a4ca3549be76ce2ec'
patterns=['ازترار','استرار','استرالی','اسطلاح','زخیره','پجوهش','تقوییت','اقصات','قرد','قرز','کارگوزار','کارگذاری','سهان','صحام','سحام','نقض شوند','نقضشوند','روشت','اردش','دوشف','دیویس','کخصالیس','سرموغش','خونقاتو','قواز','دوشبار','انترنت','احساب','تلاتم','مذیعت','معلفه','تعییم','کارافرین','جبرام','آتشتوزی','سالست','فنجن','دخملینش','دواز تا','تاین حد','هزینهٔادگیری','سلام ارز می‌کنم','سلام ازم کنم','بازنشد','روانندگی','راندگی']
lines=['# اعتبارسنجی نهایی پاک‌سازی ASR خانه تو','']
ok=True
lines.append('## ثبات ساختار خطی')
for ep in range(1,14):
    p=f'outputs/khane_to/review/md/{ep}.md'
    cur=(ROOT/p).read_text(encoding='utf-8')
    base=subprocess.check_output(['git','show',f'{BASE}:{p}']).decode('utf-8')
    a,b=len(base.splitlines()),len(cur.splitlines())
    same=a==b; ok &= same
    lines.append(f'- {ep}: baseline={a}, cleaned={b} — {"PASS" if same else "FAIL"}')
lines.append('')
lines.append('## ریشه‌های خراب شناخته‌شده')
hits=[]
for ep in range(1,14):
    text=(OUT/f'{ep}.md').read_text(encoding='utf-8')
    for pat in patterns:
        for m in re.finditer(re.escape(pat),text,re.I):
            ln=text.count('\n',0,m.start())+1
            hits.append((ep,ln,pat,text.splitlines()[ln-1].strip()))
if hits:
    for ep,ln,pat,line in hits: lines.append(f'- {ep}:L{ln} `{pat}` — {line}')
else: lines.append('- **PASS: هیچ موردی پیدا نشد.**')
lines.append('')
lines.append('## [نامفهوم]‌های باقی‌مانده (اطلاعاتی)')
for ep in range(1,14): lines.append(f'- {ep}: {(OUT/f"{ep}.md").read_text(encoding="utf-8").count("[نامفهوم]")}')
lines += ['',f'## نتیجه ساختاری: {"PASS" if ok else "FAIL"}',f'## تعداد ریشه‌های خراب باقی‌مانده: {len(hits)}']
REPORT.write_text('\n'.join(lines),encoding='utf-8')
print('structural',ok,'known_hits',len(hits))

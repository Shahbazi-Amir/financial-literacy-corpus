from pathlib import Path
import subprocess,re,json
ROOT=Path('.')
OUT=ROOT/'outputs/khane_to/review/md'
REPORT=ROOT/'reports/khane_to_asr_validation.md'
# obvious corrupt roots/tokens that should not survive unless quoted in report
patterns=[
'ازترار','استرار','استرالی','اسطلاح','زخیره','پجوهش','تقوییت','اقصات','قرد','قرز','کارگوزار','کارگذاری','سهان','صحام','سحام','نقض شوند','نقضشوند','روشت','اردش','دوشف','دیویس','کخصالیس','سرموغش','خونقاتو','قواز','دوشبار','انترنت','احساب','تلاتم','مذیعت','معلفه','تعییم','کارافرین','جبرام','آتشتوزی','سالست','فنجن','دخملینش','دواز تا','تاین حد','هزینهٔادگیری'
]
lines=['# اعتبارسنجی نهایی پاک‌سازی ASR خانه تو','']
# line-count invariance vs main baseline
ok=True
lines.append('## ثبات ساختار خطی')
for ep in range(1,14):
    p=f'outputs/khane_to/review/md/{ep}.md'
    cur=(ROOT/p).read_text(encoding='utf-8')
    base=subprocess.check_output(['git','show',f'origin/main:{p}']).decode('utf-8')
    lc_cur=len(cur.splitlines()); lc_base=len(base.splitlines())
    same=lc_cur==lc_base
    ok &= same
    lines.append(f'- {ep}: baseline={lc_base}, cleaned={lc_cur} — {"PASS" if same else "FAIL"}')
lines.append('')
# known bad stems
lines.append('## جست‌وجوی ریشه‌های خراب شناخته‌شده')
hits=[]
for ep in range(1,14):
    text=(OUT/f'{ep}.md').read_text(encoding='utf-8')
    for pat in patterns:
        for m in re.finditer(re.escape(pat),text,re.I):
            ln=text.count('\n',0,m.start())+1
            line=text.splitlines()[ln-1].strip()
            hits.append((ep,ln,pat,line))
if hits:
    for ep,ln,pat,line in hits: lines.append(f'- {ep}:L{ln} `{pat}` — {line}')
else:
    lines.append('- **PASS: موردی پیدا نشد.**')
lines.append('')
# unresolved markers: informational, not failure
lines.append('## [نامفهوم]‌های باقی‌مانده')
for ep in range(1,14):
    text=(OUT/f'{ep}.md').read_text(encoding='utf-8')
    c=text.count('[نامفهوم]')
    lines.append(f'- {ep}: {c}')
lines.append('')
lines.append(f'## نتیجه ساختاری: {"PASS" if ok else "FAIL"}')
REPORT.write_text('\n'.join(lines),encoding='utf-8')
print('structural',ok,'known_hits',len(hits))

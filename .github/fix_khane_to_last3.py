from pathlib import Path
root=Path('outputs/khane_to/review/md')
fixes={6:{'سلام ارز می‌کنم':'سلام عرض می‌کنم'},13:{'سلام ارز می‌کنم':'سلام عرض می‌کنم','دیویس':'دویست'}}
for ep,mp in fixes.items():
    p=root/f'{ep}.md'; t=p.read_text(encoding='utf-8')
    for a,b in mp.items(): t=t.replace(a,b)
    p.write_text(t,encoding='utf-8')
r=Path('reports/khane_to_asr_cleanup_applied.md')
t=r.read_text(encoding='utf-8').rstrip()+"\n\n---\n\n# اصلاح سه مورد باقی‌مانده\n\n- قسمت 6: `سلام ارز می‌کنم` → `سلام عرض می‌کنم`\n- قسمت 13: `سلام ارز می‌کنم` → `سلام عرض می‌کنم`\n- قسمت 13: `دیویس` → `دویست`\n"
r.write_text(t,encoding='utf-8')

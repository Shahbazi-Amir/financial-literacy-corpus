from pathlib import Path
import re
p=Path('outputs/uni_tehran/uni_tehran_episode_4_final/review/4.md')
s=p.read_text(encoding='utf-8')
patterns=[
'نامفهوم','پجوهش','محارت','ثواد','حوضه','افضایش','توصیح','بازدشت','قرفه','عدب','تادیه','جرعت','اتمینان','پیشتبستانی','اردیابی','نیاستنجی','ترراحی','کارگذاری','دوچار','بهرمند','گزارش هایی به تادیه','استانداردیه که داره خودش','مستند ساخته شده آمریکا','ناحیه اتحادیه اروپا','موضوع در اختیار دانشجوها داره','استاندارد پویاییه'
]
lines=['# Uni Tehran ep4 ASR sanity scan','']
for pat in patterns:
    n=s.count(pat)
    if n:
        lines.append(f'- `{pat}`: {n}')
# collect sentences containing ellipses or obvious repeated filler around punctuation
lines += ['', '## ellipsis contexts','']
for m in re.finditer(r'\.\.\.',s):
    a=max(0,m.start()-120); b=min(len(s),m.end()+160)
    lines.append('`'+re.sub(r'\s+',' ',s[a:b]).replace('`','')+'`')
Path('reports/uni_tehran_ep4_asr_sanity.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print('done')
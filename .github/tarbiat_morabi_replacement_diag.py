from pathlib import Path
checks={
3:['لخت شستن'],
4:['گفت ما فاتم مذا و ما سیعتی کفعن قوم فقتن ملفورست و بین الادمن'],
5:['یعنی همیت محبه است بر قصد تعلق محبوب از غیر و غیر از محبوب'],
9:['به سرمویی پسرخاله‌ای یا دوستی'],
11:['بابا این فرض کن بندازه یه دو هفته پول توجیبی‌ت‌ها','ممنونم از اتا'],
12:['دختر گلم، به سر گلم، گلم','در اصطلاح می‌گن گیونه','نگاه اعتراضی و نگاه شکرانه','مثلا فرض به ماهی ۵۰۰ هزار تومن','چه بدونم لس‌آنجلس'],
14:['یک، مشهوده.\n\nدو، از ارائه‌دهنده جدا نمی‌شه.'],
}
lines=['# Tarbiat Morabi replacement diagnostics','']
for i,olds in checks.items():
    text=Path(f'outputs/tarbiat_morabi/review/md/{i}.md').read_text(encoding='utf-8')
    lines.append(f'## {i}')
    for s in olds:
        lines.append(f'- count={text.count(s)} :: `{s}`')
    lines.append('')
Path('reports/tarbiat_morabi_replacement_diagnostics.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')

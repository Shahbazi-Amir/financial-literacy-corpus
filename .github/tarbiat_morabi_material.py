from pathlib import Path
from difflib import SequenceMatcher
import re
OUT=Path('outputs/tarbiat_morabi/review/md'); REF=Path('متن ها/tarbiat_morabi/md')
REP=Path('reports/tarbiat_morabi_material_candidates.md')
wr=re.compile(r'[\w\u200c]+',re.UNICODE); nr=re.compile(r'^[۰-۹0-9]+$')
def w(path):
    lines=[]
    for ln in path.read_text(encoding='utf-8').splitlines():
        s=ln.strip()
        if s.startswith('#') or s.startswith('>'): continue
        lines.append(ln)
    return wr.findall('\n'.join(lines).replace('ي','ی').replace('ك','ک'))
def cx(t,a,b,n=8): return ' '.join(t[max(0,a-n):min(len(t),b+n)])
L=['# اختلاف‌های مادی تربیت مربی','', 'فقط حذف/افزودن، اختلاف طولی، و اختلاف عددی؛ برای تصمیم انسانی.','']
for i in range(1,15):
    ow,rw=w(OUT/f'{i}.md'),w(REF/f'{i}.md')
    xs=[]
    for tag,a1,a2,b1,b2 in SequenceMatcher(None,ow,rw,autojunk=False).get_opcodes():
        if tag=='equal': continue
        os,rs=ow[a1:a2],rw[b1:b2]
        numsO=[x for x in os if nr.match(x)]; numsR=[x for x in rs if nr.match(x)]
        keep=(tag in ('insert','delete') and max(len(os),len(rs))>=2) or (tag=='replace' and abs(len(os)-len(rs))>=2) or (numsO!=numsR and (numsO or numsR))
        if keep: xs.append((tag,a1,a2,b1,b2,os,rs,numsO,numsR))
    L += [f'## قسمت {i} — {len(xs)} مورد','']
    for j,(tag,a1,a2,b1,b2,os,rs,no,nr_) in enumerate(xs,1):
        L += [f'### {i}.{j} — {tag} — O:{len(os)} R:{len(rs)}', f'- O: `{" ".join(os)}`', f'- R: `{" ".join(rs)}`', f'- Context O: `{cx(ow,a1,a2)}`', f'- Context R: `{cx(rw,b1,b2)}`']
        if no or nr_: L += [f'- Numbers: O={no} / R={nr_}']
        L += ['']
REP.write_text('\n'.join(L)+'\n',encoding='utf-8')

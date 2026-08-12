from pathlib import Path
from difflib import SequenceMatcher
import re
OUT=Path('outputs/tarbiat_morabi/review/md'); REF=Path('متن ها/tarbiat_morabi/md'); REP=Path('reports/tarbiat_morabi_gap_candidates.md')
wr=re.compile(r'[\w\u200c]+',re.UNICODE)
def t(p):
    ls=[]
    for ln in p.read_text(encoding='utf-8').splitlines():
        s=ln.strip()
        if s.startswith('#') or s.startswith('>'): continue
        ls.append(ln)
    return wr.findall('\n'.join(ls).replace('ي','ی').replace('ك','ک'))
def cx(x,a,b,n=12): return ' '.join(x[max(0,a-n):min(len(x),b+n)])
L=['# افتادگی‌های احتمالی تربیت مربی','', 'فقط Insert/Delete دو واژه‌ای به بالا؛ یعنی محتمل‌ترین افتادگی واقعی.','']
for i in range(1,15):
    ow,rw=t(OUT/f'{i}.md'),t(REF/f'{i}.md'); xs=[]
    for tag,a1,a2,b1,b2 in SequenceMatcher(None,ow,rw,autojunk=False).get_opcodes():
        if tag not in ('insert','delete'): continue
        os,rs=ow[a1:a2],rw[b1:b2]
        if max(len(os),len(rs))<2: continue
        if 'زبان تشخیص' in ' '.join(os+rs): continue
        xs.append((tag,a1,a2,b1,b2,os,rs))
    L += [f'## قسمت {i} — {len(xs)} مورد','']
    for j,(tag,a1,a2,b1,b2,os,rs) in enumerate(xs,1):
        L += [f'### {i}.{j} — {tag}', f'- Output-only: `{" ".join(os)}`', f'- Ref-only: `{" ".join(rs)}`', f'- O-context: `{cx(ow,a1,a2)}`', f'- R-context: `{cx(rw,b1,b2)}`','']
REP.write_text('\n'.join(L)+'\n',encoding='utf-8')

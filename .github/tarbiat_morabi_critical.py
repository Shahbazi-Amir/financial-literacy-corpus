from pathlib import Path
from difflib import SequenceMatcher
import re
OUT=Path('outputs/tarbiat_morabi/review/md'); REF=Path('متن ها/tarbiat_morabi/md'); REP=Path('reports/tarbiat_morabi_critical_candidates.md')
wr=re.compile(r'[\w\u200c]+',re.UNICODE); nr=re.compile(r'^[۰-۹0-9]+$'); tr=str.maketrans('۰۱۲۳۴۵۶۷۸۹','0123456789')
def toks(p):
    ls=[]
    for ln in p.read_text(encoding='utf-8').splitlines():
        s=ln.strip()
        if s.startswith('#') or s.startswith('>'): continue
        ls.append(ln)
    return wr.findall('\n'.join(ls).replace('ي','ی').replace('ك','ک'))
def norm(s): return re.sub(r'[^\w]','',s.translate(tr).replace('\u200c','').replace(' ',''))
def nums(xs): return [x.translate(tr) for x in xs if nr.match(x)]
def cx(t,a,b,n=10): return ' '.join(t[max(0,a-n):min(len(t),b+n)])
L=['# کاندیدهای بحرانی تربیت مربی','', 'فقط اختلاف‌هایی که احتمال اثر محتوایی دارند.','']
for i in range(1,15):
    ow,rw=toks(OUT/f'{i}.md'),toks(REF/f'{i}.md'); xs=[]
    for tag,a1,a2,b1,b2 in SequenceMatcher(None,ow,rw,autojunk=False).get_opcodes():
        if tag=='equal': continue
        os,rs=ow[a1:a2],rw[b1:b2]; joined=' '.join(os+rs)
        if 'زبان تشخیص' in joined: continue
        no,nrr=norm(' '.join(os)),norm(' '.join(rs)); sim=SequenceMatcher(None,no,nrr,autojunk=False).ratio() if (no or nrr) else 1
        nO,nR=nums(os),nums(rs)
        real_num=(nO!=nR and (nO or nR))
        critical=(tag in ('insert','delete') and max(len(os),len(rs))>=2) or sim<0.35 or real_num
        if critical: xs.append((tag,a1,a2,b1,b2,os,rs,sim,nO,nR))
    L += [f'## قسمت {i} — {len(xs)} مورد','']
    for j,(tag,a1,a2,b1,b2,os,rs,sim,nO,nR) in enumerate(xs,1):
        L += [f'### {i}.{j} — {tag} — sim {sim:.2f}', f'- Output: `{" ".join(os)}`', f'- Ref: `{" ".join(rs)}`', f'- O-context: `{cx(ow,a1,a2)}`', f'- R-context: `{cx(rw,b1,b2)}`']
        if nO or nR: L += [f'- Numbers normalized: O={nO} / R={nR}']
        L += ['']
REP.write_text('\n'.join(L)+'\n',encoding='utf-8')

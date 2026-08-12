from pathlib import Path
from difflib import SequenceMatcher
import re
OUT=Path('outputs/tarbiat_morabi/review/md'); REF=Path('متن ها/tarbiat_morabi/md'); REP=Path('reports/tarbiat_morabi_semantic_candidates.md')
wr=re.compile(r'[\w\u200c]+',re.UNICODE)
trans=str.maketrans('۰۱۲۳۴۵۶۷۸۹','0123456789')
def toks(p):
    ls=[]
    for ln in p.read_text(encoding='utf-8').splitlines():
        s=ln.strip()
        if s.startswith('#') or s.startswith('>'): continue
        ls.append(ln)
    return wr.findall('\n'.join(ls).replace('ي','ی').replace('ك','ک'))
def norm(s):
    s=s.translate(trans).replace('\u200c','').replace(' ','')
    return re.sub(r'[^\w]','',s)
def cx(t,a,b,n=8): return ' '.join(t[max(0,a-n):min(len(t),b+n)])
L=['# کاندیدهای معنایی تربیت مربی','', 'اختلافات ظاهری/رقمی/متادیتای ASR حذف شده‌اند؛ فقط مواردی که احتمال تغییر معنا یا افتادگی دارند.','']
for i in range(1,15):
    ow,rw=toks(OUT/f'{i}.md'),toks(REF/f'{i}.md'); xs=[]
    for tag,a1,a2,b1,b2 in SequenceMatcher(None,ow,rw,autojunk=False).get_opcodes():
        if tag=='equal': continue
        os,rs=ow[a1:a2],rw[b1:b2]
        joined=' '.join(os+rs)
        if 'زبان تشخیص' in joined: continue
        no,nr=norm(' '.join(os)),norm(' '.join(rs))
        if no==nr: continue
        sim=SequenceMatcher(None,no,nr,autojunk=False).ratio() if (no or nr) else 1
        # Keep likely semantic differences: insertion/deletion >=2, meaningful length gap, or low textual similarity.
        if (tag in ('insert','delete') and max(len(os),len(rs))>=2) or abs(len(os)-len(rs))>=2 or sim<0.58:
            xs.append((tag,a1,a2,b1,b2,os,rs,sim))
    L += [f'## قسمت {i} — {len(xs)} کاندید','']
    for j,(tag,a1,a2,b1,b2,os,rs,sim) in enumerate(xs,1):
        L += [f'### {i}.{j} — {tag} — similarity {sim:.2f}', f'- Output: `{" ".join(os)}`', f'- Ref: `{" ".join(rs)}`', f'- O-context: `{cx(ow,a1,a2)}`', f'- R-context: `{cx(rw,b1,b2)}`','']
REP.write_text('\n'.join(L)+'\n',encoding='utf-8')

from pathlib import Path
from difflib import SequenceMatcher
import re

OUT=Path('outputs/tarbiat_morabi/review/md')
REF=Path('متن ها/tarbiat_morabi/md')
REP=Path('reports/tarbiat_morabi_precision_candidates.md')
word_re=re.compile(r'[\w\u200c]+', re.UNICODE)
num_re=re.compile(r'^[۰-۹0-9]+$')

def body(s):
    lines=s.splitlines()
    kept=[]
    for ln in lines:
        st=ln.strip()
        if st.startswith('#') or st.startswith('>'):
            continue
        kept.append(ln)
    return '\n'.join(kept)

def words(s):
    return word_re.findall(body(s).replace('ي','ی').replace('ك','ک'))

def cxt(t,a,b,n=7):
    return ' '.join(t[max(0,a-n):min(len(t),b+n)])

lines=['# کاندیدهای دقیق تربیت مربی','',
       'فقط اختلاف‌های کوتاه/عددی/نامی برای بازخوانی انسانی. هیچ اصلاح خودکاری مجاز نیست.','']
for i in range(1,15):
    otext=(OUT/f'{i}.md').read_text(encoding='utf-8')
    rtext=(REF/f'{i}.md').read_text(encoding='utf-8')
    ow,rw=words(otext),words(rtext)
    sm=SequenceMatcher(None,ow,rw,autojunk=False)
    cand=[]
    allops=0
    for tag,a1,a2,b1,b2 in sm.get_opcodes():
        if tag=='equal': continue
        allops+=1
        os,rs=ow[a1:a2],rw[b1:b2]
        hasnum=any(num_re.match(x) for x in os+rs)
        material=False
        if tag in ('insert','delete') and max(len(os),len(rs))>=2:
            material=True
        elif tag=='replace' and (abs(len(os)-len(rs))>=2 or hasnum):
            material=True
        elif tag=='replace' and max(len(os),len(rs))<=4:
            # small substitutions often capture ASR/proper-term corrections
            material=True
        if material:
            cand.append((tag,a1,a2,b1,b2,os,rs,hasnum))
    lines += [f'## قسمت {i} — {len(cand)} کاندید از {allops} اختلاف','']
    for n,(tag,a1,a2,b1,b2,os,rs,hasnum) in enumerate(cand,1):
        lines += [f'### {i}.{n} — {tag} — O:{len(os)} R:{len(rs)}' + (' — عددی' if hasnum else ''),
                  f'- O: `{" ".join(os)}`',
                  f'- R: `{" ".join(rs)}`',
                  f'- O-context: `{cxt(ow,a1,a2)}`',
                  f'- R-context: `{cxt(rw,b1,b2)}`','']
REP.write_text('\n'.join(lines)+'\n',encoding='utf-8')

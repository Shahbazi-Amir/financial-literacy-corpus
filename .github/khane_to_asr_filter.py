from pathlib import Path
import re, difflib, unicodedata
from wordfreq import zipf_frequency

ROOT=Path('.')
OUT=ROOT/'outputs/khane_to/review/md'
REF=ROOT/'متن ها/khane-to'
REPORT=ROOT/'reports/khane_to_asr_strict_candidates.md'
word_re=re.compile(r"[\u0600-\u06FF\u200c]+|[A-Za-z0-9]+")

def norm(s):
    return unicodedata.normalize('NFKC',s).replace('ي','ی').replace('ك','ک').replace('\u200c','').lower()
def toks(t): return word_re.findall(t)
def lev(a,b):
    a,b=norm(a),norm(b); m,n=len(a),len(b); dp=list(range(n+1))
    for i,ca in enumerate(a,1):
        nd=[i]+[0]*n
        for j,cb in enumerate(b,1): nd[j]=min(dp[j]+1,nd[j-1]+1,dp[j-1]+(ca!=cb))
        dp=nd
    return dp[n]

def freq(s):
    w=norm(s).replace(' ','')
    return zipf_frequency(w,'fa') if w else 0

# preserve colloquial/style variants intentionally
style_markers=[
 ('تون','تان'),('مون','مان'),('شون','شان'),('میشه','میشود'),('میشه','می‌شود'),
 ('میتون','میتوان'),('میخوام','میخواهم'),('میخوایم','میخواهیم'),('میگم','میگویم'),
 ('میگن','میگویند'),('میاد','میآید'),('رو','را'),('یه','یک'),('اگه','اگر'),('واسه','برای'),
 ('همون','همان'),('اینه','این است'),('لازمه','لازم است'),('خرابه','خراب است')]
def style_only(a,b):
    x,y=norm(a),norm(b)
    if any((p in x and q in y) or (q in x and p in y) for p,q in style_markers): return True
    if x.rstrip('،؛؟')==y.rstrip('،؛؟'): return True
    return False

lines=['# کاندیدهای سخت‌گیرانه اصلاح ASR — خانه تو','',
'> فقط مواردی آمده‌اند که شکل Output از نظر بسامد زبانی به‌وضوح مشکوک‌تر از شکل مرجع است. هنوز هیچ Outputی تغییر نکرده.','']
for ep in range(1,14):
    ot=toks((OUT/f'{ep}.md').read_text(encoding='utf-8'))
    rt=toks((REF/f'episode-{ep:02d}.md').read_text(encoding='utf-8'))
    on=[norm(x) for x in ot]; rn=[norm(x) for x in rt]
    sm=difflib.SequenceMatcher(None,on,rn,autojunk=False)
    cs=[]
    for tag,i1,i2,j1,j2 in sm.get_opcodes():
        if tag!='replace': continue
        A=ot[i1:i2]; B=rt[j1:j2]
        if not A or not B or len(A)>2 or len(B)>2: continue
        sa=' '.join(A); sb=' '.join(B)
        if style_only(sa,sb): continue
        d=lev(''.join(A),''.join(B)); L=max(len(norm(''.join(A))),len(norm(''.join(B))))
        if d>3 or (L<5 and d>1): continue
        fa,fb=freq(sa),freq(sb)
        # strong language evidence: target clearly more natural; allow known technical English/Latin target
        if not (fb>=3.1 and (fb-fa)>=0.85): continue
        before=' '.join(ot[max(0,i1-5):i1]); after=' '.join(ot[i2:i2+5])
        cs.append((sa,sb,d,fa,fb,before,after))
    # dedupe
    seen=set(); u=[]
    for c in cs:
        k=(norm(c[0]),norm(c[1]))
        if k not in seen: seen.add(k); u.append(c)
    lines += [f'## قسمت {ep}',f'- کاندید سخت‌گیرانه: **{len(u)}**','']
    for a,b,d,fa,fb,bef,aft in u:
        lines.append(f'- `{a}` → `{b}` | edit={d} | freq {fa:.2f}→{fb:.2f} — … {bef} **[{a}]** {aft} …')
    lines.append('')
REPORT.parent.mkdir(parents=True,exist_ok=True)
REPORT.write_text('\n'.join(lines),encoding='utf-8')
print(REPORT)

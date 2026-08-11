from pathlib import Path
import re, difflib, unicodedata

ROOT=Path('.')
OUT=ROOT/'outputs/khane_to/review/md'
REF=ROOT/'متن ها/khane-to'
REPORT=ROOT/'reports/khane_to_asr_candidates.md'

word_re=re.compile(r"[\u0600-\u06FF\u200c]+|[A-Za-z0-9]+")

def norm(s):
    s=unicodedata.normalize('NFKC',s).replace('ي','ی').replace('ك','ک').replace('\u200c','')
    return s.lower()

def toks(text):
    return word_re.findall(text)

def lev(a,b):
    a,b=norm(a),norm(b)
    m,n=len(a),len(b)
    dp=list(range(n+1))
    for i,ca in enumerate(a,1):
        nd=[i]+[0]*n
        for j,cb in enumerate(b,1):
            nd[j]=min(dp[j]+1, nd[j-1]+1, dp[j-1]+(ca!=cb))
        dp=nd
    return dp[n]

# reject obvious style-only modernizations
STYLE_PREFIXES=('می','نمی')
STYLE_PAIRS={('میخوام','میخواهم'),('میگم','میگویم'),('میشه','میشود'),('میاد','میآید'),('میریم','میرویم'),('میذاره','میگذارد'),('میذاریم','میگذاریم'),('میخوایم','میخواهیم'),('رو','را'),('یه','یک'),('اگه','اگر'),('واسه','برای')}

def style_only(a,b):
    x,y=norm(a),norm(b)
    return (x,y) in STYLE_PAIRS or (y,x) in STYLE_PAIRS

lines=['# کاندیدهای اصلاح ASR — خانه تو','',
       '> این گزارش فقط کاندید است و هیچ Outputی را تغییر نمی‌دهد. مرجع دوم فقط برای یافتن خطاهای محتمل استفاده شده است.','']

for ep in range(1,14):
    op=OUT/f'{ep}.md'; rp=REF/f'episode-{ep:02d}.md'
    ot=toks(op.read_text(encoding='utf-8')); rt=toks(rp.read_text(encoding='utf-8'))
    on=[norm(x) for x in ot]; rn=[norm(x) for x in rt]
    sm=difflib.SequenceMatcher(None,on,rn,autojunk=False)
    cands=[]
    for tag,i1,i2,j1,j2 in sm.get_opcodes():
        if tag!='replace': continue
        A=ot[i1:i2]; B=rt[j1:j2]
        # only tiny local substitutions
        if len(A)>2 or len(B)>2 or not A or not B: continue
        sa=' '.join(A); sb=' '.join(B)
        ca=''.join(A); cb=''.join(B)
        d=lev(ca,cb)
        L=max(len(norm(ca)),len(norm(cb)))
        if style_only(sa,sb): continue
        if d <= (1 if L<=4 else 2) or (L>=6 and d<=3):
            before=' '.join(ot[max(0,i1-4):i1])
            after=' '.join(ot[i2:i2+4])
            cands.append((sa,sb,d,before,after))
    # dedupe preserving order
    seen=set(); uniq=[]
    for c in cands:
        key=(norm(c[0]),norm(c[1]))
        if key in seen: continue
        seen.add(key); uniq.append(c)
    lines += [f'## قسمت {ep}',f'- تعداد کاندید محافظه‌کار: **{len(uniq)}**','']
    for a,b,d,bef,aft in uniq:
        lines.append(f'- `{a}` → `{b}` (فاصله={d}) — … {bef} **[{a}]** {aft} …')
    lines.append('')

REPORT.parent.mkdir(parents=True,exist_ok=True)
REPORT.write_text('\n'.join(lines),encoding='utf-8')
print(REPORT)

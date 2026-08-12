from pathlib import Path
import re, difflib

OUT=Path('outputs/mq/review/md')
REF=Path('متن ها/mq/md')
REPORT=Path('reports/mq_merge_candidates.md')

def norm(s):
    s=s.replace('ي','ی').replace('ك','ک').replace('\u200c',' ')
    s=re.sub(r'[^\w\sآ-ی۰-۹]',' ',s)
    return re.sub(r'\s+',' ',s).strip().lower()

def words(s): return re.findall(r'[آ-یA-Za-z0-9۰-۹_]+',norm(s))

def clean_ref_header(ws):
    marker=['بسم','الله','الرحمن','الرحیم']
    for i in range(max(0,len(ws)-4)):
        if ws[i:i+4]==marker:
            return ws[i:]
    return ws

def spans(o,r):
    ow=words(o); rw=clean_ref_header(words(r))
    sm=difflib.SequenceMatcher(None,ow,rw,autojunk=False)
    ops=sm.get_opcodes()
    raw=[]
    for idx,(tag,i1,i2,j1,j2) in enumerate(ops):
        if tag=='equal': continue
        olen=i2-i1; rlen=j2-j1
        # keep only where ref contains materially more content OR a long replacement likely compressed by output
        if rlen-olen>=4 or (tag=='insert' and rlen>=4) or (tag=='replace' and rlen>=12 and rlen>=olen):
            raw.append([idx,tag,i1,i2,j1,j2])
    # merge neighboring candidate opcodes if separated by <= 6 equal tokens, preventing overlapping noisy fragments
    merged=[]
    for item in raw:
        if not merged:
            merged.append(item); continue
        p=merged[-1]
        # inspect op index gap and raw token gap
        if item[0]-p[0] <= 2 and item[4]-p[5] <= 6:
            p[0]=item[0]; p[1]='merged'; p[2]=min(p[2],item[2]); p[3]=max(p[3],item[3]); p[4]=min(p[4],item[4]); p[5]=max(p[5],item[5])
        else:
            merged.append(item)
    out=[]
    for _,tag,i1,i2,j1,j2 in merged:
        reftext=' '.join(rw[j1:j2]); outtext=' '.join(ow[i1:i2])
        if len(rw[j1:j2])<4: continue
        left=' '.join(rw[max(0,j1-12):j1]); right=' '.join(rw[j2:min(len(rw),j2+12)])
        outleft=' '.join(ow[max(0,i1-12):i1]); outright=' '.join(ow[i2:min(len(ow),i2+12)])
        out.append((tag,len(rw[j1:j2]),len(ow[i1:i2]),left,reftext,right,outleft,outtext,outright))
    return out

lines=['# کاندیدهای مستقل ادغام MQ','',
'این گزارش بازه‌های مستقل Ref را که در Output حذف/فشرده شده‌اند نشان می‌دهد. فقط برای بازخوانی انسانی است؛ هیچ ادغام خودکاری مجاز نیست.','']
for n in range(1,9):
    o=(OUT/f'{n}.md').read_text(encoding='utf-8'); r=(REF/f'{n}.md').read_text(encoding='utf-8')
    ss=spans(o,r)
    lines += [f'## قسمت {n} — {len(ss)} بازه مستقل','']
    if not ss:
        lines += ['- موردی ندارد.','']; continue
    for k,(tag,rl,ol,l,rt,rgt,olft,ot,orgt) in enumerate(ss,1):
        lines += [f'### {n}.{k} — {tag} — Ref {rl} واژه / Output {ol} واژه',
                  f'- قبل در Ref: `{l}`',f'- **بازه Ref:** `{rt}`',f'- بعد در Ref: `{rgt}`',
                  f'- قبل در Output: `{olft}`',f'- **بازه Output:** `{ot}`',f'- بعد در Output: `{orgt}`','']
REPORT.parent.mkdir(exist_ok=True)
REPORT.write_text('\n'.join(lines),encoding='utf-8')
print('written',REPORT)

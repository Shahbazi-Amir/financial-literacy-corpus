from pathlib import Path
import re, difflib, hashlib

paths = {
    'old_output': Path('outputs/uni_tehran/review/md/4.md'),
    'new_video_review': Path('outputs/uni_tehran/uni_tehran_episode_4_final/review/4.md'),
    'reference': Path('متن ها/uni_tehran/md/4.md'),
    'current_final': Path('final/uni-tehran/episode-04.md'),
}
texts={k:p.read_text(encoding='utf-8') for k,p in paths.items()}

def clean(s):
    s=re.sub(r'^#.*$', ' ', s, flags=re.M)
    s=s.replace('**استاد**',' ').replace('**مجری**',' ')
    s=re.sub(r'\s+',' ',s)
    return s.strip()

def norm_word(w):
    w=w.translate(str.maketrans('۰۱۲۳۴۵۶۷۸۹','0123456789'))
    w=w.replace('ي','ی').replace('ك','ک').replace('\u200c','')
    return re.sub(r'[^0-9A-Za-zآ-ی]+','',w).lower()

def toks(s): return [norm_word(x) for x in clean(s).split() if norm_word(x)]
def sha(s): return hashlib.sha256(s.encode()).hexdigest()
def ratio(a,b): return difflib.SequenceMatcher(None,toks(a),toks(b),autojunk=False).ratio()

def gaps(src, dst, min_words=5, limit=50):
    a=toks(src); b=toks(dst)
    sm=difflib.SequenceMatcher(None,a,b,autojunk=False)
    out=[]
    for tag,i1,i2,j1,j2 in sm.get_opcodes():
        if tag in ('delete','replace') and i2-i1>=min_words:
            seq=' '.join(a[i1:i2]); ctx=' '.join(a[max(0,i1-12):min(len(a),i2+12)])
            out.append((i2-i1,tag,seq,ctx))
    out.sort(reverse=True,key=lambda x:x[0])
    return out[:limit]

def add_gap_section(lines,title,a,b,min_words=5,limit=50):
    lines += [f'## {title}','']
    gs=gaps(texts[a],texts[b],min_words,limit)
    if not gs: lines.append('- هیچ موردی')
    for n,tag,seq,ctx in gs:
        lines += [f'### {n} واژه — {tag}',f'`{seq}`',f'context: `{ctx}`','']

lines=['# ممیزی سه‌نسخه‌ای دانشگاه تهران — قسمت ۴','']
for k in paths:
    lines += [f'## {k}',f'- path: `{paths[k]}`',f'- bytes: {len(texts[k].encode())}',f'- words(normalized): {len(toks(texts[k]))}',f'- sha256: `{sha(texts[k])}`','']
lines += ['## شباهت‌های واژه‌ای','']
ks=list(paths)
for i in range(len(ks)):
    for j in range(i+1,len(ks)):
        lines.append(f'- {ks[i]} ↔ {ks[j]}: {ratio(texts[ks[i]],texts[ks[j]]):.4f}')
lines.append('')
add_gap_section(lines,'new_video_review → old_output: محتوای جدید/بازیابی‌شده','new_video_review','old_output',5,60)
add_gap_section(lines,'old_output → new_video_review: محتوای احتمالی از دست‌رفته در نسخه جدید','old_output','new_video_review',5,60)
add_gap_section(lines,'current_final → new_video_review: چیزهای Final فعلی که نسخه جدید ندارد','current_final','new_video_review',5,60)
add_gap_section(lines,'new_video_review → current_final: چیزهای جدید که Final فعلی ندارد','new_video_review','current_final',5,60)
add_gap_section(lines,'reference → new_video_review: چیزهای مرجع خام که نسخه جدید ندارد','reference','new_video_review',5,40)

patterns=['نامفهوم','Financial Capability','پرتغال','لهستان','۸۰۰ هزار','هشت میلیون','شورای تبلیغ','کسب‌وکار خرد','حقوق مصرف‌کننده','شمول مالی','ساخت آمریکا','هشتصد هزار','نه میلیون','۵۰ میلیون','۱۰۰ میلیون']
lines += ['## نشانگرهای کلیدی','']
for pat in patterns:
    lines.append(f'- `{pat}`: ' + ', '.join(f'{k}={texts[k].count(pat)}' for k in paths))
Path('reports/uni_tehran_ep4_threeway_audit.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print('wrote extended audit')
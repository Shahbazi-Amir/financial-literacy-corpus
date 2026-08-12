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
    s=s.replace('**استاد**',' ')
    s=re.sub(r'\s+',' ',s)
    return s.strip()

def norm_word(w):
    w=w.translate(str.maketrans('۰۱۲۳۴۵۶۷۸۹','0123456789'))
    w=w.replace('ي','ی').replace('ك','ک').replace('\u200c','')
    return re.sub(r'[^0-9A-Za-zآ-ی]+','',w).lower()

def toks(s):
    return [norm_word(x) for x in clean(s).split() if norm_word(x)]

def sha(s): return hashlib.sha256(s.encode()).hexdigest()

def ratio(a,b): return difflib.SequenceMatcher(None,toks(a),toks(b),autojunk=False).ratio()

def gaps(src, dst, min_words=6, limit=25):
    a=toks(src); b=toks(dst)
    sm=difflib.SequenceMatcher(None,a,b,autojunk=False)
    out=[]
    for tag,i1,i2,j1,j2 in sm.get_opcodes():
        if tag in ('delete','replace') and i2-i1>=min_words:
            seq=' '.join(a[i1:i2])
            left=' '.join(a[max(0,i1-12):min(len(a),i2+12)])
            out.append((i2-i1,tag,seq,left))
    out.sort(reverse=True,key=lambda x:x[0])
    return out[:limit]

lines=['# ممیزی سه‌نسخه‌ای دانشگاه تهران — قسمت ۴','']
for k in paths:
    lines += [f'## {k}',f'- path: `{paths[k]}`',f'- bytes: {len(texts[k].encode())}',f'- words(normalized): {len(toks(texts[k]))}',f'- sha256: `{sha(texts[k])}`','']

lines += ['## شباهت‌های واژه‌ای','']
ks=list(paths)
for i in range(len(ks)):
    for j in range(i+1,len(ks)):
        lines.append(f'- {ks[i]} ↔ {ks[j]}: {ratio(texts[ks[i]],texts[ks[j]]):.4f}')

lines += ['','## بخش‌های موجود در new_video_review که در old_output پیدا نمی‌شوند','']
for n,tag,seq,ctx in gaps(texts['new_video_review'],texts['old_output'],6,40):
    lines += [f'### {n} واژه — {tag}',f'`{seq}`',f'context: `{ctx}`','']

lines += ['## بخش‌های موجود در old_output که در new_video_review پیدا نمی‌شوند','']
for n,tag,seq,ctx in gaps(texts['old_output'],texts['new_video_review'],6,40):
    lines += [f'### {n} واژه — {tag}',f'`{seq}`',f'context: `{ctx}`','']

lines += ['## بخش‌های موجود در reference که در new_video_review پیدا نمی‌شوند','']
for n,tag,seq,ctx in gaps(texts['reference'],texts['new_video_review'],6,30):
    lines += [f'### {n} واژه — {tag}',f'`{seq}`',f'context: `{ctx}`','']

# markers / suspicious tokens
patterns=['نامفهوم','سواد مالی','Financial Capability','پرتغال','لهستان','۸۰۰','800','هشت میلیون','شورای تبلیغ','کسب‌وکار خرد','حقوق مصرف‌کننده','شمول مالی']
lines += ['## نشانگرهای کلیدی','']
for pat in patterns:
    lines.append(f'- `{pat}`: ' + ', '.join(f'{k}={texts[k].count(pat)}' for k in paths))

Path('reports/uni_tehran_ep4_threeway_audit.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print('wrote audit')
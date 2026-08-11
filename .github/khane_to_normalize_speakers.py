from pathlib import Path
import re

ROOT = Path('outputs/khane_to/review/md')
SPEAKER_RE = re.compile(r'^\*\*(فرهاد جم|دکتر کمیل رودی|فرهاد جم / دکتر کمیل رودی|شرکت‌کننده \d+)\*\*$')

def parse_blocks(text):
    lines = text.splitlines()
    prefix = []
    blocks = []
    cur_speaker = None
    cur_body = []
    seen_speaker = False

    def flush():
        nonlocal cur_speaker, cur_body
        if cur_speaker is not None:
            blocks.append([cur_speaker, cur_body[:]])
        cur_speaker = None
        cur_body = []

    for line in lines:
        m = SPEAKER_RE.match(line.strip())
        if m:
            seen_speaker = True
            flush()
            cur_speaker = m.group(1)
            cur_body = []
        else:
            if not seen_speaker:
                prefix.append(line)
            else:
                cur_body.append(line)
    flush()
    return prefix, blocks

def clean_body(lines):
    # Preserve words exactly; only normalize blank edges.
    while lines and not lines[0].strip():
        lines = lines[1:]
    while lines and not lines[-1].strip():
        lines = lines[:-1]
    return lines

def merge_same_speaker(prefix, blocks):
    merged = []
    removed = 0
    for speaker, body in blocks:
        body = clean_body(body)
        if merged and merged[-1][0] == speaker:
            removed += 1
            prev = merged[-1][1]
            # Join consecutive utterance fragments as continuous speech.
            prev_text = '\n'.join(prev).strip()
            body_text = '\n'.join(body).strip()
            if prev_text and body_text:
                # If both are single paragraphs, join with a space; otherwise keep paragraph break.
                if '\n\n' not in prev_text and '\n\n' not in body_text:
                    merged[-1][1] = [prev_text + ' ' + body_text]
                else:
                    merged[-1][1] = (prev_text + '\n\n' + body_text).splitlines()
            elif body_text:
                merged[-1][1] = body
        else:
            merged.append([speaker, body])
    return merged, removed

def render(prefix, blocks):
    out = prefix[:]
    while out and not out[-1].strip():
        out.pop()
    if out:
        out.append('')
    for i, (speaker, body) in enumerate(blocks):
        out.append(f'**{speaker}**')
        out.append('')
        out.extend(body)
        if i != len(blocks)-1:
            out.append('')
    return '\n'.join(out).rstrip() + '\n'

summary = []
for ep in range(1, 14):
    p = ROOT / f'{ep}.md'
    text = p.read_text(encoding='utf-8')
    before = text
    if ep == 1:
        # User-confirmed audio resolutions, in occurrence order.
        text = text.replace('[نامفهوم]', 'به خاطر', 1)
        text = text.replace('[نامفهوم]', 'چه استعاره‌ی خوبی', 1)
    prefix, blocks = parse_blocks(text)
    merged, removed = merge_same_speaker(prefix, blocks)
    new = render(prefix, merged)
    p.write_text(new, encoding='utf-8')
    summary.append((ep, removed, before.count('[نامفهوم]'), new.count('[نامفهوم]')))

report = Path('reports/khane_to_speaker_formatting.md')
lines = [
    '# گزارش یکدست‌سازی گوینده‌ها — خانه تو', '',
    '- فقط برچسب‌های تکراریِ گوینده در گفتارهای پشت‌سرهم ادغام شده‌اند.',
    '- متن گفتار، ترتیب گویندگان و محتوا حفظ شده است.',
    '- دو `[نامفهوم]` قسمت ۱ با شنیدن کاربر رفع شد: `به خاطر` و `چه استعاره‌ی خوبی`.', '',
    '## نتیجه',
]
for ep, removed, old_u, new_u in summary:
    lines.append(f'- قسمت {ep}: {removed} برچسب تکراری حذف شد؛ نامفهوم {old_u} → {new_u}')
report.write_text('\n'.join(lines) + '\n', encoding='utf-8')

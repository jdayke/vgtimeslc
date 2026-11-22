# Square 1080x1080 VGTimes repost (for X): header on top, image below with smooth push-in, + music.
# python repost_square.py "HEADLINE / LINE2" image.png bed.wav dur out.mp4 ["fx,fy"] ["CapCut name"]
import sys, os, re, math, subprocess
from PIL import Image, ImageDraw, ImageFont
ROOT = r'J:\Claude\VGTimes and LibertyCity'; FF = r'C:\ffmpeg\bin\ffmpeg.exe'
FONTS = ROOT + r'\Tools\fonts'; G = ROOT + r'\Graphics\Repost template'
S = 1080; TOP = 262                                  # image window: y 262..1080 (1080x818)
def template(title):
    im = Image.new('RGBA', (S, S), (255, 255, 255, 255))
    av = Image.open(G + r'\repost_avatar.png').convert('RGBA').resize((96, 96), Image.LANCZOS); im.alpha_composite(av, (40, 34))
    d = ImageDraw.Draw(im)
    nf = ImageFont.truetype(FONTS + r'\arialbd.ttf', 44); d.text((152, 80), 'VGTimes', font=nf, fill=(0, 0, 0), anchor='ls')
    bx = 152 + int(d.textlength('VGTimes', font=nf)) + 12
    bd = Image.open(G + r'\repost_badge.png').convert('RGBA').resize((32, 32), Image.LANCZOS); im.alpha_composite(bd, (bx, 50))
    d.text((153, 121), '@VGTimes', font=ImageFont.truetype(FONTS + r'\arial.ttf', 30), fill=(83, 100, 113), anchor='ls')
    hf = ImageFont.truetype(FONTS + r'\ariblk.ttf', 40); lines = []
    for part in re.split(r'\s*(?:\||\s/\s|\n)\s*', title.upper()):
        cur = ''
        for w in part.split():
            t = (cur + ' ' + w).strip()
            if d.textlength(t, font=hf) <= S - 80: cur = t
            else: lines.append(cur); cur = w
        if cur: lines.append(cur)
    if len(lines) > 2: raise SystemExit('square: max 2 headline lines')
    for i, l in enumerate(lines): d.text((40, 190 + 44 * i), l, font=hf, fill=(0, 0, 0), anchor='ls')
    d.rectangle((0, TOP, S - 1, S - 1), fill=(0, 0, 0, 0)); return im
def main():
    title, img, bed, dur, out = sys.argv[1], sys.argv[2], sys.argv[3], float(sys.argv[4]), sys.argv[5]
    focus = tuple(float(x) for x in sys.argv[6].split(',')) if len(sys.argv) > 6 else None
    tp = template(title); tp.save(os.path.splitext(out)[0] + '_template.png')
    src = Image.open(img).convert('RGB')
    if src.width > 2700: src = src.resize((2700, round(src.height * 2700 / src.width)), Image.LANCZOS)
    sw, sh = src.size; WH = S - TOP; A = S / WH
    w0 = min(sw, sh * A); h0 = w0 / A; cx0, cy0 = sw / 2, sh / 2; w1 = w0 / 1.25; h1 = w1 / A
    if focus: cx1 = min(max(focus[0] * sw, w1 / 2), sw - w1 / 2); cy1 = min(max(focus[1] * sh, h1 / 2), sh - h1 / 2)
    else: cx1, cy1 = cx0, max(h1 / 2, cy0 - (h0 - h1) * 0.45)
    N = int(math.ceil(dur * 60))
    p = subprocess.Popen([FF, '-y', '-hide_banner', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', '%dx%d' % (S, S), '-r', '60', '-i', '-',
                          '-i', bed, '-map', '0:v', '-map', '1:a', '-c:v', 'h264_nvenc', '-preset', 'p7', '-cq', '18', '-b:v', '0', '-pix_fmt', 'yuv420p',
                          '-c:a', 'aac', '-b:a', '256k', '-shortest', '-movflags', '+faststart', out], stdin=subprocess.PIPE)
    base = Image.new('RGBA', (S, S), (255, 255, 255, 255))
    for i in range(N):
        e = (1 - math.cos(math.pi * i / (N - 1))) / 2
        w = w0 + (w1 - w0) * e; h = w / A; cx = cx0 + (cx1 - cx0) * e; cy = cy0 + (cy1 - cy0) * e
        f = base.copy(); f.paste(src.resize((S, WH), Image.LANCZOS, box=(cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2)), (0, TOP))
        f.alpha_composite(tp); p.stdin.write(f.convert('RGB').tobytes())
        if i == 0: f.convert('RGB').save(os.path.splitext(out)[0] + '.jpg', quality=92)   # still image for an image post
    p.stdin.close(); p.wait(); print('DONE', out, p.returncode)
    # CapCut project (1080x1080): the mp4 muted + the music as its own track, so it can be swapped/turned down
    import json
    DR = r'J:\CapCut\CapCut Drafts'; base = sys.argv[7] if len(sys.argv) > 7 else 'VGT ' + os.path.splitext(os.path.basename(out))[0]
    v = 1
    while os.path.exists(os.path.join(DR, '%s v%d' % (base, v))): v += 1
    name = '%s v%d' % (base, v)
    spec = {'canvas': [S, S], 'shots': [{'path': out.replace('\\', '/'), 't': 0, 'dur': dur, 'file_dur': N / 60, 'vol': 0.0, 'has_audio': True}],
            'labels': [], 'subs': [], 'voice': [], 'voice_path': '', 'voice_dur': 0,
            'audio_tracks': [{'path': bed.replace('\\', '/'), 'file_dur': dur, 'segs': [{'a': 0, 'b': dur, 't': 0, 'vol': 1.0}]}]}
    sp = os.path.splitext(out)[0] + '_spec.json'; json.dump(spec, open(sp, 'w'))
    subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'make_draft4.py'), os.path.join(DR, name), name, sp], check=True)
    print('CAPCUT', name)
main()

# VGTimes Repost short in one command (runs on the PC).
# python repost.py "HEADLINE" <image|video> <music url|file> <start mm:ss> <duration s> ["Project name"] ["fx,fy" push-in target]
# Builds: template PNG (Arial, Repost template spec) -> 1080x1920 60fps mp4 (image: smooth push-in; video: centre crop)
#         -> music cut + 3 s fade -> CapCut draft in J:\CapCut\CapCut Drafts\<name> (raised to top of the list if CapCut is closed).
import sys, os, re, math, json, subprocess, shutil, time, datetime
from PIL import Image, ImageDraw, ImageFont
ROOT = r'J:\Claude\VGTimes and LibertyCity'
FF = r'C:\ffmpeg\bin\ffmpeg.exe'; FP = r'C:\ffmpeg\bin\ffprobe.exe'
FONTS = ROOT + r'\Tools\fonts'; G = ROOT + r'\Graphics\Repost template'
DRAFTS = r'J:\CapCut\CapCut Drafts'
HERE = os.path.dirname(os.path.abspath(__file__))
MEDIA = ['']
WH = int(os.environ.get('REPOST_WIN_H', '760'))   # video window height (y 610..610+WH); 760 = template default

def secs(s):
    s = str(s); p = [float(x) for x in s.split(':')]
    return p[0] * 60 + p[1] if len(p) == 2 else (p[0] * 3600 + p[1] * 60 + p[2] if len(p) == 3 else p[0])

def template(title, out):
    im = Image.new('RGBA', (1080, 1920), (255, 255, 255, 255))
    im.alpha_composite(Image.open(G + r'\repost_avatar.png').convert('RGBA'), (64, 256))
    im.alpha_composite(Image.open(G + r'\repost_badge.png').convert('RGBA'), (464, 276))
    d = ImageDraw.Draw(im)
    d.text((209, 313), 'VGTimes', font=ImageFont.truetype(FONTS + r'\arialbd.ttf', 53), fill=(0, 0, 0), anchor='ls')
    d.text((210, 364), '@VGTimes', font=ImageFont.truetype(FONTS + r'\arial.ttf', 36), fill=(83, 100, 113), anchor='ls')
    hf = ImageFont.truetype(FONTS + r'\ariblk.ttf', 43)
    lines = []
    for part in re.split(r'\s*(?:\||\s/\s|\n)\s*', title.upper()):   # forced breaks: ' / ', '|' or newline
        cur = ''
        for w in part.split():
            t = (cur + ' ' + w).strip()
            if d.textlength(t, font=hf) <= 952: cur = t
            else: lines.append(cur); cur = w
        if cur: lines.append(cur)
    if len(lines) > 4: raise SystemExit('Headline too long: %d lines (max 4)' % len(lines))
    for i, l in enumerate(lines): d.text((64, 439 + 47 * i), l, font=hf, fill=(0, 0, 0), anchor='ls')
    em = os.environ.get('REPOST_EMOJI')                       # optional colour emoji PNG after the headline (Arial has no emoji)
    if em and lines:
        e = Image.open(em).convert('RGBA').resize((46, 46), Image.LANCZOS)
        im.alpha_composite(e, (int(64 + d.textlength(lines[-1], font=hf) + 12), 439 + 47 * (len(lines) - 1) - 38))
    d.rectangle((0, 610, 1079, 610 + WH - 1), fill=(0, 0, 0, 0))
    im.save(out); return lines

def bake_image(img, tpl, dur, out, focus=None):
    src = Image.open(img).convert('RGB'); tp = Image.open(tpl).convert('RGBA')
    if src.width > 2700: src = src.resize((2700, round(src.height * 2700 / src.width)), Image.LANCZOS)   # huge sources make PIL slow
    sw, sh = src.size; A = 1080 / WH
    w0 = min(sw, sh * A); h0 = w0 / A                       # full-window crop
    cx0, cy0 = sw / 2, sh / 2
    w1 = w0 / 1.25; h1 = w1 / A                             # end: x1.25
    if focus:                                               # end centre on the subject (fractions of the image), clamped inside
        cx1 = min(max(focus[0] * sw, w1 / 2), sw - w1 / 2); cy1 = min(max(focus[1] * sh, h1 / 2), sh - h1 / 2)
    else:                                                   # default: drift up a little (faces are usually upper half)
        cx1 = cx0; cy1 = max(h1 / 2, cy0 - (h0 - h1) * 0.45)
    N = int(math.ceil(dur * 60)) + 6
    cmd = [FF, '-y', '-hide_banner', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', '1080x1920', '-r', '60', '-i', '-',
           '-c:v', 'h264_nvenc', '-preset', 'p7', '-cq', '17', '-b:v', '0', '-pix_fmt', 'yuv420p', out]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE); base = Image.new('RGBA', (1080, 1920), (255, 255, 255, 255))
    for i in range(N):
        e = (1 - math.cos(math.pi * min(1.0, i / (N - 1)))) / 2
        w = w0 + (w1 - w0) * e; h = w / A; cx = cx0 + (cx1 - cx0) * e; cy = cy0 + (cy1 - cy0) * e
        f = base.copy(); f.paste(src.resize((1080, WH), Image.LANCZOS, box=(cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2)), (0, 610))
        f.alpha_composite(tp); p.stdin.write(f.convert('RGB').tobytes())
    p.stdin.close(); p.wait(); return N / 60

def bake_video(vid, tpl, dur, out, ss=0):
    fc = ('[0:v]scale=1080:%d:force_original_aspect_ratio=increase,crop=1080:%d,' % (WH, WH) + 'setsar=1,fps=60[v0];'
          'color=white:s=1080x1920:r=60[bg];[bg][v0]overlay=0:610:shortest=1[v1];[v1][1:v]overlay=0:0,format=yuv420p[v]')
    subprocess.run([FF, '-y', '-hide_banner', '-loglevel', 'error', '-ss', str(ss), '-i', vid, '-loop', '1', '-framerate', '60', '-i', tpl,
                    '-filter_complex', fc, '-map', '[v]', '-t', '%.3f' % (dur + 0.1), '-c:v', 'h264_nvenc', '-preset', 'p7', '-cq', '17', '-b:v', '0', out], check=True)
    return dur + 0.1

def music(src, start, dur, wdir):
    out = os.path.join(wdir, 'music', 'bed.wav'); os.makedirs(os.path.dirname(out), exist_ok=True)
    if src == 'orig':
        subprocess.run([FF, '-y', '-hide_banner', '-loglevel', 'error', '-ss', str(start), '-i', MEDIA[0], '-t', str(dur), '-vn', '-af', 'afade=t=out:st=%.2f:d=0.4' % (dur - 0.4), '-ar', '48000', '-ac', '2', out], check=True)
        return out
    if re.match(r'https?://', src):
        tmp = os.path.join(wdir, 'music', 'src.%(ext)s')
        # full track, then exact cut (--download-sections starts up to ~4 s early)
        subprocess.run(['yt-dlp', '--no-playlist', '-f', 'ba', '-x', '--audio-format', 'wav',
                        '--ffmpeg-location', os.path.dirname(FF), '-o', tmp, src], check=True)
        src = os.path.join(wdir, 'music', 'src.wav')
    subprocess.run([FF, '-y', '-hide_banner', '-loglevel', 'error', '-ss', str(start), '-i', src, '-t', str(dur),
                    '-af', 'afade=t=in:d=0.05,afade=t=out:st=%.2f:d=3' % (dur - 3), '-ar', '48000', '-ac', '2', out], check=True)
    return out

def raise_in_list(name):
    if 'CapCut' in subprocess.run(['tasklist'], capture_output=True, text=True).stdout:
        print('CapCut is open: the project appears after CapCut restarts'); return
    p = os.path.join(os.environ['LOCALAPPDATA'], 'CapCut', 'User Data', 'Projects', 'com.lveditor.draft', 'root_meta_info.json')
    d = json.loads(open(p, encoding='utf-8').read())
    hit = [e for e in d['all_draft_store'] if e.get('draft_name') == name]
    if hit:
        shutil.copy2(p, p + '.bak'); hit[0]['tm_draft_modified'] = int(time.time() * 1e6)
        open(p, 'w', encoding='utf-8').write(json.dumps(d, ensure_ascii=False, separators=(',', ':'))); print('raised in CapCut list')
    else:
        print('new project: CapCut adds it on next start')

def main():
    a = sys.argv[1:]
    if len(a) < 5: raise SystemExit(__doc__ or 'usage: repost.py "HEADLINE" media music start dur [name]')
    title, media, mus, start, dur = a[0], a[1], a[2], secs(a[3]), float(a[4])
    MEDIA[0] = media
    slug = re.sub(r' +', ' ', re.sub(r'[^A-Za-z0-9 ]', ' ', title.title()))[:40].strip()
    name = a[5] if len(a) > 5 and a[5] else 'VGT ' + slug
    focus = tuple(float(x) for x in a[6].split(',')) if len(a) > 6 else None   # optional 'fx,fy' push-in target
    v = 1
    while os.path.exists(os.path.join(DRAFTS, '%s v%d' % (name, v))): v += 1
    name = '%s v%d' % (name, v)
    wdir = os.path.join(ROOT, 'Work', datetime.date.today().strftime('%Y %m %d') + ' ' + name); os.makedirs(wdir + r'\shots', exist_ok=True)   # one folder per project version
    t0 = time.time()
    lines = template(title, wdir + r'\template.png'); print('headline:', lines)
    bed = music(mus, start, dur, wdir); print('music ok %.0fs' % (time.time() - t0))
    shot = wdir + r'\shots\SHOT_01.mp4'
    is_img = os.path.splitext(media)[1].lower() in ('.png', '.jpg', '.jpeg', '.webp', '.bmp')
    fd = bake_image(media, wdir + r'\template.png', dur, shot, focus) if is_img else bake_video(media, wdir + r'\template.png', dur, shot, start if mus == 'orig' else 0)
    print('video ok %.0fs' % (time.time() - t0))
    C = os.environ.get('REPOST_COLOR', '#FD3737')
    SUBS = [{'text': t, 't': a, 'dur': d, 'y': float(os.environ.get('REPOST_SUB_Y', '-0.52')), 'style': {'fg': C, 'bg': '#FFFFFF', 'size': 8.0}} for t, a, d in (json.load(open(os.environ['REPOST_SUBS'])) if os.environ.get('REPOST_SUBS') else [])]
    spec = {'shots': [{'path': shot.replace('\\', '/'), 't': 0, 'dur': dur, 'file_dur': fd, 'vol': 0.0, 'has_audio': False}],
            'labels': [], 'subs': SUBS, 'voice': [], 'voice_path': '', 'voice_dur': 0,
            'audio_tracks': [{'path': bed.replace('\\', '/'), 'file_dur': dur, 'segs': [{'a': 0, 'b': dur, 't': 0, 'vol': 1.0}]}]}
    sp = wdir + r'\spec.json'; json.dump(spec, open(sp, 'w'))
    subprocess.run([sys.executable, os.path.join(HERE, 'make_draft4.py'), os.path.join(DRAFTS, name), name, sp], check=True)
    raise_in_list(name)
    subprocess.run([FF, '-y', '-hide_banner', '-loglevel', 'error', '-ss', '1', '-i', shot, '-frames:v', '1', '-vf', 'scale=540:-1', wdir + r'\preview.jpg'])
    print('DONE %s in %.0fs -> %s' % (name, time.time() - t0, wdir))

if __name__ == '__main__':
    main()

# cut_guard.py v2 (13.11.2026) - ZERO stray frames at cuts. Mandatory for every short.
# Per-frame scene scores (GPU decode), hard cuts = score >= 0.3, or a local peak
# (>= 0.08 and >= 3x the 3 frames before and the frame 2 after). Fast motion
# (explosions, dust, wheelies) is NOT a cut; real cuts are.
# Usage:
#   python cut_guard.py cuts  <video>                  -> prints hard cuts (cache <video>.scores.json)
#   python cut_guard.py check <video> <start> <dur>    -> exit 1 if a hard cut is inside the window
#   python cut_guard.py plan  <shots.json>             -> check every video part of a shot list, exit 1 on FAIL
#   python cut_guard.py baked <clip.mp4> [...]         -> exit 1 if a baked clip contains an undeclared cut
# Window rule: start >= cut + 0.08 s; start + dur + 2 frames <= next cut - 0.12 s.
# Soft flags (score >= 0.08 inside a window, not classified as cut) are printed as WARN:
# they must be checked by eye (frame pair before/after) - phone-video overlays and dark
# shots can hide real cuts under low scores.
# Bake scripts MUST call assert_window() for every part and stop on failure.
import sys, os, re, json, subprocess
MARGIN_IN, MARGIN_OUT, EXTRA = 0.08, 0.12, 2 / 30
HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, 'cut_cache')

def _cache_path(src):
    p = src + '.scores.json'
    try:
        open(p, 'a').close(); return p
    except OSError:
        os.makedirs(CACHE, exist_ok=True)
        return os.path.join(CACHE, os.path.basename(src) + '.scores.json')

def scores(src):
    cp = _cache_path(src)
    if os.path.exists(cp) and os.path.getsize(cp) > 10:
        d = json.load(open(cp)); return d['t'], d['s']
    vf = "scale=480:-2,select='gte(scene,0)',metadata=print:key=lavfi.scene_score"
    for pre in (['-hwaccel', 'cuda'], []):
        r = subprocess.run(['ffmpeg', '-hide_banner'] + pre + ['-i', src, '-an', '-vf', vf, '-f', 'null', '-'], capture_output=True, text=True).stderr
        t = [float(x) for x in re.findall(r'pts_time:([0-9.]+)', r)]
        s = [float(x) for x in re.findall(r'lavfi.scene_score=([0-9.]+)', r)]
        if t and len(t) == len(s): break
    json.dump({'t': t, 's': s}, open(cp, 'w'))
    return t, s

def classify(t, s):
    hard, soft = [], []
    for i in range(len(s)):
        prev = max(s[max(0, i - 3):i] or [0]); nxt = s[i + 2] if i + 2 < len(s) else 0
        if s[i] >= 0.3 or (s[i] >= 0.08 and s[i] >= 3 * max(prev, 0.005) and s[i] >= 3 * max(nxt, 0.005)):
            hard.append(round(t[i], 3))
        elif s[i] >= 0.08:
            soft.append(round(t[i], 3))
    return hard, soft

def cuts(src):
    return classify(*scores(src))[0]

def check(src, start, dur):
    hard, soft = classify(*scores(src))
    end = start + dur + EXTRA
    bad = [c for c in hard if start - MARGIN_IN < c < end + MARGIN_OUT]
    warn = [c for c in soft if start < c < end]
    return bad, warn

def clean_window(src, t0):
    h = [0.0] + cuts(src) + [1e9]
    for a, b in zip(h, h[1:]):
        if a <= t0 + 1e-3 < b: return round(a + MARGIN_IN, 3), round(b - MARGIN_OUT - EXTRA, 3)

def assert_window(src, start, dur, label=''):
    bad, warn = check(src, start, dur)
    if bad:
        raise SystemExit('CUT_GUARD FAIL %s %s %.3f+%.3f cuts %s clean %s' % (label, os.path.basename(src), start, dur, bad, clean_window(src, start)))
    if warn: print('CUT_GUARD WARN (check by eye) %s %s soft %s' % (label, os.path.basename(src), warn))
    return True

def baked(clip, joins=()):
    hard, soft = classify(*scores(clip))
    return [c for c in hard if c > 0.05 and not any(abs(c - j) < 0.05 for j in joins)]

if __name__ == '__main__':
    m = sys.argv[1]
    if m == 'cuts': print(cuts(sys.argv[2]))
    elif m == 'check':
        bad, warn = check(sys.argv[2], float(sys.argv[3]), float(sys.argv[4]))
        print('OK' if not bad else 'FAIL cuts %s' % bad, 'WARN soft %s' % warn if warn else ''); sys.exit(1 if bad else 0)
    elif m == 'plan':
        shots = json.load(open(sys.argv[2])); fail = 0; n = 0
        for sh in shots:
            for p in sh.get('parts', []):
                n += 1
                bad, warn = check(p['path'], p['ss'], p['len'])
                print(sh['name'], os.path.basename(p['path']), p['ss'], p['len'], 'FAIL %s' % bad if bad else 'OK', 'WARN %s' % warn if warn else '')
                fail |= bool(bad)
        print('windows', n, 'FAIL' if fail else 'ALL OK'); sys.exit(1 if fail else 0)
    elif m == 'baked':
        fail = 0
        for f in sys.argv[2:]:
            b = baked(f); print(f, 'OK' if not b else 'CUTS %s' % b); fail |= bool(b)
        sys.exit(1 if fail else 0)

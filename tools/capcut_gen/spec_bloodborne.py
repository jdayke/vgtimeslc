# Spec example for Bloodborne x Quake (shots, labels in lanes, subtitles from whisper words, voice pieces).
import json, sys
W = json.load(open("/mnt/user-data/uploads/VGTimes and LibertyCity/Work/2026 11 10 Bloodborne/voices/EN_Andrew_bb_words.json"))
FILEDUR = json.load(open(sys.argv[1])) if len(sys.argv) > 1 else {}
base = "J:/Claude/VGTimes and LibertyCity/Work/2026 11 10 Bloodborne/capcut_shots_v1/"
durs = [2.10, 3.00, 4.00, 3.40, 3.80, 1.30, 2.30, 0.80, 3.90, 3.20, 2.60, 6.40, 2.40]
shots = []; t = 0.0
for i, du in enumerate(durs):
    n = 'BB_%02d' % (i + 1)
    shots.append({'path': base + n + '.mp4', 't': round(t, 4), 'dur': du, 'file_dur': FILEDUR.get(n, du + 0.07), 'vol': 1.0})
    t += du
T = {('S%d' % (i + 1)): s['t'] for i, s in enumerate(shots)}
# voice pieces: src [a,b] -> timeline t
P = [(0.12, 0.88, 0.25), (1.24, 3.72, T['S2'] + 0.15), (4.09, 6.42, T['S3'] + 0.30), (6.66, 7.67, T['S4'] + 0.15),
     (8.00, 8.68, T['S4'] + 1.45), (8.87, 9.65, T['S5'] + 0.15), (9.86, 11.86, T['S6'] + 0.15), (12.22, 14.54, T['S10'] + 0.15),
     (14.93, 16.05, T['S12'] + 0.60), (16.42, 17.75, T['S12'] + 2.20), (18.13, 18.86, T['S13'] + 0.20)]
voice = [{'a': a, 'b': b, 't': round(tt, 3)} for a, b, tt in P]
def at(w):  # map voice-file time to timeline
    for a, b, tt in P:
        if a - 0.05 <= w <= b + 0.05: return tt + (w - a)
    raise Exception(w)
words = [(x['w'].strip(), x['s'], x['e']) for x in W]
def wt(i): return at(words[i][1])
def we(i): return at(words[i][2])
idx = {}
for i, (w, s, e) in enumerate(words): idx.setdefault(w.lower().strip('.,?'), []).append(i)
# subtitle chunks: (text, first word index, last word index)
def find(seq):
    ws = [w.lower().strip('.,?') for w, _, _ in words]
    for i in range(len(ws)):
        if ws[i:i + len(seq)] == seq: return i, i + len(seq) - 1
    raise Exception(seq)
chunks = [("A NEW PLUGIN BRINGS", ['a', 'new', 'plug', '-in', 'brings']), ("FIRST-PERSON COMBAT", ['first', '-person', 'combat']),
          ("QUAKE-STYLE MOVEMENT", ['quake', '-style', 'movement']), ("BUNNY HOPPING", ['bunny', '-hopping']),
          ("ROCKET JUMPS", ['rocket', 'jumps']), ("AND ARENA-SHOOTER WEAPONS", ['and', 'arena', 'shooter', 'weapons']),
          ("STRAIGHT INTO YHARNAM", ['straight', 'into', 'yharnam']), ("EVEN FATHER GASCOIGNE", ['even', 'father', 'gas', 'coin']),
          ("DOESN'T STAND A CHANCE", ["doesn't", 'stand', 'a', 'chance']), ("SAME BLOODBORNE WORLD", ['same', 'bloodborne', 'world']),
          ("COMPLETELY DIFFERENT", ['completely', 'different']), ("WAY TO PLAY IT", ['way', 'to', 'play', 'it']),
          ("WOULD YOU PLAY THIS?", ['would', 'you', 'play', 'this'])]
SUB = {'fg': '#FD3737', 'bg': '#FFFFFF', 'size': 8.0}
HOOK = {'fg': '#FFFFFF', 'bg': '#FD3737', 'size': 9.0}
LAB = {'fg': '#FFFFFF', 'bg': '#FD3737', 'size': 7.0}
subs = []
for k, (txt, seq) in enumerate(chunks):
    i, j = find(seq)
    s = wt(i) - 0.05
    e = (wt(find(chunks[k + 1][1])[0]) - 0.05) if k + 1 < len(chunks) else we(j) + 0.6
    e = min(e, we(j) + 0.6)
    subs.append({'text': txt, 't': round(s, 3), 'dur': round(e - s, 3), 'y': -0.47, 'style': SUB})
end = shots[-1]['t'] + shots[-1]['dur']
subs[-1]['dur'] = round(end - subs[-1]['t'], 3)
def sh(n): return shots[n - 1]
labels = [
 {'text': 'THIS IS BLOODBORNE', 't': 0.0, 'dur': sh(1)['dur'], 'y': 0.51, 'style': HOOK},
 {'text': 'BLOODBORNE + QUAKE MECHANICS', 't': sh(2)['t'], 'dur': sh(2)['dur'], 'y': 0.51, 'style': dict(HOOK, size=8.0)},
 {'text': 'SAME YHARNAM', 't': sh(3)['t'], 'dur': sh(3)['dur'], 'y': 0.0, 'style': LAB},
 {'text': 'DODGE', 't': sh(4)['t'], 'dur': sh(4)['dur'], 'y': 0.085, 'style': LAB},
 {'text': 'BUNNY HOP', 't': sh(4)['t'], 'dur': sh(4)['dur'], 'y': -0.085, 'style': LAB, 'lane': 2},
 {'text': 'A GUN', 't': sh(6)['t'], 'dur': sh(6)['dur'], 'y': 0.51, 'style': LAB},
 {'text': 'A GRENADE LAUNCHER?!', 't': sh(7)['t'], 'dur': sh(7)['dur'] + sh(8)['dur'], 'y': 0.51, 'style': LAB},
 {'text': 'ORIGINAL COMBAT', 't': sh(9)['t'], 'dur': sh(9)['dur'], 'y': 0.085, 'style': LAB},
 {'text': 'QUAKE MECHANICS', 't': sh(9)['t'], 'dur': sh(9)['dur'], 'y': -0.085, 'style': LAB, 'lane': 2},
 {'text': 'YHARNAM', 't': sh(12)['t'], 'dur': sh(12)['dur'], 'y': 0.51, 'style': {'fg': '#FFFFFF', 'bg': '#FD3737', 'size': 6.0}},
 {'text': 'BLOODBORNE × QUAKE', 't': sh(13)['t'], 'dur': sh(13)['dur'], 'y': 0.12, 'style': {'fg': '#FFFFFF', 'bg': '#FD3737', 'size': 11.0}},
]
spec = {'shots': shots, 'labels': labels, 'subs': subs, 'voice': voice,
        'voice_path': "J:/Claude/VGTimes and LibertyCity/Work/2026 11 10 Bloodborne/voices/EN_Andrew_bb.mp3", 'voice_dur': 19.176,
        'logo': {'t': sh(3)['t'], 'dur': round(end - sh(3)['t'], 3)}}
json.dump(spec, open('/home/claude/gen/spec.json', 'w'), indent=1, ensure_ascii=False)
for s in subs: print('%6.2f %5.2f %s' % (s['t'], s['dur'], s['text']))
for v in voice: print('voice', v)
print('end', end)

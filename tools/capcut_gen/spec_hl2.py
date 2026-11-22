import json, sys
W = json.load(open("/mnt/user-data/uploads/VGTimes and LibertyCity/Work/2026 11 12 HL2 Gordon/voices/EN_Andrew_hl2_words.json"))
FD = json.load(open(sys.argv[1])) if len(sys.argv) > 1 else {}
base = "J:/Claude/VGTimes and LibertyCity/Work/2026 11 12 HL2 Gordon/"
durs = [2.85, 2.25, 1.90, 2.05, 2.95, 2.00, 0.45, 3.15, 3.75, 0.80, 0.85, 1.95, 0.80, 1.45]
shots = []; t = 0.0
for i, du in enumerate(durs):
    n = 'HL_%02d' % (i + 1)
    shots.append({'path': base + 'capcut_shots_v1/' + n + '.mp4', 't': round(t, 4), 'dur': du, 'file_dur': FD.get(n, du + 0.07), 'vol': 0.0, 'has_audio': False})
    t += du
END = round(t, 3)
def sh(k): return shots[k - 1]
# voice pieces: (src a, src b, timeline t)
P = [(0.10, 2.72, 0.15), (3.06, 4.90, sh(2)['t'] + 0.10), (5.23, 8.84, sh(3)['t'] + 0.10), (9.27, 11.30, sh(5)['t'] + 0.10),
     (11.68, 13.34, sh(6)['t'] + 0.05), (13.67, 16.88, sh(8)['t']), (17.23, 18.37, sh(9)['t'] + 0.10), (18.70, 21.00, sh(9)['t'] + 1.45),
     (21.35, 22.05, sh(10)['t'] + 0.05), (22.31, 25.50, sh(11)['t'] + 0.05)]
voice = [{'a': a, 'b': b, 't': round(tt, 3)} for a, b, tt in P]
def at(w):
    for a, b, tt in P:
        if a - 0.06 <= w <= b + 0.06: return tt + (w - a)
    raise Exception(w)
words = [(x['w'].strip().lower().strip('.,?'), x['s'], x['e']) for x in W]
def find(seq, start=0):
    ws = [w for w, _, _ in words]
    for i in range(start, len(ws)):
        if ws[i:i + len(seq)] == seq: return i, i + len(seq) - 1
    raise Exception(seq)
chunks = [("THE ORIGINAL SOFTIMAGE PROJECT", ['the', 'original', 'soft', 'image', 'project']), ("USED FOR HIS PROMO MODEL", ['used', 'for', 'his', 'promo', 'model']),
          ("JUST LEAKED", ['just', 'leaked']), ("HE LOOKS A LITTLE DIFFERENT", ['he', 'looks', 'a', 'little', 'different']),
          ("WITHOUT THE PAINT-OVER", ['without', 'the', 'paint', 'over']), (None, ['first', 'of', 'all']), (None, ['apparently']),
          ("THIS CURSED-LOOKING THING?", ['this', 'cursed', 'looking', 'thing']), ("THAT'S GORDON'S ACTUAL", ["that's", "gordon's", 'actual']),
          ("FLATTENED FACE TEXTURE", ['flattened', 'face', 'texture']), ("SO YES", ['so', 'yes']), ("ONE OF GAMING'S", ['one', 'of', "gaming's"]),
          ("MOST ICONIC FACES", ['most', 'iconic', 'faces']), ("STARTED OUT LOOKING LIKE THIS", ['started', 'out', 'looking', 'like', 'this'])]
SUB = {'fg': '#FD3737', 'bg': '#FFFFFF', 'size': 8.0}
HOOK = {'fg': '#FFFFFF', 'bg': '#FD3737', 'size': 8.0}
LAB = {'fg': '#FFFFFF', 'bg': '#FD3737', 'size': 8.0}
pos = 0; idxs = []
for txt, seq in chunks:
    i, j = find(seq, pos); pos = i + 1
    idxs.append((txt, i, j))
subs = []
for k, (txt, i, j) in enumerate(idxs):
    if txt is None: continue
    s = at(words[i][1]) - 0.05
    nxt = at(words[idxs[k + 1][1]][1]) - 0.05 if k + 1 < len(idxs) else END
    e = min(nxt, at(words[j][2]) + 0.5)
    subs.append({'text': txt, 't': round(s, 3), 'dur': round(e - s, 3), 'y': -0.47, 'style': SUB})
no_t = at(words[find(['no', 'ponytail'])[0]][1]) - 0.05
labels = [
 {'text': 'THIS IS GORDON FREEMAN', 't': 0.0, 'dur': sh(3)['t'], 'y': 0.84, 'style': HOOK},
 {'text': 'WITHOUT THE ARTWORK', 't': 0.0, 'dur': sh(3)['t'], 'y': 0.745, 'style': HOOK, 'lane': 2},
 {'text': 'ORIGINAL XSI PROJECT LEAKED', 't': sh(3)['t'], 'dur': sh(5)['t'] - sh(3)['t'], 'y': 0.55, 'style': LAB},
 {'text': 'WITH THE ARTWORK', 't': sh(5)['t'], 'dur': sh(5)['dur'], 'y': 0.085, 'style': LAB},
 {'text': 'WITHOUT IT', 't': sh(5)['t'], 'dur': sh(5)['dur'], 'y': -0.085, 'style': LAB, 'lane': 2},
 {'text': 'NO PONYTAIL 💀', 't': round(no_t, 3), 'dur': round(sh(7)['t'] - no_t, 3), 'y': 0.55, 'style': dict(LAB, size=10.0)},
 {'text': 'HALF-LIFE 1', 't': sh(7)['t'], 'dur': sh(7)['dur'], 'y': 0.55, 'style': LAB},
 {'text': '20 YEARS IN STASIS', 't': sh(8)['t'], 'dur': 1.65, 'y': 0.55, 'style': LAB},
 {'text': '= FREE HAIRCUT', 't': round(sh(8)['t'] + 1.65, 3), 'dur': round(sh(8)['dur'] - 1.65, 3), 'y': 0.55, 'style': dict(LAB, size=10.0)},
 {'text': 'WHAT THE HELL IS THIS', 't': sh(9)['t'], 'dur': 1.70, 'y': 0.55, 'style': LAB},
 {'text': 'GORDON FREEMAN', 't': round(sh(9)['t'] + 1.70, 3), 'dur': round(sh(9)['dur'] - 1.70, 3), 'y': 0.55, 'style': dict(LAB, size=10.0)},
 {'text': 'FROM THIS 💀', 't': sh(13)['t'], 'dur': sh(13)['dur'], 'y': 0.55, 'style': dict(LAB, size=10.0)},
 {'text': 'TO THIS 🗿', 't': sh(14)['t'], 'dur': sh(14)['dur'], 'y': 0.55, 'style': dict(LAB, size=10.0)},
]
SFXB = base + 'sfx/sfx_boom.wav'; SFXS = base + 'sfx/sfx_scratch.wav'
pony_t = at(words[find(['no', 'ponytail'])[1]][1])
sfx = {'segs': [
  {'path': SFXB, 'file_dur': 1.5, 'a': 0, 'b': 1.4, 't': round(pony_t, 3), 'vol': 0.9},
  {'path': SFXS, 'file_dur': 0.55, 'a': 0, 'b': 0.55, 't': round(sh(9)['t'] - 0.05, 3), 'vol': 0.8},
  {'path': SFXB, 'file_dur': 1.5, 'a': 0, 'b': 1.4, 't': sh(13)['t'], 'vol': 0.9}]}
music = {'path': base + 'music/Investigations_bed.wav', 'file_dur': END + 0.1, 'segs': [{'a': 0, 'b': END, 't': 0, 'vol': 1.0}]}
spec = {'shots': shots, 'labels': labels, 'subs': subs, 'voice': voice,
        'voice_path': base + 'voices/EN_Andrew_hl2.mp3', 'voice_dur': 25.8,
        'logo': {'t': sh(3)['t'], 'dur': round(END - sh(3)['t'], 3)}, 'audio_tracks': [music, sfx]}
json.dump(spec, open('/home/claude/gen/spec_hl2.json', 'w'), indent=1, ensure_ascii=False)
for s in subs: print('%6.2f %5.2f %s' % (s['t'], s['dur'], s['text']))
for l in labels: print('LBL %6.2f %5.2f %s' % (l['t'], l['dur'], l['text']))
print('voice', [(v['t'], round(v['t'] + v['b'] - v['a'], 2)) for v in voice]); print('END', END, 'pony', pony_t)

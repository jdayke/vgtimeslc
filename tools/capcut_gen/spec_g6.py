import json, sys
MUSIC_DROP = float(sys.argv[3]) if len(sys.argv) > 3 else 51.94
exec(open('/home/claude/g6/plan.py').read().split("print('VO end'")[0])
FD = json.load(open(sys.argv[1])) if len(sys.argv) > 1 else {}
BRAND = sys.argv[2] if len(sys.argv) > 2 else 'LC'
C = '#2fa7ff' if BRAND == 'LC' else '#FD3737'
P = 'J:/Claude/VGTimes and LibertyCity/Footage/2026 11 05/rockstar_media/GTAVI_Screenshots/Places/'
REG = {'VC': 'Vice City/Vice_City_', 'LK': 'Leonida Keys/Leonida_Keys_', 'GR': 'Grassrivers/Grassrivers_', 'PG': 'Port Gellhorn/Port_Gellhorn_',
       'AM': 'Ambrosia/Ambrosia_', 'MK': 'Mount Kalaga National Park/Mount_Kalaga_National_Park_'}
CX = {'VC_10': 1840, 'VC_01': 1760, 'VC_13': 1920, 'VC_24': 1600, 'VC_05': 2240, 'VC_18': 1920, 'VC_27': 1920,
      'LK_01': 2600, 'LK_02': 1500, 'LK_05': 1920, 'LK_06': 1700, 'LK_04': 2300, 'LK_07': 2200,
      'GR_05': 2000, 'GR_04': 1700, 'GR_01': 2000, 'GR_08': 1900,
      'PG_06': 1920, 'PG_01': 1300, 'PG_04': 2600, 'PG_05': 1600,
      'AM_04': 1300, 'AM_02': 1920, 'AM_01': 2300, 'AM_03': 1920,
      'MK_04': 1840, 'MK_02': 1840, 'MK_03': 900, 'MK_06': 1920, 'MK_01': 1500}
def img(k): r, n = k.split('_'); return P + REG[r] + n + '.jpg'
# anchors: (start time, image key)
A = []
hook = ['VC_10', 'LK_01', 'GR_04', 'PG_01', 'AM_01', 'MK_04']
hs = wt('vice')
for i, k in enumerate(hook): A.append((round(i * hs / 6, 3), k))
A += [(wt('vice'), 'VC_01'), (wt('neon'), 'VC_13'), (wt('supercars'), 'VC_24'), (wt('beaches'), 'VC_05'), (wt('probably'), 'VC_18'),
      (wt('or'), 'LK_01'), (wt('disappear', 2), 'LK_02'), (wt('tropical'), 'LK_06'), (wt('boats'), 'LK_05'), (wt('diving'), 'LK_04'), (wt('dangerous') - 0.3, 'LK_07'),
      (wt('too'), 'GR_05'), (wt('go'), 'GR_04'), (wt('alligators'), 'GR_01'), (wt('worst') - 0.35, 'GR_08'),
      (wt('still'), 'PG_06'), (wt('port'), 'PG_01'), (wt('abandoned'), 'PG_04'), (wt('basically'), 'PG_05'),
      (wt('then'), 'AM_04'), (wt('sugar') - 0.2, 'AM_02'), (wt('biker') - 0.2, 'AM_01'), (wt('everything') - 0.2, 'AM_03'),
      (wt('or', 2), 'MK_04'), (wt('mt'), 'MK_02'), (wt('hunting'), 'MK_03'), (wt('fishing'), 'MK_06'), (wt('off'), 'MK_01')]
six = wt('six', 2)
fast = ['VC_27', 'LK_01', 'GR_05', 'PG_06', 'AM_04', 'MK_04']
for i, k in enumerate(fast): A.append((round(six + i * 0.36, 3), k))
fin = round(six + 6 * 0.36, 3)
A.append((fin, 'VC_01'))
END = round(VO_END + 1.6, 3)
shots = []
for i, (t0, k) in enumerate(A):
    t1 = A[i + 1][0] if i + 1 < len(A) else END
    n = 'G6_%02d' % (i + 1)
    shots.append({'name': n, 'key': k, 'img': img(k), 'cx': CX[k], 't': round(t0, 3), 'dur': round(t1 - t0, 3),
                  'path': 'J:/Claude/VGTimes and LibertyCity/Work/2026 11 13 GTA6 Regions/capcut_shots_v1/' + n + '.mp4',
                  'file_dur': FD.get(n, round(t1 - t0, 3) + 0.07), 'vol': 0.0, 'has_audio': False})
# fix tiny float gaps: make each shot end exactly at next start
for i in range(len(shots) - 1): shots[i]['dur'] = round(shots[i + 1]['t'] - shots[i]['t'], 3)
HOOK = {'fg': '#FFFFFF', 'bg': C, 'size': 8.0}
LAB = {'fg': '#FFFFFF', 'bg': C, 'size': 9.0}
TAG = {'fg': '#FFFFFF', 'bg': C, 'size': 6.5}
SUB = {'fg': C, 'bg': '#FFFFFF', 'size': 8.0}
def L(text, t0, t1, y, st, lane=1): return {'text': text, 't': round(t0, 3), 'dur': round(t1 - t0, 3), 'y': y, 'style': st, 'lane': lane}
r = lambda w, n=1: wt(w, n)
labels = [L('WHERE ARE YOU GOING FIRST', 0, hs, 0.62, HOOK), L('IN GTA 6?', 0, hs, 0.52, HOOK, 2),
  L('VICE CITY', r('vice'), r('or'), 0.72, TAG, 2), L('NEON', r('neon'), r('supercars'), 0.5, LAB), L('SUPERCARS', r('supercars'), r('beaches'), 0.5, LAB),
  L('BAD DECISIONS', r('probably'), r('or'), 0.5, LAB),
  L('LEONIDA KEYS', r('or'), r('too'), 0.72, TAG, 2), L('PARADISE?', r('tropical'), r('dangerous') - 0.3, 0.5, LAB), L('MAYBE NOT', r('dangerous') - 0.3, r('too'), 0.5, LAB),
  L('GRASSRIVERS', r('go'), r('still'), 0.72, TAG, 2), L("GATORS AREN'T", r('worst') - 0.35, r('still'), 0.55, LAB), L('THE WORST PART', r('worst') - 0.35, r('still'), 0.45, LAB, 3),
  L('PORT GELLHORN', r('port'), r('then'), 0.72, TAG, 2), L('THE FORGOTTEN COAST', r('cheap'), r('then'), 0.5, LAB),
  L('AMBROSIA', r('then'), r('or', 2), 0.72, TAG, 2), L('SUGAR', r('sugar') - 0.2, r('biker') - 0.2, 0.5, LAB), L('BIKERS', r('biker') - 0.2, r('everything') - 0.2, 0.5, LAB),
  L('WHAT COULD GO WRONG?', r('everything') - 0.2, r('or', 2), 0.5, LAB),
  L('MOUNT KALAGA', r('mt'), six, 0.72, TAG, 2), L('HUNTING', r('hunting'), r('fishing'), 0.5, LAB), L('FISHING', r('fishing'), r('off'), 0.5, LAB), L('OFF-ROAD', r('off'), six, 0.5, LAB),
  L('WHERE ARE YOU GOING FIRST?', fin, END, 0.12, dict(LAB, size=8.5)),
  L('VICE CITY • KEYS • GRASSRIVERS', fin, END, -0.02, dict(TAG, size=5.5), 2), L('PORT GELLHORN • AMBROSIA • KALAGA', fin, END, -0.10, dict(TAG, size=5.5), 3)]
# subtitles (skip the hook line and the closing question, which are on screen as labels)
chunks = [('GTA 6 GIVES YOU SIX', 'gta', 'six'), ('VERY DIFFERENT PLACES', 'very', 'places'), ('TO DISAPPEAR INTO', 'to', 'into'), ('SO WHERE ARE YOU GOING FIRST?', 'so', 'first'), ('VICE CITY?', 'vice', 'city'), ('NEON, SUPERCARS, BEACHES', 'neon', 'beaches'), ('AND PROBABLY THE FASTEST WAY', 'and', 'way'),
  ('TO LOSE ALL YOUR MONEY', 'to', 'money'), ('OR SKIP THE CITY COMPLETELY', 'or', 'completely'), ('AND DISAPPEAR INTO', 'and', 'into'), ('THE LEONIDA KEYS', 'the', 'keys'),
  ('TROPICAL ISLANDS', 'tropical', 'islands'), ('BOATS, DIVING', 'boats', 'diving'), ('AND SOME OF THE MOST', 'and', 'most'), ('DANGEROUS WATERS IN AMERICA', 'dangerous', 'america'),
  ('TOO RELAXING?', 'too', 'relaxing'), ('GO TO THE GRASSRIVERS', 'go', 'rivers'), ('WHERE ROCKSTAR SAYS', 'where', 'says'),
  ("THE ALLIGATORS AREN'T EVEN", 'the', 'even'), ('THE WORST PREDATORS', 'the', 'predators'), ('STILL TOO SAFE?', 'still', 'safe'),
  ('PORT GELLHORN', 'port', 'gellhorn'), ('CHEAP MOTELS', 'cheap', 'motels'), ('ABANDONED ATTRACTIONS', 'abandoned', 'attractions'), ('BASICALLY FLORIDA', 'basically', 'florida'),
  ('AFTER THE TOURISTS GAVE UP', 'after', 'up'), ("THEN THERE'S AMBROSIA", 'then', 'ambrosia'), ('WHERE A SUGAR REFINERY', 'where', 'refinery'),
  ('PROVIDES THE JOBS', 'provides', 'jobs'), ('AND A BIKER GANG PROVIDES', 'and', 'provides'), ('ALMOST EVERYTHING ELSE', 'almost', 'else'),
  ('OR FORGET', 'or', 'forget'), ('CIVILIZATION ENTIRELY', 'civilization', 'entirely'), ('MOUNT KALAGA', 'mt', 'calaga'), ('HUNTING. FISHING', 'hunting', 'fishing'), ('OFF-ROAD TRAILS', 'off', 'trails'),
  ('SIX PLACES', 'six', 'places'), ('ONE FIRST DESTINATION', 'one', 'destination'), ('WHERE ARE YOU GOING?', 'where', 'going')]
ws = [w.lower().strip('.,?').lstrip('-') for w, _, _ in words]
pos = 0; subs = []
for k, (txt, w0, w1) in enumerate(chunks):
    i = ws.index(w0, pos); j = ws.index(w1, i); pos = j + 1
    subs.append([txt, at(words[i][1]) - 0.05, at(words[j][2])])
for k in range(len(subs)):
    nxt = subs[k + 1][1] if k + 1 < len(subs) else END
    subs[k][2] = min(nxt, subs[k][2] + 0.45)
subs[-1][2] = END
subs = [{'text': (s[0].rstrip(',.') ), 't': round(s[1], 3), 'dur': round(s[2] - s[1], 3), 'y': -0.47, 'style': SUB} for s in subs]
voice = [{'a': a, 'b': b, 't': t} for a, b, t in pieces]
music = {'path': 'J:/Claude/VGTimes and LibertyCity/Work/2026 11 13 GTA6 Regions/music/ViceRemix_bed.wav', 'file_dur': END + 0.1, 'segs': [{'a': 0, 'b': END, 't': 0, 'vol': 1.0}]}
spec = {'shots': shots, 'labels': labels, 'subs': subs, 'voice': voice, 'voice_path': 'J:/Claude/VGTimes and LibertyCity/Work/2026 11 13 GTA6 Regions/voices/EN_Andrew_regions.mp3',
        'voice_dur': 48.384, 'logo': {'t': hs, 'dur': round(END - hs, 3)}, 'audio_tracks': [music],
        'logo_path': 'J:/Claude/VGTimes and LibertyCity/Graphics/' + ('LC 002.png' if BRAND == 'LC' else 'VG003.png'),
        'music_offset': round(MUSIC_DROP - six, 3), 'end': END}
json.dump(spec, open('/home/claude/g6/spec_g6_%s.json' % BRAND, 'w'), indent=1, ensure_ascii=False)
print('END', END, 'six', six, 'music offset', spec['music_offset'], 'shots', len(shots))
for s in shots: print(s['name'], s['key'], s['t'], s['dur'])
for s in subs: print('SUB %6.2f %5.2f %s' % (s['t'], s['dur'], s['text']))

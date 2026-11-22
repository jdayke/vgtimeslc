import json
W = json.load(open("/mnt/user-data/uploads/VGTimes and LibertyCity/Work/2026 11 13 GTA6 Regions/voices/EN_Andrew_regions_words.json"))
SIL = [(3.905625,4.274292),(5.361958,5.775375),(6.278042,6.662333),(7.9715,8.225875),(8.645167,8.976958),(11.223167,11.593),(13.053792,13.385208),(15.092958,15.499833),(16.349583,16.613708),(17.660125,17.96125),(20.071833,20.43375),(21.018833,21.403333),(22.424917,22.754875),(25.96675,26.376458),(27.05225,27.472833),(28.077917,28.477208),(30.509833,30.837292),(32.993792,33.406958),(34.303917,34.595542),(36.584667,36.893083),(39.075958,39.476792),(41.140042,41.517208),(42.123833,42.500833),(42.792583,43.216333),(43.516292,43.904917),(44.656833,45.062458),(45.6865,46.103542),(47.145833,47.535917)]
GAP = 0.18
# voice pieces between long silences; keep a slightly longer beat before region switches
BEAT = {20.071833: 0.30, 25.96675: 0.30, 32.993792: 0.25, 39.075958: 0.30, 44.656833: 0.30}
pieces = []; a = 0.10; t = 0.20
for s0, s1 in SIL:
    b = s0 + 0.03
    pieces.append((round(a, 3), round(b, 3), round(t, 3)))
    t += (b - a) + BEAT.get(s0, GAP)
    a = s1 - 0.03
pieces.append((round(a, 3), 48.10, round(t, 3))); t += 48.10 - a
def at(x):
    for pa, pb, pt in pieces:
        if pa - 0.06 <= x <= pb + 0.06: return pt + (x - pa)
    for pa, pb, pt in pieces:  # inside a removed pause -> start of the next piece
        if x < pa: return pt
    return pieces[-1][2] + pieces[-1][1] - pieces[-1][0]
words = [(w['w'].strip(), w['s'], w['e']) for w in W]
def wt(word, n=1):
    k = 0
    for w, s, e in words:
        if w.lower().strip('.,?') == word.lower():
            k += 1
            if k == n: return round(at(s), 3)
    raise Exception(word)
def we(word, n=1):
    k = 0
    for w, s, e in words:
        if w.lower().strip('.,?') == word.lower():
            k += 1
            if k == n: return round(at(e), 3)
VO_END = round(t, 3)
print('VO end', VO_END)
json.dump({'pieces': pieces, 'vo_end': VO_END}, open('/home/claude/g6/vo.json', 'w'))

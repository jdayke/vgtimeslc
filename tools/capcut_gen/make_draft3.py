# v3: label lanes 1..N, logo_path (LC/VGT), dynamic track indexes. Usage as make_draft.py.
import json, copy, uuid, os, sys, time
TPL = "/mnt/user-data/uploads/CapCut Drafts/VGT GTA 6 30 FPS v1"
OUTDIR = sys.argv[1]; NAME = sys.argv[2]; SPEC = json.load(open(sys.argv[3]))
d = json.load(open(os.path.join(TPL, "draft_content.json"), encoding="utf-8"))
U = lambda: str(uuid.uuid4()).upper()
M = {}
for k, v in d['materials'].items():
    if isinstance(v, list):
        for m in v: M[m['id']] = (k, m)
tpl = {'shot': d['tracks'][0]['segments'][0], 'text': d['tracks'][2]['segments'][0],
       'logo': d['tracks'][3]['segments'][0], 'voice': d['tracks'][4]['segments'][0]}
tpl_tracks = {'video': d['tracks'][0], 'text': d['tracks'][2], 'audio': d['tracks'][4]}
for k, v in d['materials'].items():
    if isinstance(v, list): d['materials'][k] = []
us = lambda x: int(round(x * 1e6))
def clone(seg_key, material_patch, seg_patch):
    s = copy.deepcopy(tpl[seg_key]); s['id'] = U()
    k, m = M[s['material_id']]; m = copy.deepcopy(m); m['id'] = U(); m.update(material_patch)
    d['materials'][k].append(m); s['material_id'] = m['id']
    refs = []
    for r in s['extra_material_refs']:
        rk, rm = M[r]; rm = copy.deepcopy(rm); rm['id'] = U(); d['materials'][rk].append(rm); refs.append(rm['id'])
    s['extra_material_refs'] = refs
    for kk, vv in seg_patch.items(): s[kk] = vv
    return s, m
def track(kind, segs, idx, flag=0):
    t = copy.deepcopy(tpl_tracks[kind]); t['id'] = U(); t['segments'] = segs; t['flag'] = flag
    for s in segs: s['track_render_index'] = idx
    return t
tracks = []
# main shots
segs = []
for sh in SPEC['shots']:
    s, m = clone('shot', {'path': sh['path'], 'material_name': os.path.basename(sh['path']), 'duration': us(sh['file_dur']),
                          'has_audio': sh.get('has_audio', True), 'local_material_id': str(uuid.uuid4())},
                 {'target_timerange': {'start': us(sh['t']), 'duration': us(sh['dur'])},
                  'source_timerange': {'start': 0, 'duration': us(sh['dur'])}, 'volume': sh.get('vol', 1.0), 'last_nonzero_volume': 1.0,
                  'render_index': 0})
    segs.append(s)
tracks.append(track('video', segs, 0))
def text_track(items, idx, rbase):
    segs = []
    for it in items:
        st = it['style']
        fill = [int(st['fg'][i:i+2], 16) / 255 for i in (1, 3, 5)]
        content = {"text": it['text'], "styles": [{"fill": {"content": {"render_type": "solid", "solid": {"color": fill}}},
                   "font": {"path": "C:/Users/jdayk/AppData/Local/Microsoft/Windows/Fonts/20784.ttf", "id": ""},
                   "size": st['size'], "range": [0, len(it['text'])]}]}
        s, m = clone('text', {'content': json.dumps(content, ensure_ascii=False), 'text_color': st['fg'], 'background_color': st['bg'],
                              'font_size': st['size']},
                     {'target_timerange': {'start': us(it['t']), 'duration': us(it['dur'])}, 'render_index': rbase})
        s['clip']['transform'] = {'x': 0.0, 'y': it['y']}
        segs.append(s)
    return track('text', segs, idx)
lanes = sorted({x.get('lane', 1) for x in SPEC['labels']})
for li, ln in enumerate(lanes):
    tracks.append(text_track([x for x in SPEC['labels'] if x.get('lane', 1) == ln], 1 + li, 14002 + li))
tracks.append(text_track(SPEC['subs'], 1 + len(lanes), 14001))
# logo
lg = SPEC['logo']
s, m = clone('logo', ({'path': SPEC['logo_path'], 'material_name': os.path.basename(SPEC['logo_path'])} if 'logo_path' in SPEC else {}), {'target_timerange': {'start': us(lg['t']), 'duration': us(lg['dur'])},
                          'source_timerange': {'start': 0, 'duration': us(lg['dur'])}})
lt = copy.deepcopy(d['tracks'][3]); lt['id'] = U(); lt['segments'] = [s]; s['track_render_index'] = len(tracks)
tracks.append(lt)
# voice
segs = []
for p in SPEC['voice']:
    s, m = clone('voice', {'path': SPEC['voice_path'], 'name': os.path.basename(SPEC['voice_path']), 'duration': us(SPEC['voice_dur']),
                           'local_material_id': str(uuid.uuid4()), 'unique_id': uuid.uuid4().hex},
                 {'target_timerange': {'start': us(p['t']), 'duration': us(p['b'] - p['a'])},
                  'source_timerange': {'start': us(p['a']), 'duration': us(p['b'] - p['a'])}, 'volume': 1.5, 'last_nonzero_volume': 1.5})
    segs.append(s)
tracks.append(track('audio', segs, len(tracks)))
# extra audio tracks (music bed, sfx)
for k, at in enumerate(SPEC.get('audio_tracks', [])):
    segs = []
    for p in at['segs']:
        s, m = clone('voice', {'path': at['path'] if 'path' in at else p['path'], 'name': os.path.basename(p.get('path', at.get('path'))), 'duration': us(p.get('file_dur', at.get('file_dur'))),
                               'local_material_id': str(uuid.uuid4()), 'unique_id': uuid.uuid4().hex},
                     {'target_timerange': {'start': us(p['t']), 'duration': us(p['b'] - p['a'])},
                      'source_timerange': {'start': us(p['a']), 'duration': us(p['b'] - p['a'])}, 'volume': p['vol'], 'last_nonzero_volume': p['vol']})
        if 'path' in p: m['path'] = p['path']
        segs.append(s)
    tracks.append(track('audio', segs, len(tracks)))
d['tracks'] = tracks
total = max(sh['t'] + sh['dur'] for sh in SPEC['shots'])
d['duration'] = us(total)
tid = U(); d['id'] = tid; d['name'] = ''
now = int(time.time() * 1e6)
d['create_time'] = now // 1000000; d['update_time'] = now // 1000000
os.makedirs(os.path.join(OUTDIR, 'Timelines', tid), exist_ok=True)
txt = json.dumps(d, ensure_ascii=False, separators=(',', ':'))
for p in [os.path.join(OUTDIR, 'draft_content.json'), os.path.join(OUTDIR, 'Timelines', tid, 'draft_content.json')]:
    open(p, 'w', encoding='utf-8').write(txt)
proj = json.load(open(os.path.join(TPL, 'project.json')))
proj.update({'create_time': now, 'update_time': now, 'id': U(), 'main_timeline_id': tid,
             'timelines': [{'create_time': now, 'id': tid, 'is_marked_delete': False, 'name': 'Timeline 01', 'update_time': now}]})
for p in [os.path.join(OUTDIR, 'project.json'), os.path.join(OUTDIR, 'Timelines', 'project.json')]:
    json.dump(proj, open(p, 'w'), separators=(',', ':'))
lay = {"dockItems": [{"dockIndex": 0, "ratio": 1, "timelineIds": [tid], "timelineNames": ["Timeline 01"]}], "layoutOrientation": 1}
json.dump(lay, open(os.path.join(OUTDIR, 'timeline_layout.json'), 'w'), separators=(',', ':'))
meta = json.load(open(os.path.join(TPL, 'draft_meta_info.json'), encoding='utf-8'))
meta.update({'draft_fold_path': 'J:/CapCut/CapCut Drafts/' + NAME, 'draft_id': U(), 'draft_name': NAME, 'tm_duration': us(total),
             'draft_timeline_materials_size_': len(txt.encode('utf-8')), 'tm_draft_create': now, 'tm_draft_modified': now})
json.dump(meta, open(os.path.join(OUTDIR, 'draft_meta_info.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
st = open(os.path.join(TPL, 'draft_settings')).read().replace('1794328643', str(now // 1000000))
open(os.path.join(OUTDIR, 'draft_settings'), 'w', newline='').write(st)
open(os.path.join(OUTDIR, 'draft_agency_config.json'), 'w').write(open(os.path.join(TPL, 'draft_agency_config.json')).read())
print('ok', tid, total, len(txt))

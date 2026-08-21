import json, glob, pathlib
recs=[]
for f in sorted(glob.glob('data/records/*.json')):
    d=json.load(open(f))
    recs += d if isinstance(d, list) else d.get('competitors', [])
seen={}
for r in recs: seen[r['id']]=r
out=sorted(seen.values(), key=lambda r: r['name'].lower())
pathlib.Path('data/competitors.json').write_text(json.dumps(out, ensure_ascii=False, indent=1))
print(f'merged {len(out)} competitors from {len(glob.glob("data/records/*.json"))} record files')

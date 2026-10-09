import json
from pathlib import Path
root=Path(__file__).resolve().parent
load=lambda p:json.loads((root/p).read_text(encoding='utf8'))
a=load('data/actors.json');c=load('data/claims.json');e=load('data/evidence.json');r=load('data/relations.json');s=load('data/sources.json');t=load('config/taxonomy.json');syn=load('data/synthesis.json');m=load('data/meta.json')
ids=[x['id'] for x in a];assert len(ids)==len(set(ids)),'IDs dupliqués'
A=set(ids);E={x['id'] for x in e};S={x['id'] for x in s}
assert m['id'] in A
assert len(a)==58 and len(c)==34 and len(r)==88 and len(e)==34
assert sum(x.get('display_in_cards',True) for x in a)==34
for x in a:assert all(y in t['categories'] for y in x['categories'])
for x in c:assert x['subject_id'] in A and set(x.get('evidence_ids',[]))<=E and x['value'] in t['stances']
for x in e:assert x.get('source_id') is None or x['source_id'] in S
for x in r:assert x['source_id'] in A and x['target_id'] in A and x['type'] in t['relation_types'] and set(x.get('evidence_ids',[]))<=E
assert len(syn['griefs'])==11 and len(syn['vigilance'])==15 and len(syn['sources'])==14
print(f"OK — {len(a)} nœuds, {len(c)} fiches, {len(r)} liens, {len(e)} preuves, {len(s)} sources et 3 onglets")

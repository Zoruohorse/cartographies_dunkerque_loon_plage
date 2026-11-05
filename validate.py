#!/usr/bin/env python3
"""Contrôle non rigidifié pour mises à jour par lot, sans masquer les sources historiques non qualifiées."""
import json
from pathlib import Path
root=Path(__file__).resolve().parent
load=lambda p:json.loads((root/p).read_text(encoding='utf8'))
a=load('data/actors.json');c=load('data/claims.json');e=load('data/evidence.json');r=load('data/relations.json');s=load('data/sources.json');t=load('config/taxonomy.json');syn=load('data/synthesis.json');m=load('data/meta.json')
errors=[];warnings=[]
for k,seq in [('actors',a),('claims',c),('evidence',e),('relations',r),('sources',s)]:
 ids=[x.get('id') for x in seq]
 if len(ids)!=len(set(ids)):errors.append('IDs dupliqués : '+k)
A={x['id'] for x in a};E={x['id'] for x in e};S={x['id'] for x in s}
if m['id'] not in A:errors.append('Projet métadonnées introuvable')
for x in a:
 if any(y not in t['categories'] for y in x['categories']):errors.append('Catégorie hors taxonomie : '+x['id'])
for x in c:
 if x['subject_id'] not in A or x['project_id'] not in A:errors.append('Acteur manquant : '+x['id'])
 if x['value'] not in t['stances'] or x['certainty'] not in t['certainty_levels']:errors.append('Position ou certitude non conforme : '+x['id'])
 if not x.get('evidence_ids') or not set(x['evidence_ids'])<=E:errors.append('Preuve de position absente : '+x['id'])
for x in e:
 if x.get('source_id') and x['source_id'] not in S:errors.append('Source non résolue : '+x['id'])
 if not x.get('source_id'):warnings.append('Preuve ancienne sans source : '+x['id'])
for x in r:
 if x['source_id'] not in A or x['target_id'] not in A:errors.append('Extrémité inconnue : '+x['id'])
 if x['type'] not in t['relation_types']:errors.append('Relation hors taxonomie : '+x['id'])
 if not set(x.get('evidence_ids',[]))<=E:errors.append('Preuve de relation cassée : '+x['id'])
 if not x.get('evidence_ids'):warnings.append('Relation sans preuve : '+x['id'])
for x in s:
 if x.get('status')=='qualified' and not (x.get('url') or '').startswith(('https://','http://')):errors.append('Source qualifiée sans URL : '+x['id'])
if errors:raise SystemExit('ÉCHEC — '+'; '.join(errors))
print(f"OK STRUCTURE — {len(a)} nœuds, {len(c)} fiches, {len(r)} liens, {len(e)} preuves, {len(s)} sources, {len(syn['griefs'])} griefs, {len(syn['vigilance'])} vigilances")
print(f"SOURCES QUALIFIÉES : {sum(bool(x.get('url')) for x in s)} / {len(s)}")
print(f"AVERTISSEMENTS NON BLOQUANTS : {len(warnings)} ; voir :")
for w in warnings[:12]:print(' -',w)
if len(warnings)>12:print(f' - ... et {len(warnings)-12} autres avertissements')

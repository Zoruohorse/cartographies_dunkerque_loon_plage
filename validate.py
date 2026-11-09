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


# Extension : traçabilité du nouvel onglet « Évolution des acteurs ».
from datetime import date
from urllib.parse import urlsplit

timeline=load('data/timeline.json')
T={x['id']:x for x in timeline}
if len(T)!=len(timeline):errors.append('Évolution : IDs d’événement dupliqués')
actorIds=[x['actor_id'] for x in timeline]
if len(actorIds)!=len(set(actorIds)):errors.append('Évolution : acteur compté plusieurs fois')
config=t.get('timeline',{})
kind={x['id'] for x in config.get('categories',[])}
direct=indirect=0
for item in timeline:
 if item['actor_id'] not in A:errors.append('Évolution : acteur inconnu '+item['id'])
 if item.get('event_type')!='first_documented_appearance':errors.append('Évolution : mauvais type '+item['id'])
 if item.get('category') not in kind:errors.append('Évolution : typologie absente '+item['id'])
 if item.get('status')!='confirmed':errors.append('Évolution : statut incomplet '+item['id'])
 if item.get('scope')=='direct':direct+=1
 elif item.get('scope')=='indirect':indirect+=1
 else:errors.append('Évolution : périmètre absent '+item['id'])
 try:
  dt=date.fromisoformat(item['date'])
  if dt>date(2026,11,9) or item.get('date_precision')!='day':errors.append('Évolution : date future/imprécise '+item['id'])
 except (ValueError,TypeError):
  errors.append('Évolution : date mal formée '+item['id'])
 if not item.get('source_ids') or not item.get('evidence_ids'):errors.append('Évolution : preuve absente '+item['id'])
 for sid in item.get('source_ids',[]):
  src=next((x for x in s if x['id']==sid),None)
  if not src or urlsplit(src.get('url') or '').scheme!='https':errors.append('Évolution : URL invalide '+item['id'])
 for eid in item.get('evidence_ids',[]):
  if eid not in E:errors.append('Évolution : preuve cassée '+item['id'])

html=(root/'apps/cards/index.html').read_text(encoding='utf-8')
for tab in ('carto','griefs','watch','evolution'):
 if f'data-tab="{tab}"' not in html or f'id="tab-{tab}"' not in html:errors.append('Onglet introuvable : '+tab)
if len(timeline)!=41 or direct!=23 or indirect!=18:errors.append('Répartition inattendue du jeu d’entrée 2026-11-09')
for path in ('assets/js/evolution.js','assets/css/evolution.css'):
 if not (root/path).is_file():errors.append('Fichier évolution manquant : '+path)
loader=(root/'assets/js/data-loader.js').read_text(encoding='utf-8')
if 'timeline:"data/timeline.json"' not in loader:errors.append('Chargeur non relié à data/timeline.json')
if errors:raise SystemExit('ÉCHEC ÉVOLUTION — '+'; '.join(errors))
print(f'ÉVOLUTION OK — {direct} acteurs directs, {indirect} de contexte, 4 onglets, sources reliées.')

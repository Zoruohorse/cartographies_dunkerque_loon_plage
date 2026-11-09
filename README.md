# Cartographie des acteurs — Dunkerque / Loon-Plage

Adaptation du **moteur visuel et physique de Fouju**, basée sur les deux fichiers de code source Dunkerque / Loon-Plage transmis.

- `apps/network/` : vue relationnelle, forces, couleurs par catégorie, liens courbes, zoom, déplacements, panneau acteurs/relations, filtres ; scripts et styles de Fouju réutilisés.
- `apps/cards/` : fiches acteurs, filtres, fenêtre documentaire et deux onglets supplémentaires : synthèse des oppositions et points de vigilance/sources.
- `data/` : référentiel JSON commun aux deux vues ; `synthesis.json` reprend les 11 griefs, 15 vigilances et 14 sources transmis.
- `config/taxonomy.json` : taxonomie Fouju étendue aux thèmes énergie, vigilance et médias.

## Mise en ligne GitHub Pages

1. Créer un dépôt et charger **tous les fichiers et dossiers de l'archive à la racine** (ne pas charger le ZIP seul).
2. `Settings → Pages → Deploy from a branch → main → /(root)`.
3. Attendre la publication automatique puis ouvrir la page du dépôt ; accès direct à `apps/cards/` et `apps/network/`.

## Vérification locale

```bash
python3 -m http.server 8000
```

Ouvrir `http://localhost:8000/` : les données ne peuvent pas être chargées directement par `file://` à cause des requêtes `fetch`.

```bash
python3 validate.py
```

## Périmètre et fiabilité

- 54 nœuds et 84 liens du réseau initial, complétés par 4 acteurs apparaissant uniquement dans les fiches (État, CRE, Roland Lescure, Legrand), liés uniquement par des mentions déjà présentes dans leurs fiches.
- 34 fiches d'acteurs et 34 synthèses de preuves récupérées du tableau de fiches fourni. Les nœuds « source », « vigilance » et « projet » ne sont pas présentés comme des acteurs dans la grille des fiches.
- **Les champs `evidence.text` reprennent les formulations du corpus transmis ; ils ne sont pas systématiquement des citations littérales.** Les URL d'articles absentes n'ont pas été inventées et restent à qualifier.
- Certains liens du nuage sont purement thématiques : les flèches visuelles ne constituent pas une preuve de partenariat commercial.


## Onglet Évolution des acteurs — 9 novembre 2026

Quatrième onglet de la vue cartes : 41 acteurs datés sur les 68 entités, dont 23 rattachés au dossier de Loon-Plage et 18 acteurs du contexte industriel ou sectoriel. Le graphique est limité au **Projet Loon-Plage** par défaut ; un bouton donne accès au périmètre élargi. Les modes « Nouveaux / Cumulés », la ventilation mensuelle, les typologies et les sources cliquables reprennent le modèle Fouju/Bosquel.

Les sources datent une **première apparition documentaire dans le corpus**, pas une première prise de position. Les textes des associations FNE et Amis de la Terre parlent de recours *envisagés*, pas déposés. Les partenaires d'autres projets (EDF à Bouchain, Sesterce au Bosquel, Bull à Angers) et les industriels régionaux (Foselev, Brookfield, Legrand) sont seulement contextuels.

Fichiers : `data/timeline.json`, `config/taxonomy.json`, `assets/js/evolution.js` et `assets/css/evolution.css`. Audit : `data/evolution-audit-20261109.json`. Les fiches, positions et relations initiales demeurent inchangées.

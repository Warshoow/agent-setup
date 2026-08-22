---
name: audit-360
description: "Audit 360° d'un codebase en passes à périmètre exclusif (code, sécurité, produit, architecture, prod-readiness), findings vérifiés par le code. Modes : full | delta."
argument-hint: "full | delta"
disable-model-invocation: true
---

# Audit 360°

Audit de qualité read-only d'un codebase. Le livrable est un **rapport** (`AUDIT.md`), pas des fixes. La qualité de l'audit tient d'abord aux quatre règles ci-dessous, plus qu'à l'outillage.

## Les quatre règles

1. **Découper par dimension, pas par fichier.** Des passes indépendantes, chacune avec un seul angle de lecture. Un lecteur qui cherche *tout à la fois* rate tout ; un lecteur qui cherche *une seule classe de problème* la voit partout. **Les passes ne se re-signalent pas mutuellement** : dire explicitement à chacune ce que couvrent les autres.
2. **Vérifié ou rien.** Un finding n'existe que confirmé par lecture du code, avec `fichier:ligne` et un **scénario d'échec concret** (entrées/état → comportement erroné). Interdits : conseils génériques sans citation, « il faudrait probablement », findings déduits d'un nom de fichier non lu. Une **absence** (« pas de rate limiting ») se vérifie par recherche (grep des libs/patterns candidats) avant d'être affirmée.
3. **Read-only.** L'audit ne modifie rien.
4. **Noter aussi ce qui est bien fait.** Une courte section « points forts vérifiés » par dimension : elle calibre la confiance du lecteur et évite qu'un futur fix casse un mécanisme correct.

## Couverture adjacente — ne pas re-signaler

- **ponytail (`/ponytail-audit`)** couvre l'**over-engineering** et le **dead-code**. S'il est lancé en parallèle de cet audit, les passes le traitent comme une dimension déjà couverte : elles ne re-signalent ni sur-ingénierie, ni flexibilité spéculative, ni code mort. (S'il n'est PAS lancé, ces points restent dans le périmètre de la passe code — pour le dead-code — et architecture — pour la généralité spéculative.)
- **Problèmes déjà trackés** : lister explicitement le bloc `KNOWN_ISSUES` avec la consigne *do NOT re-report* — sinon chaque passe gaspille son budget à redécouvrir l'existant.

## 1. Contexte (à constituer AVANT de lancer les passes)

Constituer le **bloc de contexte** commun, injecté dans chaque prompt de passe :

- **Stack** : langages, frameworks, DB, queue, intégrations externes (1-3 lignes).
- **Carte du code** : répertoires clés + les 5-10 fichiers les plus importants par domaine (routes, services, config, entrypoints, hooks front). Un `ls` des dossiers `api/`/`services/`/équivalents suffit.
- **Docs internes** : les fichiers à lire d'abord (README, CLAUDE.md, docs/, specs).
- **Known issues** : les problèmes déjà connus/trackés + ponytail si lancé (voir *Couverture adjacente*).
- **Données réelles** si connues (ex. « une playlist réelle de 3 570 vidéos existe ») : les échelles réelles transforment un finding théorique en scénario concret.

## 2. Les cinq passes

Cinq dimensions, **périmètres exclusifs**, chacune résolue par un sous-agent :

- **code** → [`passes/code.md`](passes/code.md)
- **sécurité** → [`passes/security.md`](passes/security.md)
- **produit / features** → [`passes/product.md`](passes/product.md)
- **architecture / structure** → [`passes/architecture.md`](passes/architecture.md)
- **prod-readiness (SaaS)** → [`passes/saas.md`](passes/saas.md)

**Dispatch.** Lancer les cinq **en parallèle** si l'outillage le permet (sous-agents), sinon **séquentiellement** — même résultat, seul le temps change. Chaque sous-agent reçoit un prompt assemblé ainsi :

```
[rôle + read-only]
+ [le bloc de contexte du §1]
+ [le brief de la passe, lu depuis passes/<dim>.md]
+ [périmètre : CETTE dimension SEULEMENT ; les autres + ponytail sont couvertes ailleurs]
+ [le contrat de finding du §3 + le budget de findings]
```

Le **budget de findings** (10-25 max selon la passe, « skip nitpicks ») est essentiel : sans plafond, le rapport se dilue dans le style et le naming.

## 3. Contrat de finding (sortie de chaque passe)

```
**{ID} — {défaut en une phrase}.**
{fichier:ligne(s)} — {mécanisme}. Scénario : {entrées/état concret} → {conséquence}.
[Fix : {une ligne, optionnel}]
```

- **Sévérité** : `critique/élevé` (perte de données, prise de compte, coût incontrôlé, feature cassée en usage réel) · `moyen` (casse dans des conditions plausibles, dette bloquante) · `faible` (défense en profondeur, polish).
- **ID préfixé par dimension** → référençable dans les commits de fix : `C` = code, `S` = sécurité, `L` = logique produit, `A` = architecture, `SA` = saas.

## 4. Synthèse (le travail de l'orchestrateur)

Une fois les cinq rapports reçus :

1. **Dédupliquer inter-passes.** Les recoupements sont normaux (un CORS `*` sort en sécu ET en saas ; un couplage sort en code ET en architecture). Garder le finding dans sa dimension la plus naturelle, le mentionner d'une ligne ailleurs (« = C3, vu côté architecture »).
2. **Chercher les causes racines** : si 3-4 findings partagent un même mécanisme (ex. une machine à états à moitié implémentée, ou aucune couture entre domaine et persistance), le dire explicitement — c'est l'info la plus actionnable, car un seul chantier corrige plusieurs findings.
3. **Rédiger un TLDR** en tête : verdict global honnête (y compris ce qui est sain), puis les 3-4 problèmes structurants.
4. **Prioriser en lots** : 4-5 lots ordonnés par rapport coût/impact, regroupés par cause racine plutôt que par sévérité brute. Signaler à part les **quick-wins** (fort impact, faible effort).
5. **Livrable** : un `AUDIT.md` **daté (branche + commit)**, findings en cases à cocher `- [ ]` pour suivre les fixes. Le commit dans l'en-tête est la **baseline** du mode delta — ne pas l'omettre.

## Modes

Le mode arrive en argument (`full` par défaut).

### `full`

Audit global : le flow complet ci-dessus (§1 → passes → §4). Auditer le **système**, pas le diff.

### `delta`

Audit de **maintenance** : n'auditer que ce qui a bougé depuis le dernier `AUDIT.md`. À réserver à ce cas — auditer le diff *à la place* du système reste un anti-pattern pour un audit global (voir §5).

1. **Baseline** : lire le commit enregistré dans l'en-tête du dernier `AUDIT.md`.
2. **Surface** : `git diff <baseline>..HEAD` donne les fichiers changés — mais scoper chaque passe au diff **+ son rayon d'impact** (appelants/appelés/dépendants du code modifié), jamais au diff brut seul. Un changement se juge avec ce qu'il touche autour, sinon on retombe dans l'anti-pattern « auditer le diff ». Les passes **architecture** et **saas** sont moins diff-locales : pour elles, chercher surtout si le changement *introduit* un problème structurel/ops nouveau ou *aggrave* un existant.
3. **Re-vérifier l'existant** : pour chaque finding encore ouvert (`- [ ]`) du rapport précédent, vérifier si le code cité a changé et s'il est réellement corrigé ; vérifier qu'un finding coché (`- [x]`) n'a pas régressé.
4. **Mettre à jour `AUDIT.md`** : nouvelle date + commit, findings résolus cochés, nouveaux findings ajoutés (les IDs continuent la numérotation), suivi préservé.

## 5. Anti-patterns (ce qui rend un audit inutile)

- **Findings non cités** : « le error handling pourrait être amélioré » — poubelle. Pas de `fichier:ligne` + scénario = pas de finding.
- **Affirmer une absence sans avoir cherché** (« pas de tests » alors que `tests/` existe).
- **Re-reporter les problèmes déjà connus** — d'où le bloc `KNOWN_ISSUES` obligatoire.
- **Le rapport-catalogue** : 60 findings non hiérarchisés valent moins que 20 triés avec causes racines.
- **Confondre les dimensions** : la passe sécu qui fait du style, la passe code qui fait du produit — chaque passe refuse explicitement ce qui n'est pas son périmètre.
- **Auditer le diff au lieu du système** pour un audit global (l'inverse — le mode `delta` — est fait pour la maintenance ; ne pas les confondre).

## 6. Adaptations au contexte (branches)

- **Avec orchestration multi-agents** (Claude Code : outil Agent/Task) : les cinq passes en parallèle en background, chaque agent reçoit son brief + le contexte du §1 ; l'orchestrateur ne fait que le §1 et le §4.
- **Sans multi-agents / session unique** : les cinq passes séquentiellement, dans des conversations séparées (ou après un clear de contexte) — une passe polluée par la précédente perd son angle de lecture. Écrire le rapport de chaque passe dans un fichier avant de passer à la suivante.
- **Avec un modèle plus faible** : découper chaque passe en sous-passes plus étroites (« audit code de `app/services/scan_*` uniquement », « pour chaque endpoint de `app/api/videos.py`, vérifier le filtre ownership ») ; rendre les checklists **mécaniques** (« pour chaque valeur de l'enum Status, grep les ÉCRITURES ; liste celles jamais écrites » plutôt que « cherche les trous de machine à états ») ; exiger la **citation avant le finding** (« d'abord colle les lignes, puis énonce le défaut ») ; ajouter une passe de **contre-vérification** (re-soumettre chaque finding à une session vierge : « essaie de réfuter ce finding en lisant le code cité », ne garder que les survivants — utile aussi avec un bon modèle sur les findings incertains) ; réduire le budget (8-10 findings max, sévérité élevée d'abord).
- **Projet non-SaaS** : remplacer la passe prod-readiness par l'équivalent du contexte cible — « CLI-readiness » (packaging, versions, messages d'erreur), « lib-readiness » (API publique, semver, docs), « interne-entreprise » (SSO, audit trail, déploiement maison).

---
name: checkpoint
description: "Tient à jour un fichier maître d'avancement dans le repo pour reprendre le travail dans une session neuve. Modes : update | resume | init."
argument-hint: "update | resume | init"
disable-model-invocation: true
---

# Checkpoint

Un **checkpoint** est un point de sauvegarde du travail, posé sur disque dans le repo, d'où une session neuve repart sans coût de démarrage à froid. La fenêtre de contexte est finie ; ce fichier est la mémoire de travail durable qui lui survit.

Règle fondatrice — **l'index est un index, pas un magasin.** Le fichier maître résume et pointe ; il ne recopie jamais ce qui vit déjà ailleurs (commits, diff, specs, ADRs, tickets). Chaque info a **une seule source de vérité** : le git est la vérité du code, le checkpoint pointe dessus.

## L'artefact

Un dossier dans le repo (par défaut `.checkpoint/`, mais peu importe — s'il en existe déjà un, réutilise-le) qui contient :

- **`INDEX.md`** — le seul fichier lu à chaque session. Petit, survolable d'un coup d'œil.
- **`<zone>.md`** — un fichier de détail par zone (feature, partie de l'app, workstream), lu **à la demande** quand une tâche touche cette zone.

Au début, tout tient dans `INDEX.md` seul. On ne crée des fichiers de zone que quand le découpage se justifie (voir *Découper*).

### Forme de `INDEX.md`

```markdown
# Checkpoint — <projet>

## Objectif
<1-2 lignes : où va cet effort. Chaque session s'y réoriente avant de choisir un item.>

## Position actuelle
<le prochain item à traiter, et le fichier de zone à charger pour le faire. Une ligne.>

## Zones
<!-- l'index : une ligne par zone, son état, son lien. Le détail vit dans le fichier de zone, pas ici. -->
- [<zone>](./<zone>.md) — <état en une ligne : done / en cours / à faire> — <prochain point si pertinent>

## Questions ouvertes
<décisions non tranchées qui bloquent ou orientent la suite. Vide si aucune.>
```

Tant que l'effort est petit, la section **Zones** peut porter directement les items cochables (`- [x]` / `- [ ]`) au lieu de pointer vers des fichiers. Le découpage vient plus tard.

### Forme de `<zone>.md`

```markdown
# <zone>

## Items
- [x] <point comblé>
- [ ] <point restant>

## Journal
<!-- notes brèves, du plus récent au plus ancien. Référence, ne recopie pas. -->
- <date/commit> — <1-2 phrases : ce qui a été fait, + chemins/SHA/tests concernés>
```

## Discipline anti-gonflement

C'est le cœur du skill — sans ça, le fichier maître pourrit.

- **Note brève, référence plutôt que recopie.** Chaque entrée de journal fait 1-2 phrases et **pointe** vers les artefacts (SHA de commit, chemin de fichier, nom de test, URL de ticket). Jamais de diff, de bloc de code, ni de spec recopiés — ça vit déjà ailleurs.
- **L'index ne stocke rien du détail d'une zone découpée.** Une fois une zone extraite dans son fichier, l'entrée d'index se réduit à un résumé d'une ligne + le lien. Une info dans un seul endroit.
- **Élague.** Quand un point est comblé *et* que son journal n'informe plus la suite, résume-le en une ligne ou supprime-le. Le journal garde ce qui oriente le travail à venir, pas l'historique complet (le git l'a déjà).

## Découper

Découpe **par zone** (couture naturelle), pas par taille brute — pour qu'une tâche future ne charge que son fichier.

Le signal pour découper : `INDEX.md` ne se survole plus d'un coup d'œil, **ou** une zone a accumulé assez d'items/de journal pour tenir seule. Alors :

1. Crée `<zone>.md`, déplaces-y les items et le journal de cette zone.
2. Réduis l'entrée de cette zone dans `INDEX.md` à un résumé d'une ligne + le lien.
3. Vérifie qu'aucun détail déplacé ne reste dupliqué dans l'index.

Ne pré-découpe pas une zone encore floue ou minuscule : inline tant que ça se survole, extrais quand ça déborde.

## Modes

Le mode arrive en argument. Sans argument, déduis-le : un fichier de checkpoint absent → `init` ; présent → `update`.

### `init`

Amorce le checkpoint. Point de départ courant : un fichier d'audit ou une liste de points d'évolution existante.

1. Repère le dossier `.checkpoint/` (crée-le sinon).
2. S'il existe déjà un fichier d'audit / de points, aspire ses points dans `INDEX.md` (section Zones, items cochables). Sinon, dresse la liste depuis l'état courant de la conversation.
3. Renseigne Objectif et Position actuelle. Terminé quand `INDEX.md` existe et liste les items à combler.

### `update`

À invoquer quand le travail a avancé — un item terminé, une étape risquée en vue, ou un palier de tokens atteint.

1. Coche les items comblés dans la bonne section/fichier de zone.
2. Ajoute au journal une note **brève et référencée** de ce qui vient d'être fait.
3. Mets à jour **Position actuelle** et **Questions ouvertes**.
4. Applique la *Discipline anti-gonflement* et, si le signal est là, *Découpe*.
5. **Rends un prompt de reprise** (voir plus bas).

Terminé quand : chaque avancement de la session est reflété, l'index se survole toujours d'un coup d'œil, et le prompt de reprise est produit.

### `resume`

Dans une session neuve.

1. Lis `INDEX.md` en entier — la vue basse résolution, pas tous les fichiers de zone.
2. Prends l'item de **Position actuelle** (ou, si l'utilisateur en désigne un autre, le sien), et charge **seulement** le fichier de zone correspondant.
3. Reprends le travail. Ne charge un autre fichier de zone que si la tâche l'exige.

## Le prompt de reprise

À la fin de chaque `update`, produis un prompt prêt à coller pour la prochaine session, de cette forme :

```
Reprends le travail sur <projet>. Lis d'abord .checkpoint/INDEX.md, puis .checkpoint/<zone>.md.
Prochain item : <item>.
<1 ligne de contexte ou question ouverte, si utile.>
```

Cible l'item suivant directement, ou — si l'utilisateur préfère choisir — invite-le à piquer dans les items restants de l'index

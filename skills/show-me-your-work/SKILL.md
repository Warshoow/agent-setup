---
name: show-me-your-work
description: Tient un journal de décisions relisable pendant un travail long ou sans personne devant l'écran - une ligne TSV par décision (quoi, pourquoi, preuve, résultat). Local par défaut, commité quand un relecteur doit pouvoir faire confiance au résultat. À utiliser pour /show-me-your-work, un run afk, une migration, un refactor multi-étapes, ou dès que l'utilisateur dit « je vais me coucher », « tu me montreras demain », « lance et laisse tourner ».
---

# Show me your work

Un run de six heures qui rend « c'est fait » n'est pas relisable. Le relecteur
doit soit tout refaire, soit croire sur parole. Une ligne par décision coûte
trois secondes à écrire et remplace la relecture complète.

Porté de pstack (`cursor/plugins`).

## Quand

Ouvre le journal **avant** de commencer, dès qu'un des cas tient :

- l'utilisateur ne regarde pas (run afk, `/loop`, « je vais me coucher ») ;
- le travail a plus de deux phases, ou touche une migration ;
- tu vas prendre des décisions que le diff final ne montrera pas (une option
  écartée, un chemin abandonné, une hypothèse retenue faute de preuve).

Un fix d'une ligne n'a pas de journal.

## Le fichier

`.work/<slug>-<AAAA-MM-JJ>.tsv`, TSV, une décision par ligne, en append. Jamais
de réécriture d'une ligne passée : une décision revenue sur est une **nouvelle**
ligne dont `resultat` dit qu'elle annule la précédente.

**Dans un run afk**, le chemin est imposé par l'orchestrateur et vaut
`.afk/<numéro de ticket>-work.tsv` — il est donné dans le prompt de la session
(`build_prompt` dans `afk.sh`). N'en invente pas un autre : `/afk-debrief` lit
celui-là. `.afk/` est déjà gitignoré, donc le journal reste local sans rien
ajouter.

Entête, écrit une fois. Noms de colonnes et valeurs **en anglais** : ce fichier
est relu par `/afk-debrief`, dont le repo est en anglais.

```
ts	phase	decision	why	evidence	result
```

- `ts` — `date -Is`.
- `phase` — l'étape en cours, le même mot que dans ta todo.
- `decision` — ce que tu as choisi de faire, à l'impératif, une ligne.
- `why` — la raison, pas la paraphrase de la décision. Si tu écris deux fois la
  même chose dans `decision` et `why`, la ligne ne sert à rien.
- `evidence` — ce qui a fait pencher : une commande et son code de sortie, un
  chemin`:`ligne, un numéro de PR, un extrait de log. « ça semblait mieux » n'est
  pas une preuve, écris `none` et assume.
- `result` — `ok`, `ko` ou `abandoned`, ou une ligne de ce que ça a donné. Rempli
  quand tu le sais ; une ligne dont le résultat manque encore se ferme par une
  seconde ligne, pas par une édition.

Échappe les tabulations dans les champs (`tr '\t' ' '`).

```bash
log() { printf '%s\t%s\t%s\t%s\t%s\t%s\n' "$(date -Is)" "$@" >> "$WORK_LOG"; }
```

## Ce qui mérite une ligne

Ce qu'un relecteur ne peut pas déduire du diff :

- une hypothèse retenue parce que personne n'était là pour trancher ;
- une option écartée, et ce qui l'a écartée ;
- un gate rouge, ce que tu en as conclu, ce que tu as changé ;
- une prémisse démentie en cours de route ;
- tout ce que tu as fait **hors** du périmètre demandé, et pourquoi.

Ce qui n'en mérite pas : les étapes mécaniques, les commandes qui passent du
premier coup, la todo. Si chaque ligne du journal correspond à une ligne de diff,
tu écris un changelog — arrête.

## Local ou commité

Local par défaut (`.work/` dans `.gitignore`).

Commit le journal quand le relecteur doit pouvoir faire confiance au résultat
sans tout refaire : run afk qui part en PR, migration, changement sur l'auth ou
les paiements. Dans ce cas il part dans le même commit que le travail, et la
description de PR le cite par chemin.

Ne le commite jamais s'il contient un secret, un token ou du contenu client —
nettoie d'abord.

## À la fin

Rends les lignes `ko` et `abandonné` en premier, puis le prochain geste. Le
journal est la source, ton résumé n'est qu'un index dessus.

Sur un run afk, `/afk-debrief` lit ce fichier à son étape 5 : c'est lui qui
distingue « mauvais gate » de « vraie panne » sans rejouer le run.

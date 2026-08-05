---
name: handoff
description: Protocole de passation de contexte entre agents et entre sessions, via des handoffs JSON valides plutot que des notes markdown. Utilise ce skill des que tu termines une unite de travail substantielle, que tu es bloque, que tu passes la main a un autre agent ou sous-agent, ou que tu reprends un travail existant — meme si l'utilisateur ne parle pas explicitement de handoff, de memoire ou de passation. Utilise-le aussi au demarrage de toute session sur un projet qui contient un repertoire .handoff/, avant de commencer a explorer le code.
---

# Handoff

Passer du contexte entre agents par des `.md` narratifs echoue de facon previsible : rien ne force l'agent qui ecrit a inclure ce qui compte, et l'agent qui lit doit interpreter de la prose. Ce skill remplace la prose par un schema ferme, valide par script. La qualite du handoff ne depend plus de la redaction, mais du passage de la validation.

## Au demarrage d'une session

Si `.handoff/` existe a la racine du projet, lis l'etat vivant **avant** d'explorer le code :

```bash
python3 <skill>/scripts/handoff_read.py
```

Tu obtiens un digest ordonne par cout de redecouverte : blocages, pieges deja rencontres, invariants, decisions actives, points de reprise. Ce n'est pas une concatenation chronologique — les handoffs remplaces et les questions resolues en sont deja sortis.

Filtres utiles : `--task <sous-chaine>`, `--since <date ISO>`, `--agent <nom>`, `--full <id>` pour un handoff entier, `--list` pour l'index, `--json` pour du machine-readable.

## En fin d'unite de travail

Ecris un handoff quand : tu termines une tache, tu es bloque, tu passes la main, ou la session s'arrete avec du travail en cours. Pas apres chaque edit — un handoff par unite de travail coherente.

```bash
python3 <skill>/scripts/handoff_write.py --template          # squelette
python3 <skill>/scripts/handoff_write.py --file payload.json # ou via stdin
```

Le script valide, refuse avec des erreurs actionnables, ou ecrit un fichier immuable dans `.handoff/`. **Si l'ecriture est refusee, corrige le payload et resoumets-le — ne contourne pas en ecrivant un `.md` a cote.** Le refus signale presque toujours une information reellement manquante, pas une chicane de format.

`--dry-run` valide sans ecrire.

## Ce qu'il faut mettre dedans

Le reflexe naturel est de resumer ce qu'on a fait. C'est la partie la moins utile : le diff git la raconte deja. Ce qui ne se re-derive pas :

**`decisions[]`** — chaque decision avec son `why`. Sans la justification, l'agent suivant reverra le choix sans savoir qu'il etait delibere, et le refera peut-etre a l'envers. C'est le champ qui rapporte le plus.

**`failed_attempts[]`** — ce que tu as essaye et qui a echoue, avec la raison. Information la plus chere a reproduire, et celle qu'on perd systematiquement. Mets `dont_retry: true` quand l'echec est structurel et non circonstanciel. Ces entrees survivent a la supersession : un echec est un fait historique, pas une affirmation sur l'etat courant.

**`invariants[]`** — les contraintes qu'un agent naif casserait sans le savoir ("cette fonction doit rester synchrone parce que X l'appelle au niveau module"). Contrairement aux echecs, un invariant meurt avec le handoff qui le portait, puisqu'il decrit l'etat courant.

**`open_questions[]`** — ce que tu n'as pas tranche, formule comme une question. Une question ouverte transmise vaut mieux qu'une decision arbitraire silencieuse.

**`pointers[]`** — la regle centrale du protocole : **si l'information est re-derivable par un grep, stocke le pointeur, pas le fait.** Recopier une signature de fonction ou un extrait de config garantit sa divergence des que le code bouge. Un pointeur avec son `why` reste vrai plus longtemps.

## Regles que le script fait respecter

Elles existent parce que chacune correspond a un mode d'echec observe :

| Regle | Raison |
|---|---|
| `status=blocked` exige une question `blocking: true` | un blocage sans question formulee n'est pas transmissible |
| `status=done` exige `verified_by` non vide | "ca devrait marcher" n'est pas une verification |
| `status=partial`/`abandoned` exige `next_steps` | sinon la reprise repart de zero |
| `why` d'au moins 25 caracteres | une justification de trois mots ne survit pas a la relecture |
| valeurs creuses rejetees ("N/A", "TBD", "voir plus haut") | elles remplissent le champ sans porter d'information |
| blocs de code > 5 lignes rejetes | pointe vers le fichier |
| schema ferme, champs inconnus rejetes | un champ libre fait redevenir le handoff un `.md` |

## Resoudre et remplacer

Rien n'est jamais mute ni ecrase — un fichier par handoff, ecriture unique. Deux agents concurrents ne peuvent donc pas se marcher dessus.

Pour faire evoluer l'etat, ecris un nouveau handoff qui reference l'ancien :

- **`resolves: ["<id-question>"]`** — la question sort de l'etat vivant. Recupere les ids via `handoff_read.py`.
- **`supersedes: ["<id-handoff>"]`** — ses decisions, invariants et points de reprise sortent de l'etat vivant. L'historique reste consultable via `--list` et `--full`.

Le script verifie que les ids references existent : impossible de resoudre une question fantome.

## Exemple

Fin d'une migration partielle, bloquee sur une question d'API :

```json
{
  "agent": "builder",
  "task": {"title": "Migration du client HTTP vers httpx", "status": "blocked"},
  "summary": "Les appels synchrones sont migres. Le streaming reste sur requests, l'API httpx equivalente ne couvre pas le cas de reconnexion.",
  "decisions": [
    {"what": "Garder un wrapper commun plutot que migrer chaque appelant",
     "why": "Quatorze appelants dependent de la signature actuelle; un wrapper permet de migrer par lots sans casser le build a chaque etape."}
  ],
  "failed_attempts": [
    {"what": "Remplacer requests.Session par httpx.Client en drop-in",
     "why_failed": "httpx ne rejoue pas les redirections POST de la meme facon, deux tests d'integration cassent silencieusement.",
     "dont_retry": true}
  ],
  "pointers": [
    {"kind": "file", "ref": "net/wrapper.py", "why": "point d'entree unique de la migration"}
  ],
  "open_questions": [
    {"question": "Accepte-t-on de perdre la reconnexion automatique sur le streaming, ou faut-il l'implementer a la main ?",
     "blocking": true}
  ],
  "next_steps": ["Trancher la question de reconnexion, puis migrer net/stream.py"],
  "confidence": "medium"
}
```

## Sous-agents

Quand tu delegues a un sous-agent, demande-lui de produire le payload de handoff comme sortie finale plutot qu'un rapport en prose. Tu consommes alors une structure validee au lieu d'interpreter un resume — et le contexte survit a la fin du sous-agent.

## Emplacement du store

`.handoff/` est localise en remontant depuis le repertoire courant jusqu'a la racine du projet (`.git`), pour qu'un agent lance depuis un sous-repertoire n'ecrive pas dans un store parallele invisible des autres. `HANDOFF_DIR` permet de forcer un chemin.

Le repertoire se versionne ou non selon l'usage : commite-le si la passation doit franchir les machines, ajoute-le a `.gitignore` si elle est locale a un poste.

Le schema complet et annote est dans `scripts/schema.json`.

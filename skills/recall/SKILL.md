---
name: recall
description: Reconstruit le contexte de travail récent à partir des transcripts Claude Code, de git/gh et du ticket tracker, et rend un brief court - où en est chaque chantier, ce qui a déjà échoué, le prochain geste. À utiliser au réveil, avant de reprendre un sujet, ou avant /afk-debrief. Déclencheurs : /recall, « où j'en étais ? », « remets-moi dans le bain », « qu'est-ce que j'ai fait sur X ? », « catch me up », « reprends le sujet X ».
---

# Recall

Tu reconstruis où en est le travail, puis tu rends un brief tenant sur un écran.
Tu ne racontes pas l'historique, tu dis l'état courant et le prochain geste.

Porté de pstack (`cursor/plugins`), adapté aux transcripts Claude Code.

## 1. Fixer le périmètre avant de chercher

Trois choses, annoncées en une ligne à l'utilisateur :

- **Fenêtre** : par défaut les 7 derniers jours. « récent » est une vraie borne.
- **Sujet** : celui qu'il nomme, sinon « tout ce que j'ai fait » (pas de sujet).
- **Projet** : le cwd courant. Ne lis jamais les transcripts d'un autre projet
  sans qu'il le demande.

Ne transforme jamais silencieusement « tout » en « les N derniers ».

S'il t'a déjà donné l'état (branche, PR, fichiers), sers-t'en et saute la fouille.

Cas voisins à router ailleurs : reprendre **une** conversation précise → il
suffit de la lire ; transformer une habitude en skill → `evolve` ; relire un run
afk fini → `afk-debrief`.

## 2. Indexer les transcripts

Les transcripts vivent dans `~/.claude/projects/<slug>/<uuid>.jsonl`, un message
JSON par ligne. `<slug>` = le chemin du workspace avec `/`, `_` et `.`
remplacés par `-`, le `/` initial compris (`/home/jane_doe/projects/my_app`
→ `-home-jane-doe-projects-my-app`, l'underscore aussi). Les
worktrees afk ont leur propre slug (`…--afk-wt-14`) : inclus-les quand le sujet
touche un run afk. Les fichiers `agent-*.jsonl` sont des sous-agents, pas des
conversations : ignore-les.

Chaque fichier porte une ligne `{"type":"ai-title","aiTitle":…}` : c'est le sujet
de la session, et ça suffit à trier sans ouvrir les fichiers.

```bash
# index : date, titre, chemin — fenêtre de 7 jours, projet courant
SLUG=$(pwd | tr '/_.' '---')
find ~/.claude/projects/"$SLUG"* -name '*.jsonl' ! -name 'agent-*' -mtime -7 2>/dev/null |
  while read -r f; do
    printf '%s\t%s\t%s\n' "$(date -r "$f" +%F\ %H:%M)" \
      "$(grep -m1 -o '"aiTitle": *"[^"]*"' "$f" | cut -d'"' -f4)" "$f"
  done | sort -r
```

Trie par date de modification (`ls -t`, `-mtime`), **jamais** par nom d'UUID.

Filtre sur le sujet avec `grep -l` sur les fichiers de l'index, puis ne lis que
les régions qui matchent.

## 3. Fouiller

Deux ou trois fichiers → lis-les directement, pas de sous-agents.

Au-delà → un `Agent` `scout` par tranche de l'index, `model: haiku`, lancés dans
un seul message. Chaque sous-agent :

- ne lit que les fichiers de sa tranche qui matchent le sujet, et seulement les
  régions qui matchent ;
- saute les sessions sidechain (`"isSidechain":true`), les sessions de test et
  la session courante ;
- rend le même bloc par session : **sujet**, **objectif de l'utilisateur**,
  **décisions**, **fils ouverts**, **ce qui a coincé et les corrections
  reçues**, **artefacts** (PR, tickets, branches), chacun cité par UUID.

Les transcripts bruts restent chez les sous-agents. Le thread principal ne reçoit
que leurs blocs.

## 4. Balayer le dossier partagé

Dès que le sujet nomme une feature, un fichier, un module ou un bug — donc par
défaut, « mon travail sur X » n'exempte pas :

```bash
git log --oneline -20 -- <chemin>
git log --all --oneline --since='7 days ago'
gh pr list --state all --limit 20 --json number,title,state,headRefName,updatedAt
gh pr view <n> --json title,body,state,mergedAt,comments,reviews
```

Jira : si le MCP Atlassian est authentifié, une requête sur les tickets touchés ;
sinon note « Jira non branché » dans le brief plutôt que de l'ignorer. Un résultat
vide est un résultat, un outil absent est un trou — les deux se disent.

Lance ce balayage **en parallèle** de l'étape 3, pas après.

## 5. Vérifier contre l'état réel

Les PR, branches et tickets remontés par les étapes 3 et 4 sont des souvenirs.
Confirme chacun avec `git`/`gh` avant de l'écrire. Une PR « ouverte » dans un
transcript de mardi peut être mergée ou fermée.

## 6. Le brief

Dans cet ordre, rien avant :

- **Capsule** — 5 puces max. Ce qu'est ce travail et où il en est.
- **Chantiers** — une ligne chacun, préfixée d'exactement un tag :
  `[mergé #N]`, `[PR ouverte #N]`, `[en cours <branche>]`,
  `[vérifié, non commité]`, `[revert #N]`, `[prévu, pas commencé]`.
  Pas de tag = pas fini, donc mets-en un.
- **Problèmes** — 5 max, les récurrents. Inclus les symptômes qui reviennent et
  tout fix qui a été livré puis reverté : la prochaine tentative doit démarrer là
  où la précédente s'est cassée.
- **Prochain geste** — un seul, concret.

Une feature ou un ticket voisin reste dehors sauf s'il bloque celui-ci. Si ça
dépasse un écran, coupe du détail, pas des chantiers.

Passe le brief par `behuman` avant de l'envoyer. Cite les sessions par UUID, les
PR par numéro, les tickets par ID.

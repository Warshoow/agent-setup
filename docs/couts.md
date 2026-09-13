# Ce que coûtent les sessions

Mesuré, pas estimé. Tout vient de `~/.claude/projects/*/*.jsonl` : chaque message
assistant y porte son bloc `usage` réel. C'est la facture, elle est déjà sur le
disque, il n'y a rien à installer ni à surveiller.

```bash
./bin/audit-tokens.py 30      # régénère tous les chiffres ci-dessous
```

Instantané du **13 septembre 2026**, 30 jours glissants, 370 sessions.
Les noms de projets sont anonymisés ici.

---

## 1. Où est l'argent

```
input_tokens                     0.1 M
cache_creation_input_tokens    226.6 M
cache_read_input_tokens       9097.8 M      97.6 % de l'entrée
output_tokens                   52.2 M
```

**97,6 % de l'entrée facturée est du cache_read** : le renvoi du contexte déjà
constitué, à chaque tour. Ce n'est pas la lecture d'un fichier qui coûte, c'est
sa relecture aux 200 tours suivants.

Conséquence directe, souvent contre-intuitive : le coût d'une session monte **au
carré du nombre de tours**, pas proportionnellement. Le tour *n* paie tout ce
qu'ont produit les tours 1 à *n−1*. Même travail découpé en 4 sessions ≈ 4 fois
moins cher.

D'où une dépense très concentrée :

```
top  1 session    5.5 %  de l'entrée
top  5           21.3 %
top 10           33.1 %
top 20           46.4 %      (sur 370 sessions)
top 50           64.6 %
```

Un seul projet pro porte 37 % de l'entrée. Les worktrees `afk` en portent 25 %.

## 2. Ce qui remplit le contexte

```
sortie Bash                      57.3 %
paramètres d'appels d'outils     27.1 %     <- le contenu écrit dans les heredocs / Edit
texte utilisateur                 5.6 %
texte assistant                   4.7 %
sortie Read                       3.3 %
sortie autres outils              1.8 %
```

`Read` ne pèse que 3,3 % parce que le mode auto fait lire par `cat` / `sed` /
`grep` — ces lectures sont comptées dans Bash. C'est pour ça que
[`big-read-gate.py`](hooks.md#3-pretooluse-sur-read-et-bash--big-read-gatepy)
garde les deux portes et pas seulement `Read`.

Les 27 % de **paramètres d'appels** sont le contenu des fichiers écrits : un
heredoc de 400 lignes met 400 lignes dans le préfixe, définitivement. Poste non
traité à ce jour.

Sortie Bash par commande :

```
cat   23.0 %     sed   21.1 %     cd    15.8 %     grep   8.8 %
git    8.5 %     gh     3.6 %     ls     3.4 %     docker 1.7 %
```

Sur **28 099 appels Bash, aucune sortie ne dépasse 40 000 caractères.**
Moyenne : 1 827. Retenir ce chiffre, il décide de la section 4.

## 3. Le trou dans `/context`

```
entrée interactive, selon le contexte AU MOMENT du tour
  <50k         0.5 %       770 tours
  50-100k     10.6 %     10166 tours
  100-150k    17.9 %     10538 tours
  150-200k    18.3 %      7678 tours
  200-300k    28.7 %      8627 tours
  >300k       24.0 %      4726 tours

-> 71 % de l'entrée interactive part au-dessus de 150k de contexte
-> 53 %                         au-dessus de 200k
```

La discipline « je m'arrête vers 200k » est visible dans les données — pic médian
153k en VS Code, 125k en CLI — et pourtant la moitié de la facture se fait
au-dessus du seuil. Le compactage automatique fait redescendre, la session
continue, le compteur ne repart jamais de zéro visuellement.

**`/context` est un débit, pas un total.** Il dit ce que coûtera le *prochain*
tour, pas ce qui a déjà été dépensé. Deux sessions plafonnant toutes deux à 200k
peuvent différer d'un facteur 10 selon le nombre de tours passés en haut. À 200k,
un `ls` coûte 200k tokens, exactement comme un refacto.

Entrée **cumulée** par session interactive :

```
médiane   8 M      p75  22 M      p90  72 M      p95  144 M      max  509 M

budget 20 M : 27 % des sessions le dépassent, et portent 67 % de l'entrée
budget 30 M : 20 %                                          59 %
budget 50 M : 13 %                                          49 %
```

D'où `CTX_BUDGET=20000000` dans
[`context-watch.sh`](hooks.md#2-stop--context-watchsh) : 2,5× la médiane, donc
silencieux sur une session normale, et il attrape les deux tiers de la dépense.

### Corollaire : `CTX_LIMIT=1000000` était une mauvaise idée

Le raisonnement « le modèle est `opus[1m]`, donc l'alerte doit tomber à 1 M » est
faux. La taille de la fenêtre ne dit rien du coût : un contexte de 900k coûte six
fois plus par tour qu'un contexte de 150k, fenêtre ou pas. L'alerte doit être
**basse**, pas alignée sur la fenêtre. `export CTX_LIMIT=1000000` n'a jamais été
recollé dans `~/.bashrc`, donc le défaut 200k s'appliquait — heureusement.

## 4. rtk, mesuré

Le README de rtk annonce 60–90 % d'économie. JetBrains a testé, en apparié — même
suite de 86 tâches dans les deux bras, agent épinglé, 4 runs, critères fixés
avant. Résultat : **+7,6 % de coût par tâche à effort faible** (p=0,004, 80 paires
propres), **±0 à effort élevé**, qualité inchangée. Cause : +13,8 % de tours et
+14,3 % de cache reads, pendant que la seule classe de trafic réellement
compressée bougeait à peine.

- [blog.jetbrains.com/ai/2026/07/rtk-claude-code-token-savings/](https://blog.jetbrains.com/ai/2026/07/rtk-claude-code-token-savings/)
- [rtk-ai/rtk#3157](https://github.com/rtk-ai/rtk/issues/3157) — « README is outdated », **ouverte, sans réponse du mainteneur**.

Le dashboard de rtk annonçait 96 M de tokens économisés sur des runs plus chers :
il compare à une alternative imaginaire (la sortie brute complète) et ignore la
troncature intégrée de Claude Code. **`rtk gain` compte ce qui a été envoyé, pas
ce qui a été économisé** — il ne peut pas répondre à la question.

Sur ce profil précisément :

| | |
|---|---|
| Portée réelle | 91,5 % de la sortie d'outils passe par Bash — l'argument « rtk ne voit qu'un cinquième du trafic » ne s'applique pas ici |
| Ce qu'il sait filtrer | `git` 8,5 % + `gh` 3,6 % + `docker` 1,7 % + `pnpm` 0,6 % ≈ **14 % du volume Bash**, soit ~8 % du contexte |
| Ce qu'il ne peut pas filtrer | `cat` + `sed` + `cd` + `grep` = **69 % du volume** : du code explicitement demandé |
| Grosses sorties à écraser | **zéro** sur 28 099 appels |
| Plafond réaliste | **1 à 2 %** de l'entrée |

**À quel effort rtk devient-il rentable ?** L'effort ne le fait pas passer du
négatif au positif, il fait disparaître le négatif : la courbe monte de −7,6 %
vers 0 et ne le dépasse pas dans les données. À faible effort le modèle compense
par des tours courts et nombreux, et comme le coût est dominé par le renvoi du
contexte, chaque tour ajouté coûte plus que ce que la compression rapporte. À
effort élevé la taxe s'annule.

Deux variables, donc : **l'effort décide si rtk coûte, le mélange de commandes
décide s'il rapporte.** Ici l'effort est déjà au meilleur point (`xhigh` sur
40 463 messages, `high` sur 16 990, `low` sur 5) — donc légèrement positif, mais
très en dessous du bruit entre deux sessions. rtk est laissé en place : ni gain
ni perte détectable.

Le profil où rtk paierait est l'inverse : sorties Bash dominées par du log verbeux
(`npm install`, suite de tests complète, `docker build`, `terraform plan`, logs de
CI) avec des sorties de plusieurs centaines de milliers de caractères.

## 5. Ce qui a été fait, par ordre d'effet

| Levier | Effet attendu | État |
|---|---|---|
| Baisser le seuil d'arrêt de 200k à ~120k | 30–40 % de l'entrée | à la main ; alerte instantanée déjà en place |
| Alerte sur budget cumulé (`CTX_BUDGET=20 M`) | rend visibles les 67 % qui étaient invisibles | [`context-watch.sh`](hooks.md#2-stop--context-watchsh) |
| Bloquer les lectures pleines > 350 lignes | borne la croissance du préfixe | [`big-read-gate.py`](hooks.md#3-pretooluse-sur-read-et-bash--big-read-gatepy) |
| rtk | 1–2 %, sous le bruit | laissé en place |

Non traité : les 27 % de contexte en paramètres d'appels d'outils.

## Méthode, pour la refaire ailleurs

1. Ne jamais croire le compteur d'un outil sur ses propres économies : c'est une
   affirmation sur un scénario qui n'a pas eu lieu.
2. Mesurer la composition avant de mesurer un gain — si la classe de trafic visée
   fait 3 % du contexte, l'expérience est inutile.
3. Comparer en apparié (même tâche, deux bras) ou pas du tout. Sur de l'usage
   organique, le bruit du mélange de tâches écrase tout écart inférieur à ~20 %.
4. Le cumulé est dans `/cost`, pas dans `/context`.

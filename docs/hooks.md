# Hooks

Trois hooks déclarés dans `settings.json`. Les deux premiers existaient déjà, le
troisième et le budget cumulé du deuxième viennent de la mesure décrite dans
[docs/couts.md](couts.md).

## 1. PreToolUse sur Bash — `rtk hook claude`

Réécrit les commandes shell vers leur équivalent [rtk](outils.md#rtk--rust-token-killer) avant
exécution (`git status` → `rtk git status`). Transparent, 0 token d'overhead.
Marche techniquement.

⚠️ **Les 60–90 % annoncés ne se vérifient pas ici.** Mesuré sur 30 jours : rtk ne
peut filtrer que ~14 % du volume Bash (`git`, `gh`, `docker`, `pnpm`), le reste
étant du `cat`/`sed`/`grep` non compressible, et aucune des 28 099 sorties Bash ne
dépasse 40k caractères. Plafond réaliste : **1 à 2 %**. Laissé en place — ni gain
ni perte détectable à effort `high`/`xhigh`. Détail et sources :
[couts.md § 4](couts.md#4-rtk-mesuré).

## 2. Stop — context-watch.sh

Deux alertes indépendantes, qui se cumulent dans un seul message si elles tombent
au même tour. L'état est mémorisé dans `$TMPDIR/cc-ctx-<session_id>*`.

### a. Contexte du tour courant — `CTX_LIMIT`, défaut 200 000

Prévient à 85 % (« tu approches ») puis à 100 % (« pense à /compact »), une fois
par palier. Lit le dernier bloc `usage` du transcript (hors sous-agents) et somme
`input + cache_read + cache_creation + output`. Se réarme après un compactage :
l'état redescend, l'alerte repart à la remontée.

C'est le même nombre que `/context`.

**`CTX_LIMIT=1000000` était une erreur.** Le raisonnement « le modèle est
`opus[1m]`, donc l'alerte à 1 M » confond la taille de la fenêtre avec le coût :
un contexte de 900k coûte six fois plus par tour qu'un contexte de 150k, fenêtre
ou pas. L'alerte doit être basse. La ligne n'avait jamais été recollée dans
`~/.bashrc`, donc le défaut 200k s'appliquait. Elle est retirée de
[`shell/bashrc-claude.sh`](../shell/bashrc-claude.sh).

### b. Entrée cumulée de la session — `CTX_BUDGET`, défaut 20 000 000

Le trou que `/context` ne voit pas : il affiche un **débit**, pas un total. Deux
sessions plafonnant toutes deux à 200k peuvent différer d'un facteur 10 selon le
nombre de tours passés en haut. Mesuré : **53 % de l'entrée interactive part
au-dessus de 200k de contexte**, alors que le pic médian est à 153k.

Le hook somme donc l'entrée de tous les tours depuis le début de la session et
alerte à 85 % du budget, puis à chaque multiple (1×, 2×, 3×…) — sinon on serait
averti une fois puis plus jamais, précisément là où ça coûte.

20 M = 2,5× la médiane des sessions interactives (8 M) : silencieux sur une
session normale, il attrape les 27 % de sessions qui portent 67 % de la dépense.

**Lecture incrémentale** : l'offset et le total sont gardés dans
`$TMPDIR/cc-ctx-<session>.cum`, seuls les octets ajoutés depuis le tour précédent
sont reparsés. Coût constant même sur une session à 2 000 tours. Une dernière
ligne incomplète est ignorée et relue au tour suivant ; si le transcript
rapetisse (remplacé, tronqué), le compteur repart de zéro.

### Pourquoi il ne marchait pas — corrigé

**Cause : le champ `"args": []` dans `settings.json`.**

```jsonc
// AVANT — le hook n'est jamais enregistré
{ "type": "command", "command": "${HOME}/hooks/context-watch.sh", "args": [] }
// APRÈS
{ "type": "command", "command": "${HOME}/hooks/context-watch.sh" }
```

`args` n'existe pas dans le schéma d'un hook Claude Code. L'entrée est rejetée à
la validation et **silencieusement ignorée** : aucun message, aucun log, le script
n'est simplement jamais appelé.

Vérifié par bissection sur `claude 2.1.238`, deux runs identiques à ce champ près :

```bash
# sans args → le hook tourne
echo '{"hooks":{"Stop":[{"hooks":[{"type":"command","command":"echo OK >> /tmp/p.log"}]}]}}' > /tmp/a.json
claude -p "ok" --settings /tmp/a.json </dev/null   # /tmp/p.log contient OK

# avec args → rien
echo '{"hooks":{"Stop":[{"hooks":[{"type":"command","command":"echo OK >> /tmp/p.log","args":[]}]}]}}' > /tmp/b.json
claude -p "ok" --settings /tmp/b.json </dev/null   # /tmp/p.log n'existe pas
```

Ce qui **n'était pas** en cause, au passage :
- `${HOME}` dans `command` — la commande passe par un shell, l'expansion se fait.
- le script lui-même — rejoué à la main sur un vrai payload, il calcule juste.

### Limite qui reste

**Le hook a un tour de retard.** Au moment où `Stop` se déclenche, le message de
l'assistant n'est pas encore écrit dans le transcript : le script lit le `usage`
du tour *précédent*. Sur une session neuve il n'y a rien à lire, il sort en
silence (`exit 0`). Sans importance pour un garde-fou, à savoir quand même.

## 3. PreToolUse sur Read et Bash — big-read-gate.py

Bloque la **lecture pleine** d'un fichier de plus de `BIG_READ_MAX` lignes
(défaut 350) et renvoie au modèle, au moment de sa tentative, quoi faire à la
place : `grep -n` pour localiser puis lire la tranche, ou déléguer la question
d'ensemble au subagent [`scout`](../agents/scout.md) qui tourne sur Haiku.

Une règle écrite dans un `CLAUDE.md` est un conseil, `exit 2` n'en est pas un.

**Deux portes, parce qu'une seule ne sert à rien ici.** `Read` ne pèse que 3,3 %
du contexte : le mode auto fait lire par `cat`/`sed`, comptés dans Bash, où `cat`
seul pèse 13 %. Bloquer `Read` sans bloquer `cat` laisse la porte ouverte.

Laisse passer, dans cet ordre :

| Cas | Pourquoi |
|---|---|
| `offset` / `limit` sur `Read` | le modèle sait déjà ce qu'il veut |
| `head -20`, `tail -5`, `head` nu | déjà borné sous le seuil |
| `sed -n '10,40p'`, `sed -n '/motif/p'` | tranche bornée |
| `sed` sans `-n` | transformation, pas lecture |
| pipe, redirection, heredoc, substitution | déjà ciblé, ou la sortie n'entre pas dans la conversation |
| fichier absent | laisse `Read` remonter sa propre erreur |
| JSON illisible, erreur de lecture | **fail open** : on ne casse jamais un appel par accident |

Gère les commandes composées (`cd x && cat gros.py`) et les préfixes
`sudo`/`time`/`env`/`rtk`.

```bash
~/hooks/big-read-gate.py --test     # 19 assertions, ~1 s
export BIG_READ_MAX=500             # pour remonter le seuil
```

## Debug d'un hook qui ne dit rien

```bash
# 1. le hook est-il seulement appelé ?
cat > /tmp/probe.json <<'JSON'
{"hooks":{"Stop":[{"hooks":[{"type":"command","command":"cat >> /tmp/hook-in.log"}]}]}}
JSON
claude -p "ok" --settings /tmp/probe.json < /dev/null

# 2. si oui, tracer le vrai script sur le payload capturé
sed '2a exec 2>>/tmp/trace.log; set -x' ~/hooks/context-watch.sh > /tmp/t.sh && chmod +x /tmp/t.sh
/tmp/t.sh < /tmp/hook-in.log
```

Le `< /dev/null` compte : sans lui, `claude -p` attend 3 s sur stdin et pollue la sortie.

Pour un `PreToolUse`, le payload se fabrique à la main :

```bash
echo '{"tool_name":"Bash","tool_input":{"command":"cat gros.py"}}' | ~/hooks/big-read-gate.py; echo "exit=$?"
```

`exit 2` = bloqué, stderr renvoyé au modèle. `exit 0` = laissé passer.

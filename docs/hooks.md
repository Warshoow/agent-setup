# Hooks

Les deux comptes déclarent les mêmes hooks dans leur `settings.json`.

## 1. `PreToolUse` sur `Bash` → `rtk hook claude`

Réécrit les commandes shell vers leur équivalent [rtk](outils.md#rtk) avant
exécution (`git status` → `rtk git status`). Transparent, 0 token d'overhead,
60–90 % de sortie en moins. Marche.

## 2. `Stop` → `~/hooks/context-watch.sh`

Prévient quand le contexte se remplit : à 85 % de `CTX_LIMIT` (« tu approches »),
puis à 100 % (« pense à /compact »). Il ne parle qu'une fois par palier — l'état
est mémorisé dans `$TMPDIR/cc-ctx-<session_id>`.

Il lit le dernier bloc `usage` du transcript (hors sous-agents) et somme
`input + cache_read + cache_creation + output`.

### Pourquoi il ne marchait pas — corrigé ici

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

### Deux limites qui restent

1. **Le hook a un tour de retard.** Au moment où `Stop` se déclenche, le message
   de l'assistant n'est pas encore écrit dans le transcript : le script lit le
   `usage` du tour *précédent*. Sur une session neuve il n'y a rien à lire, il
   sort en silence (`exit 0`). Sans importance pour un garde-fou, à savoir quand
   même.

2. **`CTX_LIMIT` vaut 200 000 par défaut, mais le modèle est `opus[1m]`.**
   La fenêtre est de 1 M tokens → l'alerte tomberait à 17 % de la fenêtre réelle.
   À poser dans `~/.bashrc` :

   ```bash
   export CTX_LIMIT=1000000
   ```

### Debug d'un hook qui ne dit rien

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

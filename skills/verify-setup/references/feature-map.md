# Forme de la carte des features

Un `README.md` qui indexe, un fichier par feature. Chaque fichier répond du point
de vue de l'utilisateur, jamais du code.

## README.md

```markdown
# Features de <app>

| Feature | Fichier | Surface |
|---|---|---|
| Connexion | [login.md](login.md) | web |
| Créer une séance | [seance-create.md](seance-create.md) | web |
| Export CSV | [export.md](export.md) | CLI |

Une feature sans fichier n'est pas vérifiable. Ajoute le fichier avant de dire
qu'elle marche.
```

## Un fichier de feature

Exactement ces quatre titres de niveau 2, dans cet ordre.

```markdown
# Créer une séance

## Sous-features

- Créer depuis un modèle
- Créer vide
- Dupliquer une séance existante

## Comment y arriver (point de vue utilisateur)

Connecté, sur `/seances`, bouton « Nouvelle séance » en haut à droite. Ouvre un
panneau latéral. Le champ nom a le focus.

## Piloter avec <harnais>

```bash
cd "$SCRATCHPAD" && ~/projects-perso/playright-env/pw --in <projet>-app \
  shot http://localhost:3010/seances avant.png
```

Sélecteurs stables : `[data-testid="new-session"]`, label ARIA « Nom de la
séance », bouton `role=button[name="Enregistrer"]`.

État observable qui prouve que ça marche : la séance apparaît dans la liste
`[data-testid="session-list"]` **et** une ligne existe en base
(`select count(*) from sessions where name = …`).

## Gotchas

- Le panneau s'anime : attendre `[data-testid="new-session-panel"]` visible,
  pas un `sleep`.
- Sans données de seed, la liste est vide et le sélecteur de la liste n'existe
  pas du tout — ce n'est pas un bug.
```

Les *Gotchas* sont la seule section qu'un agent ne peut pas re-déduire du code.
C'est celle qui se remplit à chaque fois qu'un run s'est fait piéger.

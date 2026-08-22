# Le stack design

Cinq skills + un plugin qui se recouvrent partiellement. **Le piège n'est pas de
les installer, c'est de les faire tourner ensemble** : trois d'entre eux
revendiquent la même décision (« quelle est l'esthétique de ce projet ? ») et se
contredisent.

Projet de référence : **`~/projects-perso/qr_code_project`** — impeccable + emil,
avec un vrai design system committé.

---

## Le principe : un directeur, des satellites

```
                   ┌─────────────────────────────┐
   LE DIRECTEUR    │  décide l'esthétique         │   UN SEUL À LA FOIS
   (choisir 1)     │  impeccable                  │   sur une même surface
                   │  design-taste-frontend       │
                   │  high-end-visual-design      │
                   └─────────────────────────────┘
                                 │
   LES SATELLITES    ┌───────────┴───────────┐        cumulables sans risque
   (cumuler)         │ emil-design-eng       │        avec n'importe quel
                     │ ui-ux-pro-max         │        directeur
                     └───────────────────────┘
                                 │
   LES TECHNIQUES    ┌───────────┴───────────┐        « comment on fabrique
   (au besoin)       │ awwwards-motion-site  │        cet effet-là »
                     │ cinematic-scroll-site │
                     └───────────────────────┘
```

Un **directeur** pose le système : palette, typo, échelle, registre. Deux
directeurs sur le même écran = deux systèmes qui se réécrivent l'un l'autre à
chaque itération. Un **satellite** n'a pas d'avis sur le système, il l'affine
(emil) ou lui propose des candidats (pro-max) — d'où l'absence de conflit.

---

## Les directeurs

### impeccable — le seul qui tient un système dans le temps

[pbakaus/impeccable](https://github.com/pbakaus/impeccable) · [impeccable.style](https://impeccable.style/)

C'est le plus lourd et le seul qui **persiste sur disque** :

```
PRODUCT.md            qui sont les users, quel registre (brand | product), la voix
DESIGN.md             la palette et la typo committées, en OKLCH
.impeccable/design.json   les tokens, rampes tonales, ombres — la source de vérité
.agents/skills/impeccable/  la skill + ses ~25 références de sous-commandes
```

25 sous-commandes, chacune une passe étroite : `init` `audit` `craft` `shape`
`polish` `critique` `typeset` `colorize` `layout` `distill` `bolder` `quieter`
`overdrive` `delight` `harden` `optimize` `adapt` `onboard` `document` `extract`
`live` `brand` `product` `interaction-design` `codex`.

Deux registres, choisis par le projet : **brand** (le design EST le produit —
landing, portfolio) vs **product** (le design SERT le produit — dashboard, outil).
Cette distinction est le cœur du truc : c'est ce que les autres skills n'ont pas.

```bash
npx impeccable install     # depuis la racine du projet
/impeccable init           # écrit PRODUCT.md, propose DESIGN.md
```

Flux habituel : `audit` (diagnostiquer) → `normalize`/`craft` (aligner) → `polish` (finir).

Le mode `live` ouvre un navigateur et itère sur le DOM réel (`.impeccable/live/config.json`
dit dans quel fichier injecter). Il y a aussi des hooks `hook-before-edit.mjs` qui
interceptent les éditions — c'est intrusif, à savoir.

> **Règle d'or d'impeccable : l'identité existante gagne.** S'il trouve des
> couleurs de marque committées, il ne les remplace pas. C'est exactement ce que
> `high-end-visual-design` piétine (voir plus bas).

### design-taste-frontend — l'anti-slop one-shot

[Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill) · [tasteskill.dev](https://www.tasteskill.dev/)

```bash
npx skills add https://github.com/Leonxlnx/taste-skill --skill design-taste-frontend
```

Périmètre déclaré en toutes lettres : **landing pages, portfolios, redesigns.
Pas les dashboards, pas les tableaux de données, pas l'UI produit multi-étapes.**

Sa force : la phase **« Design Read »** — avant toute ligne de code, il lit le
brief (type de page, mots-vibes, références, audience, contraintes) et annonce en
une ligne *« je lis ça comme : landing B2B pour acheteurs techniques, langage
minimaliste type Linear »*. Puis il règle trois dials. Discipline anti-défaut
explicite : pas de dégradé violet IA, pas de hero centré sur mesh sombre, pas de
trois cartes égales, pas d'Inter + slate-900.

Autres variantes du même repo : `gpt-taste` (pour Codex), `image-to-code`,
`redesign-existing-projects`, `minimalist-ui`, `industrial-brutalist-ui`, `brandkit`.

### high-end-visual-design — le marteau

Même repo (`Leonxlnx/taste-skill`), install name `high-end-visual-design`.

Persona « Vanguard_UI_Architect », objectif « expérience d'agence à 150k$ ».
Interdits durs : **Inter, Roboto, Arial, Open Sans, Helvetica bannis**, Lucide
épais banni, bordures 1px gris bannies, `ease-in-out` banni. Un « moteur de
variance » tire au sort un archétype (Ethereal Glass / Editorial Luxury / Soft
Structuralism × Bento / Z-Axis Cascade / Editorial Split) pour ne jamais rendre
deux fois la même page.

Excellent sur une landing d'agence à faire péter. **Destructeur sur un produit
existant** : il bannit la police que ton design system a committée.

---

## Les satellites

### emil-design-eng — la couche mouvement

[emilkowalski/skills](https://github.com/emilkowalski/skills) · cours : [animations.dev](https://animations.dev/)

La philosophie d'Emil Kowalski (Vercel, Linear ; auteur de sonner et vaul) sur le
polish : animation, courbes d'easing, spring physics pour les gestes
interruptibles, `:active` scale sur les boutons, `transform-origin` d'un popover
calé sur son trigger, `prefers-reduced-motion`, n'animer que `transform` et
`opacity`.

Il rend ses revues en **tableau Before / After / Why** — format imposé par la skill.

Pourquoi ça ne rentre pas en conflit : il ne choisit ni palette, ni typo, ni
layout. Il arrive **après** le directeur et resserre les 200ms qui font que ça
« feel right ». C'est le complément naturel d'impeccable, dont la section Motion
est plus courte.

### ui-ux-pro-max — la base de données ✅ installé

[nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) · [ui-ux-pro-max-skill.com](https://ui-ux-pro-max-skill.com/)

```bash
/plugin marketplace add nextlevelbuilder/ui-ux-pro-max-skill
/plugin install ui-ux-pro-max@ui-ux-pro-max-skill
```

Installé en **v2.13.0 sur le compte perso** (déclaré dans `settings.perso.json`,
donc restauré tout seul par `install.sh`). Nécessite Python 3 (scripts de
recherche, stdlib seulement) — présent.

Ce n'est pas un directeur : c'est un **oracle consultable**. Une base locale de
84 styles, 192 palettes, 74 pairings de polices, 192 types de produits, 98 règles
UX, 104 icônes, 16 presets GSAP, 25 types de graphes, sur 22 stacks (React, Next,
Vue, Nuxt, Svelte, SwiftUI, React Native, Flutter, Tailwind, shadcn/ui, Compose,
Angular, Laravel, Three.js…).

Zéro conflit *par construction* : il propose des candidats, il n'impose pas de
verdict. C'est le bon partenaire d'impeccable — il alimente le choix de palette
et de typo, impeccable décide et le committe dans `DESIGN.md`.

---

## Les skills de technique

Ni directeurs ni satellites : elles décrivent **comment fabriquer un effet précis**.
Trouvées dans `~/projects-perso/test-front/` (bacs à sable).

| Skill | Effet | Stack |
|---|---|---|
| `awwwards-motion-site` | landing éditoriale, accent unique, typo grotesque XXL, scroll pinné, clip-path reveals, objet 3D central | Next + Lenis + GSAP ScrollTrigger + R3F/Spline |
| `cinematic-scroll-site` | le scroll scrube une caméra pré-rendue (le truc des pages produit Apple) | Next + Lenis + scrub `<canvas>` frame par frame |

À sortir seulement quand la landing demande cet effet-là. Elles supposent une
direction déjà posée.

---

## Ce qu'il ne faut PAS mélanger

| Combinaison | Verdict | Pourquoi |
|---|---|---|
| impeccable + emil | ✅ **recommandé** | emil ne touche pas au système, il resserre le mouvement. C'est le duo du qr_code_project. |
| impeccable + ui-ux-pro-max | ✅ recommandé | pro-max propose, impeccable arbitre et committe. |
| impeccable + **high-end-visual-design** | ❌ **jamais** | high-end bannit Inter et impose ses archétypes ; impeccable préserve l'identité committée. Ils se réécrivent en boucle. |
| impeccable + design-taste-frontend | ⚠️ redondant | les deux font le « quel registre / quelle direction ». Le split brand/product d'impeccable couvre déjà le besoin. |
| design-taste-frontend + high-end-visual-design | ❌ contradictoires | taste-skill dit « lis la salle, pas de défaut » ; high-end dit « toujours du premium d'agence ». Même repo, philosophies opposées. |
| design-taste-frontend + emil / pro-max | ✅ | mêmes raisons que plus haut. |
| high-end-visual-design sur une **UI produit** | ❌ | c'est une skill *brand*. Sur un dashboard elle produit du bruit. |
| n'importe quel directeur sans `PRODUCT.md` | ⚠️ | impeccable refuse et renvoie vers `init` ; les autres devinent, donc dérivent d'une session à l'autre. |

**La règle courte :** un directeur par surface, choisi par le registre.

- Il existe déjà un design system → **impeccable**, registre `product`.
- Landing / portfolio one-shot, pas de système → **design-taste-frontend**.
- Landing d'agence qui doit choquer, aucune contrainte de marque → **high-end-visual-design**, seul.
- Dans tous les cas : **+ emil-design-eng + ui-ux-pro-max**.

---

## Comment c'est installé chez moi

**Par projet, pas au niveau user.** Contrairement aux skills de `~/skills/`, les
skills design vivent dans le repo du projet — parce qu'elles écrivent des états
(`DESIGN.md`, `.impeccable/`) qui appartiennent au projet.

```
<projet>/
├── PRODUCT.md              impeccable init
├── DESIGN.md               impeccable init/document
├── .impeccable/
│   ├── design.json         tokens, rampes OKLCH, ombres
│   └── live/config.json    où injecter en mode live
├── .agents/skills/<nom>/   installation canonique (npx skills add / impeccable install)
└── .claude/skills/<nom>/   copie lue par Claude Code
```

État actuel :

| Projet | impeccable | emil | taste | high-end |
|---|:--:|:--:|:--:|:--:|
| `qr_code_project` | ✅ | ✅ | — | — |
| `WatchLaterAI` | ✅ | ✅ | ✅ | — |
| `notion-todo` | ✅ | ✅ | ✅ | ✅ |
| `adcom-project-next` | ✅ | ✅ | ✅ | ✅ |

> `notion-todo` et `adcom-project-next` ont les quatre. C'est précisément la
> combinaison à éviter : quatre directeurs, dont deux qui se contredisent. À
> réduire à impeccable + emil (+ pro-max, maintenant global).

`ui-ux-pro-max` est le seul du lot installé **en plugin user** : pas d'état par
projet, donc rien à installer par repo.

## Repartir de zéro sur un projet

```bash
cd <projet>
npx impeccable install                                              # le directeur
npx skills add https://github.com/emilkowalski/skills --skill emil-design-eng
# ui-ux-pro-max est déjà là, c'est un plugin user
claude
> /impeccable init        # PRODUCT.md + DESIGN.md — à faire AVANT toute UI
> /impeccable audit       # si le projet a déjà une UI
```

`/impeccable init` d'abord, toujours : les autres skills lisent `PRODUCT.md` pour
savoir à qui elles parlent.

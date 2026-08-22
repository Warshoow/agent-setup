# Le stack design

Cinq skills tierces + un plugin + deux skills maison. Certaines se complètent,
**trois se contredisent sur des points précis et vérifiables** — pas « en
philosophie », sur la même police, la même courbe, le même fichier de tokens.

Ce document dit qui décide quoi, et pourquoi certaines paires produisent une UI
qui se réécrit toute seule à chaque itération.

---

## Qui décide quoi

Le seul axe qui compte : **une skill décide-t-elle le système (palette, typo,
échelle), ou l'affine-t-elle ?** Deux décideurs sur la même surface, et chaque
passe défait la précédente.

| | Skill | Décide le système ? |
|---|---|:--:|
| **Directeurs** | `impeccable` | ✅ et le committe sur disque |
| | `design-taste-frontend` | ✅ par session |
| | `high-end-visual-design` | ✅ et interdit le reste |
| **Satellites** | `emil-design-eng` | ❌ mouvement uniquement |
| | `ui-ux-pro-max` (la skill) | ❌ base de données consultable |
| **Techniques** | `awwwards-motion-site`, `cinematic-scroll-site` | ❌ recettes d'effet |

> ⚠️ Le **plugin** `ui-ux-pro-max` livre 7 skills, pas une. Trois d'entre elles
> sont des décideurs déguisés. Voir la section dédiée — c'est le piège le moins
> visible du lot.

---

## Les directeurs

### impeccable

[pbakaus/impeccable](https://github.com/pbakaus/impeccable) · [impeccable.style](https://impeccable.style/)

```bash
npx impeccable install     # depuis la racine du projet
/impeccable init           # écrit PRODUCT.md, propose DESIGN.md
```

Le seul qui **persiste sur disque**, et c'est toute la différence :

```
PRODUCT.md                users, registre (brand | product), voix, anti-références
DESIGN.md                 palette + typo committées, en OKLCH
.impeccable/design.json   tokens, rampes tonales, ombres — la source de vérité
.impeccable/live/config.json  où injecter en mode live
```

~25 sous-commandes, chacune une passe étroite : `init` `audit` `craft` `shape`
`polish` `critique` `typeset` `colorize` `layout` `animate` `distill` `bolder`
`quieter` `overdrive` `delight` `harden` `optimize` `adapt` `onboard` `document`
`extract` `clarify` `live` `codex`.

**Le cœur du truc, c'est le registre.** `brand` (le design EST le produit) et
`product` (le design SERT le produit) ne suivent pas les mêmes règles — dans la
*même* skill. Exemple concret, la même police :

| | brand.md | product.md |
|---|---|---|
| Inter | dans la **ban list** des « training-data defaults » | dans les **permissions** : « System fonts and familiar sans defaults (Inter, SF Pro, system-ui) » |
| familiarité | « Restraint without intent now reads as mediocre. Go big or go home. » | « Familiarity is often a feature here. Consistency over surprise. » |

Aucune des autres skills n'a cette bascule. C'est pour ça qu'elle tient dans le
temps sur une UI produit là où les autres dérivent.

**Sa règle de survie**, `brand.md` :

> « The reflex-reject lists apply to **new design choices**. When the existing
> brand has already committed to a font or a lane as part of its identity,
> **identity-preservation wins**. »

Retenir cette phrase : c'est elle qui est incompatible avec `high-end-visual-design`.

Flux : `audit` (diagnostiquer) → `craft` / `polish`. Le mode `live` ouvre un
navigateur et itère sur le DOM réel ; des hooks `hook-before-edit.mjs`
interceptent les éditions — c'est intrusif, à savoir avant de l'activer.

### design-taste-frontend

[Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill) · [tasteskill.dev](https://www.tasteskill.dev/)

```bash
npx skills add https://github.com/Leonxlnx/taste-skill --skill design-taste-frontend
```

Périmètre déclaré en tête de skill : **landing pages, portfolios, redesigns. Pas
les dashboards, pas les tableaux de données, pas l'UI produit multi-étapes.**

Sa vraie valeur, c'est la phase **« Design Read »** : avant toute ligne de code,
lire le brief (type de page, mots-vibes, références, audience, contraintes
silencieuses) et l'annoncer en une ligne — *« je lis ça comme : landing B2B pour
acheteurs techniques, langage minimaliste type Linear »*. Puis trois dials.

Le reste est une longue liste d'anti-clichés **avec chemin d'override explicite**,
ce qui la rend moins brutale qu'elle n'en a l'air :

- Inter « discouraged as default », override si le brief demande neutre / Linear / secteur public.
- « THE LILA RULE » : pas de glow violet IA par défaut.
- « PREMIUM-CONSUMER PALETTE BAN » : la palette beige+laiton+espresso est bannie par défaut sur les briefs premium, avec 7 familles de rechange et une **règle de rotation** (ne pas ressortir la même deux fois).
- « COLOR CONSISTENCY LOCK » : un accent choisi vaut pour toute la page.
- « SERIF DISCIPLINE » : serif très découragé par défaut.
- « **One system per project.** Do not mix Fluent React with Carbon in the same tree. Do not import shadcn/ui components into a Material 3 app. »

Cette dernière phrase est la sienne. Elle vaut aussi pour les skills elles-mêmes.

Variantes du même repo : `gpt-taste` (Codex), `image-to-code`,
`redesign-existing-projects`, `minimalist-ui`, `industrial-brutalist-ui`,
`full-output-enforcement`, `brandkit`.

### high-end-visual-design

Même repo, install name `high-end-visual-design`.

Persona « Vanguard_UI_Architect », cible « expérience d'agence à 150k$ ». Deux
mécaniques la distinguent :

1. **La « ABSOLUTE ZERO DIRECTIVE »** — pas des recommandations, des échecs :
   « If your generated code includes ANY of the following, the design instantly
   fails ». **Polices bannies : Inter, Roboto, Arial, Open Sans, Helvetica.**
   Plus Lucide épais, bordures 1px grises, `ease-in-out`, navbars sticky bord à bord.
2. **La « Variance Mandate »** — « NEVER generate the exact same layout or
   aesthetic twice in a row ». Elle tire au sort un archétype de vibe
   (Ethereal Glass / Editorial Luxury / Soft Structuralism) × un archétype de
   layout (Bento asymétrique / Z-Axis Cascade / Editorial Split).

Redoutable sur une landing d'agence greenfield. **Structurellement inutilisable
sur un projet qui a une identité** : « ne jamais refaire pareil » est la négation
exacte de « identity-preservation wins ».

---

## Les satellites

### emil-design-eng

[emilkowalski/skills](https://github.com/emilkowalski/skills) · cours [animations.dev](https://animations.dev/)

```bash
npx skills add https://github.com/emilkowalski/skills --skill emil-design-eng
```

La philosophie d'Emil Kowalski (Vercel, Linear ; auteur de `sonner` et `vaul`) :
courbes d'easing, spring physics pour les gestes interruptibles, `:active` scale
sur les boutons, `transform-origin` d'un popover calé sur son trigger,
`prefers-reduced-motion`, n'animer que `transform` et `opacity`. Revue rendue en
**tableau Before / After / Why**, format imposé par la skill.

**Nuance importante :** ce n'est *pas* un complément à un trou d'impeccable.
impeccable couvre déjà le mouvement (`animate.md`, `interaction-design.md`,
`polish.md`). Les deux se recouvrent et **divergent sur deux points** :

| Point | impeccable | emil |
|---|---|---|
| springs | « Use bounce or elastic easing curves » est dans la liste des **erreurs** (« they feel dated ») | section entière « Spring Animations » : « springs feel more natural than duration-based animations » |
| `ease-in` | reconnaît un usage légitime (effet de pic-fin : ease-in fait *paraître* la tâche plus courte) | « **Never** use ease-in for UI animations » |
| tokens | `--ease-out-quart/quint/expo` | `--ease-out`, `--ease-drawer` (valeurs différentes) |

Aucune de ces divergences n'est fatale — un spring critiquement amorti ne
rebondit pas — mais l'agent qui charge les deux tranchera au hasard. **Décider
une fois pour toutes : emil est l'autorité sur le mouvement, impeccable sur le
reste.** Et n'importer qu'une seule échelle de tokens d'easing.

### ui-ux-pro-max — attention, c'est 7 skills

[nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) · [ui-ux-pro-max-skill.com](https://ui-ux-pro-max-skill.com/)

```bash
/plugin marketplace add nextlevelbuilder/ui-ux-pro-max-skill
/plugin install ui-ux-pro-max@ui-ux-pro-max-skill
```

Installé en **v2.13.0, compte perso** (déclaré dans `settings.perso.json`).
Python 3 requis pour les scripts de recherche
(stdlib seule). Coût : **~1 082 tokens always-on**, aucun hook, aucun agent,
aucun serveur MCP enregistré.

Le plugin livre **sept** skills, et elles ne jouent pas le même rôle :

| Skill | on-invoke | Rôle | Avec un directeur |
|---|--:|---|---|
| `ui-ux-pro-max` | ~6.3k | la base : 84 styles, 192 palettes, 74 pairings, 119 règles UX, 105 icônes, 17 presets GSAP, 25 types de graphes, 22 stacks | ✅ **c'est celle qu'on veut** — elle propose, elle n'impose pas |
| `design-system` | ~2.6k | architecture de tokens 3 couches (primitive→semantic→component), échelles typo/spacing | ❌ **doublon frontal** avec `DESIGN.md` + `.impeccable/design.json` |
| `ui-styling` | ~3.8k | impose shadcn/ui + Radix + Tailwind comme LE stack | ⚠️ décide à la place du directeur ; et viole le « one system per project » de taste-skill si le projet n'est pas sur ce stack |
| `brand` | ~1.1k | voix de marque, identité visuelle, style guides | ⚠️ recouvre `PRODUCT.md` (voix) et le registre `brand` |
| `design` | ~4.7k | méga-skill : logos, CIP, slides, bannières, icônes, photos sociales — **nécessite `GEMINI_API_KEY`** | hors sujet ici |
| `banner-design` | ~3.1k | bannières social/ads/print | recouvre `marketing-skills` |
| `slides` | ~360 | présentations HTML + Chart.js | hors sujet |

**Le problème pratique :** les descriptions de `ui-styling` et `design-system`
sont larges (« Use when building user interfaces… », « Use for design tokens »).
Elles se déclenchent sur exactement les mêmes prompts qu'impeccable. On croit
consulter une base de données, on a invité trois décideurs de plus.

> **En pratique :** garder le plugin pour `ui-ux-pro-max`, et quand la session
> touche au design system, dire explicitement quelle skill on veut. Si les
> collisions deviennent pénibles, `claude plugin disable` et copier la seule
> skill `ui-ux-pro-max/` en skill de projet.

---

## Les skills maison

Écrites pour reproduire un effet précis repéré sur un site. Archivées dans
[`skills/`](../skills/) — **pas installées au niveau user** : elles sont trop
spécifiques pour être always-on, on les copie dans le projet qui en a besoin.

| Skill | Effet | Stack |
|---|---|---|
| [`awwwards-motion-site`](../skills/awwwards-motion-site/) | landing éditoriale : accent unique, typo grotesque XXL, scroll pinné, clip-path reveals, marquees, objet 3D central | Next ou HTML nu + Lenis + GSAP ScrollTrigger + R3F/Spline |
| [`cinematic-scroll-site`](../skills/cinematic-scroll-site/) | le scroll scrube une caméra pré-rendue (la technique des pages produit Apple) — avec `ScrollScrubScene.tsx`, `chapters.ts` et `extract-frames.sh` fournis | Next App Router + Lenis + scrub `<canvas>` |

`cinematic-scroll-site` porte une observation qui vaut le détour : ces sites ne
sont presque jamais de la 3D temps réel, c'est une vidéo pré-rendue scrubbée par
la position de scroll — d'où le photoréalisme qui tourne sur un téléphone.

```bash
cp -r <ce-repo>/skills/awwwards-motion-site <projet>/.claude/skills/
```

Ce sont des **recettes de fabrication**, pas des directions artistiques : elles
supposent qu'un directeur a déjà tranché la palette et la typo.

---

## Ce qu'il ne faut pas mélanger

| Combinaison | Verdict | Le point de rupture, concrètement |
|---|---|---|
| impeccable + emil | ✅ **le duo de référence** | se recouvrent sur le mouvement ; trancher une fois : emil décide le mouvement, impeccable le reste |
| impeccable + skill `ui-ux-pro-max` seule | ✅ | pro-max propose des candidats, impeccable arbitre et committe |
| impeccable + `design-system` (du plugin) | ❌ | deux architectures de tokens sur le même projet, chacune se croyant la source de vérité |
| impeccable + `ui-styling` (du plugin) | ⚠️ | impose shadcn/Radix/Tailwind quel que soit le stack réel |
| impeccable **product** + high-end-visual-design | ❌ **jamais** | product.md autorise Inter ; high-end le déclare « instant fail ». Et « identity-preservation wins » vs « never the same twice » |
| impeccable **brand** + high-end-visual-design | ❌ quand même | les deux bannissent Inter, donc l'accord est superficiel — mais deux ban lists différentes et deux moteurs de direction restent deux directeurs |
| design-taste-frontend + high-end-visual-design | ❌ | même repo, thèses opposées : « lis la salle, override possible » vs « toujours du premium d'agence, aucun override ». Et taste dit lui-même « one system per project » |
| impeccable + design-taste-frontend | ⚠️ redondant | le split brand/product d'impeccable couvre déjà le « quelle direction ». Deux ban lists de polices qui ne coïncident pas (taste bannit le serif par défaut ; impeccable/brand bannit les serifs *réflexes* — Playfair, Fraunces, Cormorant — mais encourage à chercher un vrai serif) |
| high-end-visual-design sur une UI produit | ❌ | c'est une skill *brand*. Sur un dashboard, la « Variance Mandate » casse la cohérence écran à écran |
| n'importe quel directeur sans `PRODUCT.md` | ⚠️ | impeccable refuse et renvoie vers `init`. Les autres devinent — donc dérivent d'une session à l'autre |

**La règle courte :**

- Un design system existe déjà → **impeccable**, registre `product`.
- Landing / portfolio one-shot, rien de committé → **design-taste-frontend**.
- Landing greenfield qui doit choquer, zéro contrainte de marque → **high-end-visual-design**, seul.
- Dans les trois cas : **+ emil-design-eng** (mouvement) **+ la skill `ui-ux-pro-max`** (catalogue).
- Jamais deux directeurs sur la même surface. Jamais `high-end` sur un projet qui a une identité.

---

## Comment c'est installé

**Par projet, pas au niveau user** — contrairement aux skills de `~/skills/`.
Raison simple : elles écrivent un état (`DESIGN.md`, `.impeccable/`) qui
appartient au repo. Seul `ui-ux-pro-max` est un plugin user, parce qu'il ne
persiste rien.

```
<projet>/
├── PRODUCT.md              impeccable init
├── DESIGN.md               impeccable init / document
├── .impeccable/
│   ├── design.json         tokens, rampes OKLCH, ombres
│   └── live/config.json    point d'injection du mode live
├── .agents/skills/<nom>/   installation canonique (npx skills add / impeccable install)
└── .claude/skills/<nom>/   copie lue par Claude Code
```

Les deux dossiers coexistent : `.agents/skills/` est la cible des installeurs npx
(convention inter-outils), `.claude/skills/` est ce que Claude Code lit.

## Repartir de zéro sur un projet

```bash
cd <projet>
npx impeccable install                                                       # le directeur
npx skills add https://github.com/emilkowalski/skills --skill emil-design-eng   # le mouvement
# ui-ux-pro-max est déjà là (plugin user)
claude
> /impeccable init        # PRODUCT.md + DESIGN.md — AVANT toute UI
> /impeccable audit       # si une UI existe déjà
```

`init` d'abord, toujours : les autres skills lisent `PRODUCT.md` pour savoir à
qui elles parlent. Sans lui, chaque session redevine le public et le registre.

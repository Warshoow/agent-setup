# Le stack design

Cinq skills tierces + un plugin + un MCP + deux skills maison.

**La répartition qu'on croit avoir est la bonne** : `impeccable` fait le gros du
travail, `design-taste-frontend` apprend le goût et bloque le slop,
`emil-design-eng` tient les transitions. Le partage des tâches est juste.

Ce qui l'est moins, c'est d'en conclure qu'elles s'additionnent. Deux d'entre
elles se prononcent sur les mêmes axes — police, couleur, layout — avec des
listes qui ne coïncident pas. Voir [le verdict sémantique](#le-verdict-sémantique)
et [lesquels garder](#lesquels-garder).

Ce document existe pour deux exceptions que rien n'annonce :

1. **`high-end-visual-design`** vient du *même repo* que `design-taste-frontend`.
   On croit installer « taste-skill », on installe deux skills dont une seule est
   combinable. Celle-là ne l'est pas.
2. **Le plugin `ui-ux-pro-max`** livre sept skills, dont trois décident le design
   system sans le dire.

Le reste — le MCP 21st.dev, les skills de technique — est orthogonal et
s'additionne sans risque.

---

## Qui décide quoi

Le seul axe qui compte : **une skill décide-t-elle le système (palette, typo,
échelle), ou l'affine-t-elle ?** Deux décideurs sur la même surface, et chaque
passe défait la précédente.

| | Skill | Décide le système ? |
|---|---|:--:|
| **Directeurs** | `impeccable` | ✅ et le committe sur disque |
| | `design-taste-frontend` | ✅ par session — mais **se met hors-jeu tout seul** sur l'UI produit |
| | `high-end-visual-design` | ✅ et interdit le reste, sans échappatoire |
| **Satellites** | `emil-design-eng` | ❌ mouvement uniquement |
| | `ui-ux-pro-max` (la skill) | ❌ base de données consultable |
| **Techniques** | `awwwards-motion-site`, `cinematic-scroll-site` | ❌ recettes d'effet |

Deux directeurs sur la **même surface**, c'est le problème. Mais
`design-taste-frontend` déclare lui-même son périmètre — *« landing pages,
portfolios, redesigns. **Not** dashboards, not data tables, not multi-step
product UI »* — donc sur un dashboard il ne se déclenche pas et laisse
`impeccable` travailler. Le chevauchement n'existe en pratique que sur une
landing, là où les deux veulent diriger. C'est le seul moment où il faut trancher.

`high-end-visual-design` n'a pas ce garde-fou : il s'applique partout, et sa
« Variance Mandate » interdit la cohérence écran à écran dont une UI produit vit.

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

Même repo que `design-taste-frontend`, install name `high-end-visual-design`.

> **C'est le piège.** Les deux sortent de `Leonxlnx/taste-skill`, donc on les
> installe ensemble en croyant installer « taste-skill ». Ce sont deux skills
> opposées : l'une lit la salle et prévoit un override pour chaque règle, l'autre
> impose un standard d'agence sans échappatoire. `design-taste-frontend` est la
> skill par défaut du repo ; `high-end-visual-design` en est une variante.

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

## Le MCP 21st.dev (magic)

[21st.dev](https://21st.dev/) — bibliothèque de composants React/Tailwind
consultable par l'agent. Déclaré **par projet** dans un `.mcp.json` :

```json
"magic": {
  "type": "stdio",
  "command": "npx",
  "args": ["-y", "@21st-dev/magic@latest"],
  "env": { "API_KEY": "${MAGIC_API_KEY}" }
}
```

Outils exposés : `21st_magic_component_inspiration` (chercher des exemples),
génération et refinement de composants, recherche de logos.

**Zéro conflit avec quoi que ce soit, par nature.** Ce n'est pas une skill : il
n'a pas d'opinion, il ne s'injecte pas dans le prompt, il ne se déclenche pas
tout seul. C'est un outil qu'on appelle pour voir comment d'autres ont résolu un
bloc — et ce que le directeur en fait reste sa décision. C'est le complément
naturel du catalogue `ui-ux-pro-max` : l'un donne des styles et des palettes,
l'autre des composants réels.

Seule précaution : ce qu'il rend est du **matériau**, pas une direction. Un
composant collé tel quel arrive avec sa propre typo et son propre spacing — le
passer par `/impeccable polish` ou `/impeccable extract` avant de le garder.

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

## Ce que ça donne en vrai — mesuré

Trois runs sur un projet neuf, les quatre skills installées en `.claude/skills/`,
compte perso, sonnet, `claude -p`.

| Prompt | Skill déclenchée | Ce qui s'est passé |
|---|---|---|
| « landing SaaS B2B — **ne code rien**, dis-moi la direction » | **aucune** | les 4 étaient listées et disponibles ; le modèle a répondu de lui-même |
| « **construis** la landing… pas du template » | `design-taste-frontend`, **seule** | déclenchée une fois au début, puis 15 éditions en autonomie sans rappeler d'autre skill |
| « **construis** le dashboard admin : sidebar, table, panneau de détail » | `impeccable`, **seule** | a lancé `context.mjs` → `NO_PRODUCT_MD` → lu `reference/init.md` → **s'est arrêtée pour poser 3 questions** au lieu de coder |

Trois conclusions factuelles :

**1. Le routage se fait tout seul.** Le prompt landing a pris taste-skill, le
prompt dashboard a pris impeccable — exactement ce que leurs périmètres
annoncent. Personne n'a eu à choisir.

**2. Une seule skill se déclenche par tour.** C'est le point qui désamorce
presque tout. Le coût permanent des quatre `description:` est d'environ **390
tokens** — négligeable. Le corps ne se charge qu'à l'invocation, et il est gros :

| Skill | `description:` (permanent) | corps (à l'invocation) |
|---|--:|--:|
| impeccable | ~223 tok | 21 Ko + une référence de commande + une de registre |
| design-taste-frontend | ~67 tok | **87 Ko** (~22k tokens d'un coup) |
| emil-design-eng | ~38 tok | 27 Ko |
| high-end-visual-design | ~58 tok | 10 Ko |

Un modèle qui vient d'avaler 22k tokens de direction artistique n'en charge pas
5k de plus qui le contredisent. **Le conflit n'existe que si deux skills entrent
dans le même tour** — ce qui n'arrive pas spontanément.

**3. La contradiction est réelle, elle attend juste qu'on l'invoque.** La landing
produite par taste-skill utilise `Space Grotesk` (display) et `Plus Jakarta Sans`
(body). Ces deux polices sont dans la **ban list de `impeccable/brand.md`**
(« training-data defaults »). `Plus Jakarta Sans` est en même temps dans la liste
*approuvée* de `high-end-visual-design`. Trois verdicts opposés sur la même
police, sur la même page.

Personne ne l'a vu passer, parce qu'une seule skill parlait. Mais lancer
`/impeccable polish` sur cette page **changera les deux polices** — et ça se
présentera comme une amélioration, pas comme un conflit.

> **La règle qui tombe de là :** le risque n'est pas d'avoir plusieurs skills
> installées, c'est de **les enchaîner à la main sur la même surface**. Laisser
> le routage faire son travail ; ne pas passer une page d'un directeur à l'autre.

## Le vrai test : est-ce qu'elles disent la même chose ?

Le déclenchement n'est pas le sujet. Puisqu'on les appelle **soi-même**, chacune
pour son périmètre, la seule question qui compte est : **leurs prescriptions
pointent-elles dans le même sens ?** Si deux skills appellent « bon » deux choses
opposées, elles sont incompatibles — même invoquées à dix minutes d'intervalle.

Comparaison sur les axes où elles se prononcent toutes. Citations littérales.

### Polices

| Police | impeccable `brand` | impeccable `product` | design-taste-frontend | high-end |
|---|:--:|:--:|:--:|:--:|
| `Inter` | ❌ ban list | ✅ « Product permissions » | ⚠️ découragée, override prévu | ❌ « instant fail » |
| `Outfit` | ❌ ban list | — | ✅ **recommandée** | — |
| `Plus Jakarta Sans` | ❌ ban list | — | — | ✅ **recommandée** |
| `Space Grotesk` | ❌ ban list | — | — | ✅ (« geometric Grotesk ») |
| `Geist` | ✅ | ✅ | ✅ | ✅ |

`Geist` est la **seule police sur laquelle les quatre tombent d'accord**. Tout le
reste est un champ de mines : la police recommandée par l'une est bannie par
l'autre.

### Cartes

> **impeccable** : « Cards are the lazy answer. Use them only when they're truly the best affordance. **Nested cards are always wrong.** »
> **taste-skill** : « Use cards **ONLY** when elevation communicates real hierarchy. Otherwise group with `border-t`, `divide-y`, or negative space. »
> **high-end**, archétypes de layout : « **The Asymmetrical Bento** — a masonry-like CSS Grid of varying card sizes » · « **The Z-Axis Cascade** — elements stacked like physical cards, slightly overlapping, some with a `-2deg` rotation »

Deux des trois archétypes de layout de high-end **sont** des grilles de cartes
empilées. Les deux autres skills considèrent la carte comme le réflexe paresseux.

### Fond et gradients

> **taste-skill**, « Anti-Default Discipline » : « Do not default to: **AI-purple gradients**, **centered hero over dark mesh**, three equal feature cards, **generic glassmorphism on everything** »
> **high-end**, archétype n°1 « Ethereal Glass » : « Deepest OLED black (`#050505`), **radial mesh gradients (subtle glowing purple/emerald orbs)** in the background. **Vantablack cards with heavy `backdrop-blur-2xl`** »

L'archétype phare de high-end est, mot pour mot, la liste de ce que taste-skill
interdit. Ce n'est pas une nuance de goût : c'est la même chose décrite une fois
comme la cible, une fois comme le piège.

### Identité

> **impeccable** : « When the existing brand has already committed to a font or a lane, **identity-preservation wins**. »
> **high-end** : « **NEVER** generate the exact same layout or aesthetic twice in a row. »

Inconciliable par construction : l'un protège ce qui existe, l'autre a pour
mandat de ne jamais le refaire.

### Mouvement

| | impeccable | emil | high-end |
|---|---|---|---|
| springs | « bounce/elastic **feel dated** » (liste des erreurs) | section entière : « springs feel more natural » | — |
| `ease-in` | usage légitime reconnu (effet pic-fin) | « **Never** use ease-in for UI » | — |
| `ease-in-out` | — | token défini `cubic-bezier(0.77,0,0.175,1)` | ❌ **banni** |

### Le verdict sémantique

| | impeccable | taste | emil | high-end |
|---|:--:|:--:|:--:|:--:|
| **impeccable** | — | ⚠️ même but, listes différentes | ⚠️ divergent sur le mouvement | ❌ **opposés** |
| **taste** | ⚠️ | — | ✅ axes disjoints | ❌ **opposés** |
| **emil** | ⚠️ | ✅ | — | ⚠️ `ease-in-out` |
| **high-end** | ❌ | ❌ | ⚠️ | — |

- **emil** ne se prononce ni sur la police, ni sur la couleur, ni sur le layout.
  C'est le seul dont le périmètre est vraiment disjoint : il est compatible avec
  tout, à un arbitrage près sur les springs.
- **impeccable et taste veulent la même chose** — chasser les défauts LLM — mais
  avec deux listes qui ne coïncident pas. Ils ne se contredisent pas sur le *but*,
  seulement sur les *entrées*. C'est arbitrable : une seule liste fait foi.
- **high-end contredit les deux sur le fond.** Cartes, gradients, identité : à
  chaque fois l'inverse. Aucun arbitrage possible, c'est un autre projet.

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
| impeccable + design-taste-frontend | ✅ sur UI produit, ⚠️ sur landing | sur un dashboard, taste se met hors-jeu tout seul (périmètre déclaré). Sur une landing les deux dirigent : deux ban lists de polices qui ne coïncident pas (taste bannit le serif par défaut ; impeccable/brand bannit les serifs *réflexes* — Playfair, Fraunces, Cormorant — mais encourage à chercher un vrai serif). Là, en choisir un. |
| high-end-visual-design sur une UI produit | ❌ | c'est une skill *brand*. Sur un dashboard, la « Variance Mandate » casse la cohérence écran à écran |
| n'importe quel directeur sans `PRODUCT.md` | ⚠️ | impeccable refuse et renvoie vers `init`. Les autres devinent — donc dérivent d'une session à l'autre |

## Lesquels garder

**Garder :**

| Skill | Pourquoi |
|---|---|
| **impeccable** | le seul qui persiste un système sur disque et qui bascule `brand` / `product`. Rien ne le remplace. |
| **emil-design-eng** | le seul dont le périmètre est vraiment disjoint : il ne dit rien sur la police, la couleur ni le layout. Trancher une fois : **emil fait autorité sur le mouvement, impeccable sur le reste.** |
| skill **`ui-ux-pro-max`** (celle-là seule) | catalogue consultable, aucune prescription — pas de conflit sémantique possible |
| **MCP magic** (21st.dev) | fournit du matériau, pas une direction. Repasser ce qu'il rend par `/impeccable polish`. |

**Jeter :**

| Skill | Pourquoi |
|---|---|
| **high-end-visual-design** | ce n'est pas « une version plus agressive », c'est l'**inverse**. Cartes, gradients, identité : contredit impeccable *et* taste-skill à chaque fois. Inarbitrable. |
| les 6 autres skills du plugin (`design-system`, `ui-styling`, `brand`, `design`, `banner-design`, `slides`) | mêmes prescriptions qu'impeccable, autre voix. `design-system` en particulier redéfinit l'architecture de tokens. |

**Cas par cas :**

**design-taste-frontend** — redondant avec impeccable dès qu'un `PRODUCT.md`
existe : même but (chasser les défauts LLM), listes différentes. Utile pour une
landing one-shot sans système. Si tu gardes les deux : sur une landing, en
choisir **un**, et ne pas repasser l'autre dessus après coup.

### Le mode d'emploi qui en découle

- Un design system existe → **impeccable** mène, registre `product`, + emil.
- Landing one-shot, rien de committé → **design-taste-frontend** seul, + emil.
- Jamais deux directeurs sur la même surface — pas parce qu'ils se déclenchent
  ensemble (ils ne le font pas), mais parce que **le second défera le travail du
  premier en croyant l'améliorer**.

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

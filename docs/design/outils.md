# Les outils, étape par étape

Ce qui sert **avant** et **autour** des skills de design : trouver des références,
en extraire un système, explorer des directions, produire des visuels, animer,
vérifier. Les skills eux-mêmes (impeccable, taste, emil, ui-ux-pro-max) sont dans
[stack.md](stack.md).

Prix et conditions relevés en octobre 2026 — à revérifier avant de payer. Le niveau
de preuve de chaque affirmation est dans [recherche.md](recherche.md).

---

## Références

Le but : partir de vrais sites **de la même catégorie** que le tien. La recherche
UX dit que « peu chargé et conforme à ce qu'on attend du type de site » est ce qui
plaît en 17 à 50 ms ([recherche.md §4](recherche.md#4-ce-qui-fait--premium--selon-la-recherche-ux)).

| Outil | Ce qu'il donne | Prix | Branchement Claude Code |
|---|---|---|---|
| **[Nutlope/inspo](https://github.com/Nutlope/inspo)** | 832 vrais sites, 2 320 pages captées desktop + mobile, palette, polices, techno détectée, analyse écran par écran, **un DESIGN.md par site**, 68 composants de référence en JSX (heros, pricing, footers…) | gratuit, MIT | MCP : `claude mcp add --transport http inspo https://inspomcp.dev/api/mcp` ou `npx -y inspo-mcp install` |
| **[VoltAgent/awesome-design-md](https://github.com/VoltAgent/awesome-design-md)** | DESIGN.md tirés des design systems de marques connues : on en dépose un et l'agent génère une UI assortie | gratuit, MIT | copier le fichier dans le projet |
| [VoltAgent/official-design-md](https://github.com/VoltAgent/official-design-md) | DESIGN.md publiés par les entreprises elles-mêmes | gratuit | idem |
| [kwakseongjae/oh-my-design](https://github.com/kwakseongjae/oh-my-design) | 500+ références DESIGN.md notées par qualité + skills, une commande | gratuit, MIT | installeur |
| [bergside/awesome-design-skills](https://github.com/bergside/awesome-design-skills) | 67 DESIGN.md et SKILL.md de design | gratuit | copier |
| **Mobbin** | bibliothèque d'écrans d'apps et de sites en production | Pro 10 $/mois en annuel (120 $/an) ou 15 $/mois en trimestriel, pas de mensuel. Team 16 ou 24 $/membre/mois | **MCP officiel, Pro et au-dessus** (absent du Free) |
| **Refero** | références de design, styles | plans Pro, Team, Lifetime | **MCP officiel**, absent du Free |
| Awwwards, Godly, Land-book, Dribbble, Behance | galeries d'inspiration | gratuit | captures à la main |

Écarté : `recent.design` + « copier le HTML brut » — on s'inspire, on ne recopie pas.

---

## Extraire un design system

Transformer un site qui te plaît en valeurs concrètes — couleurs, typo, espacements,
rayons, ombres — sans les inventer. On ne prend que des valeurs, pas le design.

| Outil | Ce qu'il sort | Prix | Branchement |
|---|---|---|---|
| **[designlang](https://github.com/Manavarya09/design-extract)** (repo design-extract, 4,2k★) | 8 fichiers (17+ en CLI seul) : markdown pensé pour l'IA, **config Tailwind**, **thème shadcn/ui**, variables Figma, tokens W3C, variables CSS. Aussi SwiftUI, Compose, Flutter. Audit CSS, correction WCAG | gratuit, MIT | `/plugin marketplace add Manavarya09/design-extract` puis `/plugin install designlang@designlang`, commande `/extract <url>`. Ou `npx skills add Manavarya09/design-extract`. Une fois : `npx designlang install-browser` |
| [dembrandt](https://github.com/dembrandt/dembrandt) (3,6k★) | logo, couleurs, typo, espacements, bordures, ombres, mouvement, composants → tokens W3C. Peut vérifier le respect du système en CI | gratuit, MIT | `npm install -g dembrandt` |
| [bergside/design-md-chrome](https://github.com/bergside/design-md-chrome) | extension Chrome : styles d'un site → DESIGN.md | gratuit | navigateur |
| Google Stitch | « extract from URL » | voir plus bas | MCP Stitch |
| `/impeccable extract` | dans le système d'un projet impeccable | — | [stack.md](stack.md) |

Options utiles de designlang : `--screenshots`, `--depth N` (plusieurs pages),
`--dark`, `--wait` (pour les SPA).

---

## Explorer des directions

L'étape qui manque après impeccable : **voir** 3 à 5 directions et en choisir une,
au lieu de la décrire en mots.

### Claude Design

Le premier choix, parce qu'il est déjà payé et branché sur Claude Code.

- **Disponibilité** : inclus dans **tous les plans, Free compris**, depuis le
  16/09/2026, sans prix séparé — consomme les limites partagées du plan, puis des
  crédits d'usage. Enterprise : activé par défaut le 15/10/2026. Le site séparé
  `claude.ai/design` ferme le **14/12/2026** : ensuite, tout passe par une
  conversation, Claude Code ou l'onglet Artifacts.
- **Dans Claude Code** : `/design` ouvre une session, **`/design-sync`** importe le
  design system depuis la base de code locale.
- **Construit un design system** en lisant la base de code et les fichiers de
  design, ou à partir d'un repo GitHub, de fichiers envoyés (images, DOCX, PPTX,
  XLSX), d'une capture web. Vérifie ensuite ce qu'il produit contre ce système.
- **Sur le canevas** : commentaires sur un élément, édition directe du texte,
  curseurs de réglage générés par Claude (espacement, couleur), glisser /
  redimensionner / aligner.
- **Exports** : .zip, PDF, PPTX, Google Slides, HTML autonome, Canva. 15
  intégrations (Adobe, Vercel, Miro, Lovable, v0, Netlify, Wix…).
- **Passage au code** : un « handoff bundle » envoyé à Claude Code, en local ou sur
  le Web.
- Lancé le 17/04/2026 (Anthropic Labs, Opus 4.7), toujours en preview. Le contenu
  du bundle et la fidélité des exports ne sont documentés par personne d'autre
  qu'Anthropic.

Sources : [annonce](https://www.anthropic.com/news/claude-design-anthropic-labs),
[aide](https://support.claude.com/en/articles/14604416-get-started-with-claude-design),
[release notes](https://support.claude.com/en/articles/12138966-release-notes).

### Google Stitch

Ex-Galileo AI, racheté par Google en 2025, refondu le 18/03/2026.

- Canevas infini qui prend captures, texte, code et références concurrentes.
- **Agent Manager** : plusieurs directions visuelles menées en parallèle.
- Jusqu'à 5 écrans liés d'un coup (source secondaire), export Figma en calques
  éditables, à sens unique.
- **DESIGN.md** en export et import. Skills Google pour Claude Code :
  `npx plugins add google-labs-code/stitch-skills --target claude-code`
  (`design-md`, `extract-design-md`, `manage-design-system`). Claude Code ne lit pas
  ce fichier tout seul : le référencer dans `CLAUDE.md`.
- **MCP** officiel (entrée HTTP avec en-tête `X-Goog-Api-Key`), ou proxy communautaire
  `npx @_davideast/stitch-mcp proxy` après `gcloud auth application-default login`.
  Le proxy ajoute `get_screen_code` (HTML), `get_screen_image` (capture) et
  `build_site`. Frictions : jeton gcloud qui expire en quelques heures, un `.env`
  dans le dossier de lancement fait planter le proxy.
- Gratuit tant qu'il reste dans Google Labs (selon des blogs, non confirmé par
  Google). Expérimental, sans engagement de service.

### Les autres

| Outil | Pour quoi | Prix | Branchement |
|---|---|---|---|
| **Figma Make** | le choix sûr si le design system vit dans Figma | Figma Professional 16 $/siège/mois en annuel, 3 000 crédits/mois, un prompt complexe coûte 60 à 340 crédits (environ 50 à 70 prompts/mois) | — |
| **Magic Patterns** | part du design system existant, sort du React/Tailwind, export Figma | Starter 20 $/siège, 1 000 crédits. Import de design system sur plan payant | MCP compatible Claude Code |
| **Nano Banana Pro** (Gemini 3 Pro Image) | maquettes en image pour fixer un « look » | API Gemini, payante pour l'EEE | une commande slash qui appelle l'API — témoignage unique, voir [recherche.md §5](recherche.md#5-images-et-vidéo-générées-par-ia) |
| [nexu-io/open-design](https://github.com/nexu-io/open-design) | alternative locale à Claude Design, images et vidéo | Apache-2.0, mais pousse une offre payante et des clés de fournisseurs | écarté : trop lourd pour ce besoin |

---

## Figer la direction

Le résultat de l'exploration doit tenir dans **un fichier** que les agents lisent.

| Format | D'où | Note |
|---|---|---|
| `DESIGN.md` | impeccable, Stitch, inspo, awesome-design-md, designlang | format ouvert, passe d'un outil à l'autre. **Référencer dans `CLAUDE.md`** |
| `PRODUCT.md` | `/impeccable init` | public, registre `brand` / `product`, voix. Sans lui chaque session redevine |
| tokens W3C / config Tailwind / thème shadcn | designlang, dembrandt | les valeurs concrètes |
| Variables Figma | Figma, designlang | si on passe par Figma |

La méthode des studios (A List Apart, Samantha Warren) : références et moodboard →
**style tile** (une planche qui fixe polices, couleurs et styles d'éléments, plus
aboutie qu'un moodboard, moins qu'une maquette) → tokens. Pour une IA, la style
tile est l'entrée idéale de la spec.

### Passage Figma → Claude Code

Pour qui a un fichier Figma : [serveur MCP distant officiel](https://help.figma.com/hc/en-us/articles/35281350665623)
(recommandé plutôt que le serveur desktop), Claude Code supporté, et la skill
`implement-design` (repo figma/mcp-server-guide) qui lit les propriétés exactes des
frames (espacements, fills, typo, tokens) via `get_design_context`. Il faut un
**siège Full ou Dev sur un plan payant** : Professional = 200 appels/jour, Starter
et sièges View/Collab = **6 appels/mois**. Socket et Snyk ont émis des alertes de
sécurité sur la skill : la lire avant de l'installer.

---

## Composants

| Bibliothèque | Pour | Licence / prix | Limites |
|---|---|---|---|
| **shadcn/ui** | toute l'app | MIT, gratuit | — |
| Aceternity UI | landings, effets | composants gratuits ; accès à vie 199 $ (prix barré 299 $, peut-être une promo), 169 $/an, offre équipe | effets 3D qui tirent Three.js, accessibilité basique, couleurs codées en dur |
| Magic UI | landings | — | thème sombre par défaut |
| MCP `magic` (21st.dev) | composants réels à consulter | clé API | du matériau, pas une direction — voir [stack.md](stack.md#le-mcp-21stdev-magic) |
| [shadcn-ui/lint](https://github.com/shadcn-ui/lint) | linter de design system pour agents : des règles que l'agent peut vérifier | — | non évalué |

Recommandation reprise de plusieurs sources : shadcn pour tout le produit,
Aceternity ou Magic UI au cas par cas sur la landing.

---

## Visuels : images et vidéo

| Générateur | Usage commercial | À savoir |
|---|---|---|
| **GPT Image** (OpenAI) | oui | pas d'exclusivité |
| **Nano Banana** (API Gemini) | oui par déduction | pas d'exclusivité, payant pour l'EEE |
| Higgsfield | oui | **entraîne ses modèles sur tes contenus par défaut** ; plan gratuit inutilisable (0 crédit, filigrane) |
| Midjourney | oui | **licence perpétuelle** conservée par Midjourney, **public par défaut**, Pro/Mega obligatoire au-delà de 1 M$ de CA |

Détail des conditions : [recherche.md §5](recherche.md#5-images-et-vidéo-générées-par-ia).
Pour un site client ou commercial, préférer GPT Image ou Nano Banana.

**Vidéo hero** : toujours un attribut `poster`, contrôler le LCP (la vidéo devient
en général l'élément mesuré), éviter `autoplay` hors écran.

Repérés dans les favoris, non évalués : [cth9191/motion-design](https://github.com/cth9191/motion-design)
(skill qui produit des films via Higgsfield),
[calesthio/OpenMontage](https://github.com/calesthio/OpenMontage) (production vidéo agentique),
[kaankiziltug/logo-design-skill](https://github.com/kaankiziltug/logo-design-skill)
(logos SVG, 1 400 références). Écarté : `Open-Generative-AI`, qui s'annonce
lui-même « sans filtres de contenu ».

---

## Animation

| Outil | Licence | Règles |
|---|---|---|
| **GSAP** + ScrollTrigger | gratuit depuis avril 2025, usage commercial et plugins compris. Licence propriétaire : seule restriction gênante, bâtir un outil concurrent de Webflow | — |
| **Lenis** (défilement lissé) | MIT | le défilement lissé détourne le scroll natif : tester l'accessibilité |
| Motion (ex Framer Motion) | non vérifiée | — |

Règles confirmées, quel que soit l'outil :

- animer **seulement `transform` et `opacity`** — `top` / `left` dégradent le CLS ;
- **`prefers-reduced-motion`** : le W3C cite le parallaxe et le mouvement au scroll
  comme causes de vertiges ;
- une animation qui démarre seule et dure plus de 5 s doit pouvoir être mise en
  pause (WCAG 2.2.2, niveau A).

Côté skills : `emil-design-eng` fait autorité sur le mouvement
([stack.md](stack.md#emil-design-eng)). Recettes maison : `awwwards-motion-site`,
`cinematic-scroll-site`. Repérés, non évalués :
[nateherkai/scroll-craft](https://github.com/nateherkai/scroll-craft) (dirige aussi le
reste, voir stack.md), [oso95/scroll-world](https://github.com/oso95/scroll-world),
[robonuggets/cinematic-site-components](https://github.com/robonuggets/cinematic-site-components),
[DavidHDev/canvas-ui](https://github.com/DavidHDev/canvas-ui),
[MengTo/threeui](https://github.com/MengTo/threeui).

---

## Critique visuelle

| Outil | Ce qu'il fait |
|---|---|
| **`visual-check`** (maison) | captures, erreurs console, clics, Playwright dans un conteneur, rien installé dans le projet — [skills.md](../skills.md) |
| design-loop (jezweb) | sert le site, captures à **1280 px et 375 px**, les compare au design system et corrige. Comparaison par le modèle qui regarde, pas pixel par pixel |
| [OneRedOak/claude-code-workflows](https://github.com/OneRedOak/claude-code-workflows) | Design Review Workflow : Playwright MCP + agents dédiés, cohérence UI/UX, accessibilité, standards, sur chaque changement front (~3,9k★) |
| `web-design-guidelines` (Vercel) | 100+ règles a11y / perf / UX sur du code existant — [stack.md](stack.md) |
| [vercel-labs/web-interface-guidelines](https://github.com/vercel-labs/web-interface-guidelines) | les guidelines elles-mêmes |
| **`gauntlet-loop`** (maison) | builders en parallèle, critique dans un contexte neuf, comparaison A/B à l'aveugle — c'est la forme que la recherche appuie ([recherche.md §3](recherche.md#3-la-méthode)) |

Aucun de ces outils n'a de mesure d'efficacité publiée.

---

## Skills « anti-slop » concurrents d'impeccable

Repérés, non installés. Ils font le même travail qu'un directeur : **en prendre un
seul**, voir la règle « un directeur par surface » de [stack.md](stack.md).

| Skill | Note |
|---|---|
| [Nutlope/hallmark](https://github.com/Nutlope/hallmark) | Together AI. Choisit une structure de page, l'habille d'un des 21 thèmes, 57 contrôles anti-slop et une auto-critique avant de rendre |
| [agiwhitelist/auteur](https://github.com/agiwhitelist/auteur) | direction artistique figée avant le code, visuels générés par des CLI locaux, linter anti-slop exécutable et contrôle du mouvement qui bloquent chaque livraison. Le plus proche d'un processus complet. Jeune (1k★) |
| [superdesigndev/superdesign-skill](https://github.com/superdesigndev/superdesign-skill) | appuyé sur le service superdesign.dev |
| [educlopez/ui-craft](https://github.com/educlopez/ui-craft) | « design engineering system » |
| [ibelick/ui-skills](https://github.com/ibelick/ui-skills), [emilkowalski/skills](https://github.com/emilkowalski/skills) | skills de design engineer |
| [joeseesun/qiaomu-design](https://github.com/joeseesun/qiaomu-design) | conseiller anti-générique, « cabine d'essayage » de styles, 58 design systems |
| [miqdadbadjuber/anti-slop](https://github.com/miqdadbadjuber/anti-slop) | règles contre l'UI, le texte et le code génériques |

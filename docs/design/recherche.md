# Ce que dit la recherche — preuves, verdicts, sources

Relevé des 9 et 10 octobre 2026. Cinq recherches web (workflow `deep-research` :
recherche en éventail, lecture des sources, chaque affirmation soumise à trois
vérificateurs, deux refus suffisent à l'écarter), un passage dans les favoris
GitHub et sur GitHub (`prior-art`), et un rapport externe compilé à partir de
vidéos YouTube et de posts X, vérifié point par point.

**Comment lire ce fichier.** Chaque point porte un verdict :

| Verdict | Sens |
|---|---|
| **confirmé** | source primaire (doc de l'éditeur, étude publiée, repo) qui le dit |
| **partiel** | vrai en partie, ou appuyé indirectement |
| **non étayé** | aucune affirmation n'a passé la vérification — ce qui ne veut **pas** dire faux |
| **réfuté** | écarté par les vérificateurs (2 ou 3 votes contre 3) |

Les prix, quotas et conditions d'utilisation changent souvent : tout est daté
d'octobre 2026.

---

## 1. Le constat de départ

**Laissé seul, un LLM produit du générique** — confirmé.

- Anthropic l'écrit lui-même : sans consigne, Claude retombe sur les choix les plus
  fréquents de ses données d'entraînement — police Inter, dégradés violets sur fond
  blanc, grilles de cartes arrondies. C'est la raison d'être du skill
  `frontend-design` ([blog Anthropic, 12/11/2025](https://claude.com/blog/improving-frontend-design-through-skills),
  [cookbook](https://platform.claude.com/cookbook/coding-prompting-for-frontend-aesthetics) :
  « defaults to safe choices unless explicitly encouraged otherwise »).
- Search Engine Journal (mai 2026) : « if you leave the choices to an LLM you will
  100% get the most common design choices », et « the human is now the editor ».
- Test de l'agence ted&gustaf (2026) : la même idée de landing donnée à Figma Make,
  Lovable, Stitch, Replit et Relume. Presque tous sortent une page complète en
  quelques minutes, avec les mêmes défauts : boutons d'action génériques, message
  faible, composants incohérents, espacements et hiérarchie ratés. Test informel,
  sans méthode, par une agence qui a intérêt à dire que les designers restent
  utiles.

**Conséquence** : la qualité vient de décisions prises **avant** de générer, et
d'un humain qui trie. Pas de l'outil de génération.

---

## 2. Les skills de design

### Ce qu'ils contiennent — confirmé

| Skill | Contenu vérifié |
|---|---|
| `frontend-design` (Anthropic) | prompt d'environ 400 tokens sur 4 axes : typographie, couleur et thème, animation, arrière-plans. Interdit Inter, Roboto, Arial, les polices système, les dégradés violets sur blanc |
| `impeccable` (pbakaus) | 1 skill, 24 commandes, 59 règles de détection des tics visuels de l'IA, fichiers `PRODUCT.md` et `DESIGN.md` persistants. Part de `frontend-design` (« Impeccable started from there ») et ajoute des références typo, couleur, espacement, mouvement, interaction, responsive, textes d'interface |
| `design-taste-frontend` (Leonxlnx/taste-skill) | v2 marquée « experimental ». Lit le brief, en déduit un style, règle trois curseurs de 1 à 10 : `DESIGN_VARIANCE`, `MOTION_INTENSITY`, `VISUAL_DENSITY`. La v1 reste dispo sous `design-taste-frontend-v1` |
| `ui-ux-pro-max` | SKILL.md de 214 lignes (~4k tokens) en v2.13.0, plus sa base consultable |

Analyse détaillée de leurs prescriptions et de leurs contradictions : [stack.md](stack.md).

### Est-ce qu'ils améliorent le résultat ? — non étayé

**Aucune mesure n'existe.** Les seules preuves sont des captures avant/après
choisies par les auteurs : 3 paires dans le blog d'Anthropic, 3 dans le cookbook,
2 captures dans le README de taste-skill. Aucune métrique, aucun test à l'aveugle,
aucun échantillon, aucun classement. Le blog d'Anthropic parle de « significant
improvement » sans chiffre. Le dossier `research/` de taste-skill porte sur la
troncature de code par les LLM, pas sur la qualité d'UI. impeccable affiche un
« LCP 3.4s → 1.1s » sans source.

Rien non plus pour Taste, UI/UX Pro Max, emil-kowalski ou apple-design, ni sur
l'intérêt de combiner plusieurs skills.

### Ce que coûte d'en charger plusieurs — confirmé

[Doc officielle des Agent Skills](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) :

| Niveau | Quand | Coût |
|---|---|---|
| 1 — nom et description | toujours, pour chaque skill installé | ~100 tokens (200-250 si la description est longue) |
| 2 — corps du SKILL.md | quand le skill se déclenche | « Under 5k tokens » — ordre de grandeur, pas une limite |
| 3 — fichiers de référence | quand le skill les fait lire | en plus |

Ça s'additionne d'un skill à l'autre. La page des bonnes pratiques dit que chaque
token chargé « competes with conversation history ». Les consignes contradictoires
entre skills ne sont documentées nulle part — mais elles sont **mesurées** ici,
dans [stack.md](stack.md#ce-que-ça-donne-en-vrai--mesuré) : la même police
recommandée par l'un, bannie par l'autre.

---

## 3. La méthode

| Règle | Verdict | Ce qui l'appuie |
|---|---|---|
| Plan mode avant de coder | **confirmé** (recommandé, pas mesuré) | [best practices Claude Code](https://code.claude.com/docs/en/best-practices) : explorer, planifier, coder. « Letting Claude jump straight to coding can produce code that solves the wrong problem ». Sauter le plan si le diff tient en une phrase |
| Se faire interviewer | **confirmé** (idem) | même page : sur une grosse fonctionnalité, « have Claude interview you first » avec AskUserQuestion, UI/UX comprise, écrire une spec, implémenter dans une session neuve |
| Vérifier le rendu en boucle | **confirmé** (idem) | même page, « Verify UI changes visually » : « take a screenshot of the result and compare it to the original. list differences and fix them » |
| Ne jamais accepter le premier jet | **partiel** | voir ci-dessous |
| Note d'auto-évaluation par l'IA | **partiel** | le mécanisme existe (Self-Refine), rien ne montre qu'une note que l'IA se donne améliore une UI |
| Design system avant le prompt | **non étayé** | seul appui indirect : Claude Design importe le design system puis vérifie ce qu'il produit contre lui |
| Hero d'abord, puis section par section | **non étayé** | aucune source |

### Itérer : ce qui marche et ce qui ne marche pas

- **Self-Refine** (NeurIPS 2023) : le même LLM écrit, se critique, se corrige.
  Environ +20 points en moyenne sur 7 tâches de texte et de code. Aucune d'UI, gain
  quasi nul en maths.
- **Huang et al.** (ICLR 2024) : sans retour extérieur, l'autocorrection dégrade
  parfois le raisonnement. CommonSenseQA : de 75,8 % à 38,1 %. GSM8K : 75,9 → 74,7.
- **Code d'UI** (Xiong 2026, Design2Code, préprint) : itérer sans voir le rendu
  gagne +1,5 %, contre +6,2 % pour un tour avec rendu et critique. Laissée libre,
  l'autocorrection n'améliore pas de façon régulière : corriger un défaut visuel en
  casse un autre.
- La doc Claude Code préfère une relecture par **un contexte neuf** (un sous-agent),
  et prévient qu'un relecteur trouve presque toujours des défauts, ce qui pousse à
  en faire trop.

**Ce qu'on en retient** : itérer, oui, mais chaque tour doit s'appuyer sur quelque
chose d'extérieur — le rendu réel, des tests, ou un relecteur qui n'a pas écrit le
code. Une IA qui note son propre travail sans le voir ne vaut rien de prouvé.

Réfutés au vote : une boucle de critique automatique à +17,8 % (+10,8 % pour
Claude 4.5 Sonnet), une itération guidée par grille gagnante dans 15 cas sur 18.

---

## 4. Ce qui fait « premium » selon la recherche UX

| Critère | Verdict | Étude |
|---|---|---|
| Première impression esthétique | **confirmé** | Lindgaard 2006 : jugement de beauté formé en **50 ms**, qui concorde avec celui formé en 500 ms (r = 0,947 sur les moyennes par page, n = 40). L'accord entre individus est bien plus faible (r ≈ 0,56-0,60) |
| Peu chargé + conforme à la catégorie | **confirmé** | Tuch 2012 (119 sites, N = 82) : la complexité visuelle et la conformité à ce qu'on attend d'un site de ce type jouent dès **17 ms** (ηp² = 0,38 et 0,19), vers 0,65 à 50 ms. Les sites peu chargés **et** conformes sont jugés les plus beaux |
| Le look et la crédibilité | **partiel** | Fogg / Stanford 2002 (2 684 participants) : le « design look » est le critère le plus cité dans les commentaires sur la crédibilité (46,1 %). Déclaratif, pas causal. Lindgaard 2011 : un jugement à 50 ms est moins fiable pour la confiance et l'utilisabilité |
| Espace blanc, cohérence | **partiel** | seulement par analogie avec la faible complexité visuelle de Tuch — une interprétation |
| Images | **partiel** | NN/g ([photos as web content](https://www.nngroup.com/articles/photos-as-web-content/), 2010, relu en 2026) : en oculométrie, les gens ignorent les images décoratives et les photos de stock génériques, regardent celles qui informent et les vraies photos de l'équipe. Mesure l'attention, pas la confiance ni la conversion |
| Hiérarchie, typographie, animation, performance, signaux de confiance | **non étayé** | rien n'a passé la vérification (Baymard, Tractinsky, NN/g sur l'effet esthétique-utilisabilité non retenus) |

**Aucune de ces études ne mesure la conversion.** Elles mesurent la beauté perçue
ou ce que les gens déclarent.

**Ce qu'on en retient pour un non-designer** : la première impression se joue en
une fraction de seconde, sur deux choses mesurables — **peu de choses à l'écran**
et **ressembler à ce qu'on attend de ce type de site**. D'où l'intérêt de partir de
références de la même catégorie, plutôt que de chercher l'originalité à tout prix.

---

## 5. Images et vidéo générées par IA

### Licences — confirmé (conditions d'utilisation officielles)

| Générateur | Usage commercial | Pièges |
|---|---|---|
| **Midjourney** | oui, propriétaire « to the fullest extent possible under applicable law » | une entreprise de **plus de 1 M$ de CA** doit être en Pro ou Mega pour être propriétaire. Midjourney garde une **licence perpétuelle, irrévocable, sous-licenciable** sur prompts et images. Contenu **public et remixable par défaut**, sauf mode Stealth (Pro/Mega, « best efforts ») |
| **OpenAI** (ChatGPT, images) | oui, OpenAI cède ses droits « if any » | pas d'exclusivité : un autre peut obtenir une image similaire. Interdit de la présenter comme faite par un humain. Conditions propres à Codex et à l'API image non vérifiées |
| **Google** (API Gemini, Nano Banana) | permis par déduction (rien ne l'interdit) | Google peut générer la même chose pour d'autres. API réservée à un usage professionnel ; service payant obligatoire pour des utilisateurs dans l'EEE. App grand public et Veo non vérifiées |
| **Higgsfield** | oui, sans condition de plan | plan gratuit à 0 crédit avec filigrane, donc inutilisable en pratique. **Tes contenus entraînent leurs modèles par défaut** (sauf entreprise) |

Aucun ne garantit l'exclusivité ni un droit d'auteur que tu pourrais faire valoir.
Non vérifiés : Runway, Kling, Veo, la position du US Copyright Office et du droit
européen, l'existence d'un MCP Higgsfield, les prix actuels.

### Est-ce que des visuels sur mesure font plus premium ? — non étayé

Le rapport externe en fait le levier qui fait passer de « bien » à « waouh ». Aucune
étude ni A/B test publié ne le confirme. Le seul appui est l'étude NN/g ci-dessus :
les photos de stock génériques sont ignorées.

Un témoignage (blog, novembre 2025, un seul développeur) : une commande
`/nano-banana` dans Claude Code qui génère des maquettes, puis le design system
implémenté d'après elles. Sa conclusion : « make it more premium » est flou en mots
et évident en image. Sa limite : la maquette donne une direction, pas une spec — la
typo, les espacements et les composants restent à décider.

### Vidéo hero et performance — confirmé

- Depuis Chrome 116 (août 2023), une vidéo peut être l'élément LCP (Largest
  Contentful Paint, le temps d'affichage du plus gros élément, mesuré par Google),
  horodatée à sa première image affichée. Une grande vidéo en `autoplay` devient
  donc en général l'élément LCP ([changelog Chromium](https://chromium.googlesource.com/chromium/src/+/main/docs/speed/metrics_changelog/2023_08_lcp.md)).
- `autoplay` lance le téléchargement tout de suite, même hors écran.
  [web.dev](https://web.dev/learn/performance/video-performance) conseille de ne
  l'utiliser qu'en cas de besoin, avec un attribut `poster`.

### Captures d'écran comme source — partiel

Une capture ne montre qu'un état, à une largeur, sans structure : survol, focus,
HTML et responsive sont devinés. Quand la page de référence est en ligne, extraire
son vrai DOM (designlang, dembrandt) donne plus d'information. Le chiffre de 70 à
80 % de fidélité des outils capture → code a été réfuté.

---

## 6. Animation

| Point | Verdict | Détail |
|---|---|---|
| GSAP gratuit | **confirmé** | depuis le 30 avril 2025 (rachat par Webflow), tout GSAP est gratuit pour tous, usage commercial compris, anciens plugins payants inclus (SplitText, MorphSVG…). Licence **propriétaire**, pas open source : interdit de l'utiliser dans un outil d'animation sans code concurrent de Webflow, de faire de la rétro-ingénierie pour un produit concurrent, de retirer les mentions. Le code généré par IA est explicitement autorisé ([licence](https://gsap.com/community/standard-license/)) |
| Lenis | **confirmé** | bibliothèque de défilement lissé de darkroom.engineering, **MIT**, v1.3.26. Poids et problèmes d'accessibilité propres non vérifiés |
| Coût sur la mise en page | **confirmé** | animer `top` ou `left` crée des décalages comptés dans le CLS (Cumulative Layout Shift, le score de stabilité de la page), même sur un calque à part. `transform` (translate, scale, rotate, skew) ne compte pas. web.dev : se limiter à `opacity` et `transform`. Un décalage dans les 500 ms après une action de l'utilisateur n'est pas compté |
| Accessibilité | **confirmé** | WCAG 2.2 critère 2.3.3 (pouvoir couper une animation déclenchée par une interaction) : niveau **AAA**, donc pas exigé par les cibles AA courantes (RGAA, EN 301 549). Le W3C cite le parallaxe et le mouvement au scroll comme causes de vertiges, nausées et maux de tête chez les personnes atteintes de troubles vestibulaires. Le critère 2.2.2 (niveau **A**) s'applique à une animation qui démarre seule et dure plus de 5 s |
| « Stack de référence » GSAP + ScrollTrigger + Lenis | **non étayé** | avis d'influenceurs |
| Effet de l'animation sur la conversion ou la qualité perçue | **non étayé** | rien |
| Licence de Motion (ex Framer Motion), effet sur l'INP | **non étayé** | non vérifié |

---

## 7. Outils

| Outil | Verdict | Détail |
|---|---|---|
| Claude Design | **confirmé** | voir [outils.md](outils.md#claude-design) — inclus dans tous les plans depuis le 16/09/2026 |
| Figma MCP + skill `implement-design` | **confirmé** | serveur MCP distant officiel, Claude Code supporté. Siège Full ou Dev payant. Socket et Snyk ont émis des alertes de sécurité sur la skill |
| Google Stitch | **confirmé** (fonctions), **partiel** (gratuité) | refonte du 18/03/2026, canevas, Agent Manager, DESIGN.md, MCP et SDK. La gratuité ne repose que sur des blogs ; « 350 générations gratuites par mois » réfuté tel quel |
| Mobbin et Refero | **confirmé** | chacun a un MCP officiel, seulement en payant |
| designlang (design-extract) | **confirmé** | voir [outils.md](outils.md#extraire-un-design-system) |
| Figma Make, Magic Patterns | **confirmé** (prix) | voir [outils.md](outils.md#explorer-des-directions) |
| shadcn/ui, Aceternity, Magic UI | **confirmé** | voir [outils.md](outils.md#composants) |
| 21st.dev, Paper, recent.design, getdesign.md, styles.refero.design, Skillry | **non étayé** | ni l'existence, ni l'offre, ni les prix n'ont passé la vérification. 21st.dev et son MCP `magic` sont par ailleurs installés et documentés dans [stack.md](stack.md#le-mcp-21stdev-magic) |
| v0, Framer, Webflow, Relume, Tailwind Plus, Lovable | **non étayé / réfuté** | prix de v0 réfutés, « Lovable donne les meilleurs visuels » réfuté |

---

## 8. Mobile

Presque rien de vérifié. Seul le principe des design tokens partagés entre web, iOS
et Android est confirmé (le studio Yummygum les stocke comme Variables Figma pour
garder les plateformes cohérentes). Pistes repérées dans GitHub, non vérifiées :

- [Meliwat/awesome-ios-design-md](https://github.com/Meliwat/awesome-ios-design-md) — 200 DESIGN.md d'apps, avec variantes SwiftUI, Jetpack Compose et Expo ;
- [sleekdotdesign/agent-skills](https://github.com/sleekdotdesign/agent-skills) — skill officiel Sleek pour créer et éditer des écrans d'app mobile ;
- `animate-expo` dans [emilkowalski/skills](https://github.com/emilkowalski/skills) ;
- [lnkiai/m3e-canvas](https://github.com/lnkiai/m3e-canvas) — croquis Material 3 Expressive transformés en prompts.

Reste ouvert : kits UI Expo / React Native (NativeWind, Tamagui, gluestack),
générateurs d'écrans mobiles, Figma vers React Native.

---

## 9. Le rapport externe, point par point

Rapport compilé le 10/10/2026 à partir de vidéos YouTube (Yashika Jain, Riko Nazza,
Mikey Website, AI LABS, Coriace…), d'articles (Anthropic, Sergei Chyrkov, Pietro
Montaldo, Medium) et de posts X. Ce qu'il dit, et ce qui en reste :

| Affirmation du rapport | Verdict |
|---|---|
| Le premier jet de l'IA est générique | **confirmé** |
| Claude Design : canevas, design system, commentaires, curseurs, exports, passage à Claude Code | **confirmé**, sauf : « Tweaks » n'est pas le nom officiel, Figma et les captures ne sont pas cités par Anthropic. Le réserver aux plans payants est **périmé** |
| Combo Taste + Impeccable + Frontend Design (+ emil ou apple-design) | **non étayé** — et [stack.md](stack.md) mesure des contradictions entre eux |
| Ne pas installer plus de 2 à 4 skills | **partiel** — le coût en contexte est réel et documenté, le seuil est arbitraire |
| Visuels sur mesure = boost énorme | **non étayé** |
| GSAP + ScrollTrigger + Lenis | licences **confirmées**, « référence » **non étayé** |
| Mobbin MCP, Refero | **confirmé** (payants) |
| 21st.dev, recent.design, getdesign.md, Skillry, Paper | **non étayé** |
| Design system d'abord, hero d'abord | **non étayé** |
| Plan mode + questions | **confirmé** |
| Auto-audit noté sur 100 | **partiel** — préférer une critique sur capture par un contexte neuf |
| Ses propres « déductions » (design system > prompt, assets > tout, rythme > quantité) | opinions de l'auteur, non vérifiables |

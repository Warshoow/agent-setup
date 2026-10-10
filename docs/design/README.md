# Design

Tout ce qui a été récolté sur le design d'interfaces construites par des agents :
quels skills, quels outils, quel processus, et ce que la recherche appuie vraiment.
Point de départ : un dev qui n'est pas designer, et des rendus qui finissent
« mid-tier » même avec de bons skills.

| Fichier | Ce qu'il contient | Statut |
|---|---|---|
| **[processus.md](processus.md)** | les 9 étapes, de « pas designer » à un rendu qui tient, avec prompts, checklist et place dans la factory | à éprouver |
| **[outils.md](outils.md)** | les outils par étape — références, extraction, exploration (Claude Design, Stitch), visuels, animation, critique — avec prix, licences, branchement Claude Code | relevé oct. 2026 |
| **[recherche.md](recherche.md)** | chaque affirmation avec son verdict (confirmé / partiel / non étayé / réfuté) et ses sources : skills, méthode, recherche UX, licences d'images, performance, accessibilité | vérifié |
| **[stack.md](stack.md)** | les skills de design installés ou évalués : qui décide quoi, ce qui a été mesuré, ce qu'il ne faut pas mélanger, l'index des repos | mesuré |

---

## L'essentiel en dix lignes

1. **Un LLM seul fait du générique** — Inter, dégradé violet, trois cartes. Anthropic le dit lui-même.
2. **Aucun skill de design n'a de preuve mesurée** d'amélioration : seulement des avant/après choisis par leurs auteurs.
3. **Ce qui manque après impeccable, c'est choisir une direction** — voir 3 options en image et en garder une. impeccable polit, il ne choisit pas.
4. **Claude Design** est inclus dans tous les plans depuis le 16/09/2026, avec `/design` et `/design-sync` dans Claude Code. C'est l'outil de cette étape.
5. **Partir de références de la même catégorie** : la beauté perçue se joue en 17-50 ms, sur « peu chargé » et « conforme à ce qu'on attend » (Lindgaard 2006, Tuch 2012).
6. **Figer la direction dans `DESIGN.md`**, référencé dans `CLAUDE.md`, avec `PRODUCT.md` (`/impeccable init`).
7. **Un seul directeur par surface** : deux skills de direction se contredisent sur les polices, les cartes, les fonds (mesuré dans stack.md).
8. **Itérer sur le rendu, critiqué par un contexte neuf** : +6,2 % avec rendu contre +1,5 % sans ; une IA qui se note sans voir peut dégrader.
9. **Images IA** : GPT Image ou Nano Banana pour du commercial. Midjourney garde une licence perpétuelle et publie par défaut. Aucune exclusivité nulle part.
10. **Animation** : GSAP est gratuit, n'animer que `transform` et `opacity`, toujours `prefers-reduced-motion`.

Non étayé à ce jour, donc à tester plutôt qu'à croire : que des visuels sur mesure
ou de l'animation augmentent la conversion, « hero d'abord », « design system
d'abord », l'intérêt de combiner plusieurs skills, et tout le mobile.

---

## Sources de ce dossier

- Analyse mesurée des skills (runs `claude -p`, comparaison des prescriptions) — stack.md.
- Cinq recherches `deep-research` des 9 et 10/10/2026 : design premium web et
  mobile ; outils IA pour non-designer ; vérification d'un rapport externe ; deux
  passes ciblées (skills, méthode, recherche UX / visuels, animation, outils).
- Passage `prior-art` dans les 820 favoris GitHub puis sur GitHub (topics design,
  anti-slop, DESIGN.md, extraction de design system).
- Un rapport externe compilé à partir de vidéos YouTube et de posts X — vérifié
  point par point dans [recherche.md §9](recherche.md#9-le-rapport-externe-point-par-point).

---
name: evolve
description: Promouvoir les patterns récurrents de la mémoire persistante vers leur bonne destination — une skill dans ~/skills/ si on l'invoque, une règle CLAUDE.md si c'est un réflexe permanent, ou l'enrichissement d'une skill/d'un agent existant. Relit les mémoires de tous les projets (configs pro et perso), détecte les feedbacks/procédures revenus plusieurs fois, propose (validation explicite avant toute création). Trigger : /evolve, « promeus mes mémoires », « qu'est-ce qui mériterait de devenir une skill ? ».
---

# Evolve — instinct → skill

Ce qui se répète dans la mémoire doit finir en skill (ou en CLAUDE.md), pas
rester en notes dispersées. Inspiré du système d'instincts d'ECC, version
minimale : pas de hooks, pas de scores — la mémoire existante EST l'observation,
il ne manque que la promotion.

## Procédure

1. **Collecte.** Lister les mémoires de la config : `~/.claude/projects/*/memory/*.md`.
   Dans un devcontainer, la config de l'hôte est montée au même chemin absolu ; si
   elle est absente, faire avec ce qui est là et le signaler dans le rapport. Lire en priorité `type: feedback` et
   `type: user`, puis `project`. Ignorer les mémoires contenant déjà le marqueur
   `Promu (evolve)`, **quelle que soit la destination** de cette promotion.

2. **Détection.** Un candidat à la promotion doit cocher les trois cases :
   - **récurrent** : la même consigne/correction/procédure apparaît dans ≥ 3
     mémoires ou buckets de projets différents (une bonne idée vue une fois
     reste une mémoire) ;
   - **actionnable** : c'est un « comment faire » reproductible, pas un simple
     fait ou une préférence ponctuelle ;
   - **cross-projet** : si c'est spécifique à un projet, la destination est le
     CLAUDE.md de ce projet — le proposer comme tel, pas comme skill.
   Écarter ce qui est déjà couvert : `ls ~/skills/` + skills et agents listés
   dans la session. En cas de recouvrement partiel, proposer d'**enrichir**
   l'existant plutôt que de créer un doublon.

3. **Proposition.** Présenter les candidats via AskUserQuestion (multiSelect),
   chacun avec **sa destination** (skill, CLAUDE.md global, CLAUDE.md d'un projet,
   ou enrichissement d'une skill/d'un agent existant), un nom kebab-case, la
   description projetée si c'est une skill, et une ligne de justification citant
   les mémoires sources. **Ne rien créer sans sélection explicite.** Zéro candidat
   solide = le dire et s'arrêter là.

4. **Promotion.** Selon la destination retenue :
   - **skill** : créer `~/skills/<nom>/SKILL.md` — frontmatter `name` +
     `description` (les triggers vivent dans la description), corps concis :
     quand, procédure, exemples concrets tirés des mémoires sources ; puis
     symlinker : `ln -sfn ~/skills/<nom> ~/.claude/skills/<nom>`.
   - **règle CLAUDE.md** (global ou projet) : une section courte, des exemples
     tirés des mémoires sources. C'est la bonne destination pour un réflexe
     permanent — quelque chose qu'on n'invoque jamais mais qui doit toujours
     être chargé. Une skill qu'on n'invoque pas est une skill morte.
   - **enrichissement** d'une skill ou d'un agent existant : la plus petite
     addition qui couvre le pattern, sans dupliquer ce qui est déjà écrit.

   Puis, dans tous les cas, marquer chaque mémoire source en ajoutant :

   ```
   **Promu (evolve)** le <date> → <destination>.
   ```

   où `<destination>` est `skill [[<nom>]]`, `CLAUDE.md global, section « X »`,
   `CLAUDE.md du projet <p>`, ou `enrichissement de <skill|agent>`. C'est ce
   marqueur, et lui seul, que relit l'étape 1 — ne pas en inventer d'autre.

5. **Rapport.** Ce qui a été créé, ce qui a été écarté et pourquoi, et les
   patterns « en incubation » (2 occurrences — à surveiller au prochain /evolve).

## Garde-fous

- Une skill = une procédure **qu'on invoque**. Un réflexe permanent va dans un
  CLAUDE.md, pas dans une skill. Pas de fourre-tout.
- La barre des 3 occurrences est dure : mieux vaut zéro promotion qu'une skill
  morte. Chaque skill ajoutée dilue le routage automatique de toutes les autres.
- Jamais de suppression ou réécriture de mémoire au-delà de l'ajout de la
  mention de promotion.

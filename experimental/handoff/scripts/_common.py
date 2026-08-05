"""Helpers partages entre handoff_write.py et handoff_read.py. Stdlib uniquement."""

import json
import os
import re
from pathlib import Path

STORE_DIRNAME = ".handoff"


def store_dir(create=False):
    """Localise .handoff/ en remontant depuis cwd jusqu'a une racine de projet.

    Ordre: $HANDOFF_DIR > un .handoff existant en remontant > a cote du premier
    .git rencontre > cwd. Remonter evite qu'un agent lance depuis un
    sous-repertoire ecrive dans un store parallele invisible des autres.
    """
    env = os.environ.get("HANDOFF_DIR")
    if env:
        p = Path(env).expanduser().resolve()
        if create:
            p.mkdir(parents=True, exist_ok=True)
        return p

    cwd = Path.cwd().resolve()
    git_root = None
    for parent in [cwd, *cwd.parents]:
        if (parent / STORE_DIRNAME).is_dir():
            return parent / STORE_DIRNAME
        if git_root is None and (parent / ".git").exists():
            git_root = parent

    target = (git_root or cwd) / STORE_DIRNAME
    if create:
        target.mkdir(parents=True, exist_ok=True)
    return target


def load_all(path=None):
    """Charge tous les handoffs, tries par date de creation croissante.

    Un fichier illisible n'interrompt pas la lecture: il est signale et ignore,
    sinon un seul JSON corrompu rendrait toute la memoire inaccessible.
    """
    d = path or store_dir()
    if not d.is_dir():
        return [], []
    records, broken = [], []
    for f in sorted(d.glob("*.json")):
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
            data["_path"] = str(f)
            records.append(data)
        except Exception as e:
            broken.append((f.name, str(e)))
    records.sort(key=lambda r: r.get("created_at", ""))
    return records, broken


def slug(text, maxlen=32):
    s = re.sub(r"[^a-zA-Z0-9]+", "-", (text or "").lower()).strip("-")
    return (s[:maxlen].rstrip("-")) or "untitled"

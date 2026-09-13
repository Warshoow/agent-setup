#!/usr/bin/env python3
"""PreToolUse : bloque la lecture pleine d'un gros fichier, via Read ou via Bash
(cat / head / tail / sed sans borne). exit 2 = bloque, stderr renvoye au modele."""
import json, os, re, shlex, sys

MAX = int(os.environ.get("BIG_READ_MAX", 350))
READERS = {"cat", "head", "tail", "sed"}


def nlines(p):
    try:
        with open(p, "rb") as f:
            return sum(1 for _ in f)
    except OSError:
        return 0


def refus(p, n, how):
    return (f"{p} : {n} lignes (seuil {MAX}). Lecture pleine bloquee ({how}).\n"
            f"- Pour editer : grep -n pour localiser, puis lire la tranche "
            f"(Read offset/limit, ou sed -n 'D,Fp').\n"
            f"- Pour une question d'ensemble : sous-agent scout (Haiku).")


def check_read(ti):
    p = ti.get("file_path") or ""
    if not p or ti.get("offset") or ti.get("limit") or not os.path.isfile(p):
        return None
    n = nlines(p)
    return refus(p, n, "Read") if n > MAX else None


def bounded(tool, args):
    """La commande demande-t-elle deja une tranche bornee ?"""
    if tool in ("head", "tail"):
        for i, a in enumerate(args):
            if re.fullmatch(r"-\d+", a):
                return int(a[1:]) <= MAX
            if a == "-n" and i + 1 < len(args):
                return re.fullmatch(r"\d+", args[i + 1]) is not None and int(args[i + 1]) <= MAX
        return True  # head/tail nu = 10 lignes
    if tool == "sed":
        s = " ".join(args)
        if "-n" not in args:
            return True  # sed sans -n : c'est une transformation, pas une lecture
        for d, f in re.findall(r"(\d+)\s*,\s*(\d+)\s*p", s):
            if int(f) - int(d) <= MAX:
                return True
        return bool(re.search(r"/.*/\s*p", s))  # slice par motif
    return False  # cat


def check_bash(ti):
    cmd = ti.get("command") or ""
    if any(t in cmd for t in ("|", ">", "<<", "$(", "`")):
        return None  # pipe, redirection, heredoc, substitution : deja cible ou hors conversation
    for part in re.split(r"&&|\|\||;", cmd):
        try:
            args = shlex.split(part)
        except ValueError:
            continue
        while args and (args[0] in ("sudo", "time", "env", "rtk") or "=" in args[0].split()[0][:0]):
            args.pop(0)
        if not args or args[0] not in READERS:
            continue
        tool, rest = args[0], args[1:]
        if bounded(tool, rest):
            continue
        for a in rest:
            if a.startswith("-") or not os.path.isfile(a):
                continue
            n = nlines(a)
            if n > MAX:
                return refus(a, n, tool)
    return None


def verdict(tool_name, ti):
    return check_read(ti) if tool_name == "Read" else check_bash(ti) if tool_name == "Bash" else None


def _test():
    big, small = "/tmp/_brg_big.txt", "/tmp/_brg_small.txt"
    open(big, "w").write("x\n" * 400)
    open(small, "w").write("x\n" * 10)
    T = lambda c: verdict("Bash", {"command": c})
    assert verdict("Read", {"file_path": big})
    assert not verdict("Read", {"file_path": big, "offset": 10})
    assert not verdict("Read", {"file_path": small})
    assert T(f"cat {big}")
    assert T(f"cd /tmp && cat {big}")
    assert not T(f"cat {small}")
    assert not T(f"cat {big} | grep x"), "pipe = deja cible"
    assert not T(f"cat {big} > /tmp/_o"), "redirection = hors conversation"
    assert not T(f"head -20 {big}")
    assert not T(f"head -n 20 {big}")
    assert T(f"head -n 5000 {big}")
    assert not T(f"head {big}")
    assert not T(f"tail -5 {big}")
    assert not T(f"sed -n '10,40p' {big}")
    assert T(f"sed -n 'p' {big}")
    assert not T(f"sed 's/a/b/' {big}"), "sed sans -n = transformation"
    assert not T(f"grep foo {big}")
    assert not T("git status")
    assert not T(f"python3 - <<EOF\ncat {big}\nEOF")
    for f in (big, small):
        os.remove(f)
    print("ok")


if __name__ == "__main__":
    if "--test" in sys.argv:
        _test(); sys.exit(0)
    try:
        d = json.load(sys.stdin)
    except Exception:
        sys.exit(0)
    msg = verdict(d.get("tool_name") or "", d.get("tool_input") or {})
    if msg:
        print(msg, file=sys.stderr)
        sys.exit(2)

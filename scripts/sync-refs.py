#!/usr/bin/env python3
"""Sync references.bib from the Zotero master export (MIRROR mode).

Pipeline (see ~/notes/10-Books/quarto-book-publishing-playbook.md):

    Zotero + Better BibTeX auto-export
      -> ~/Documents/bibs/zotero.bib          (master, 'home of record')
      -> this script, run as a Quarto pre-render hook
      -> references.bib                       (only what this book cites)

MIRROR mode: every key cited in the manuscript is refreshed from the master.
Keys that are cited but absent from the master are *preserved* from the existing
references.bib rather than dropped, so hand-made entries survive a sync. Entries
no longer cited anywhere are removed. Output is sorted by key so diffs stay small.

Cite keys are Better BibTeX keys. Copy them from Zotero (right-click -> Copy
Citation Key); do not invent them.

Usage:
    python3 scripts/sync-refs.py                 # sync, report, exit 0
    python3 scripts/sync-refs.py --check         # report only, write nothing
    python3 scripts/sync-refs.py --strict        # exit 1 if any key is unresolved
    python3 scripts/sync-refs.py --master PATH   # override the master bib
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

DEFAULT_MASTER = Path.home() / "Documents" / "bibs" / "zotero.bib"
PROJECT = Path(__file__).resolve().parent.parent
OUTPUT = PROJECT / "references.bib"

# Directories that never contain manuscript source.
SKIP_DIRS = {"_book", ".quarto", ".git", "_freeze", "scripts", "node_modules"}

# Quarto cross-reference prefixes. `@fig-triple-diamond` is a cross-ref, not a
# citation, and must never be looked up in the bibliography.
XREF_PREFIXES = (
    "fig", "tbl", "eq", "sec", "lst", "thm", "lem", "cor", "prp", "cnj",
    "def", "exm", "exr", "sol", "rem", "nte", "tip", "wrn", "imp", "cau",
)

# Pandoc citation key: starts with a letter/digit/underscore, may contain
# internal punctuation. Deliberately conservative.
CITE_RE = re.compile(r"@([A-Za-z0-9_][A-Za-z0-9_:.#$%&+?<>~/-]*[A-Za-z0-9_])")

FENCED_RE = re.compile(r"^```.*?^```", re.M | re.S)
INLINE_CODE_RE = re.compile(r"`[^`\n]*`")
HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.S)
# Real addresses only. A bare `[-@key]` (suppress-author citation) must NOT look
# like an email, so require a dotted TLD.
EMAIL_RE = re.compile(r"\b[A-Za-z0-9._%+]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}\b")


def is_xref(key: str) -> bool:
    return any(key.startswith(p + "-") for p in XREF_PREFIXES)


def parse_bib(path: Path) -> dict[str, str]:
    """Return {key: raw entry text}, preserving the master's own formatting."""
    if not path.exists():
        return {}
    text = path.read_text(encoding="utf-8", errors="replace")
    entries: dict[str, str] = {}
    starts = [(m.start(), m.group(1)) for m in
              re.finditer(r"^@\w+\s*\{\s*([^,\s]+)\s*,", text, re.M)]
    for i, (pos, key) in enumerate(starts):
        end = starts[i + 1][0] if i + 1 < len(starts) else len(text)
        entries[key] = text[pos:end].rstrip() + "\n"
    return entries


def source_files() -> list[Path]:
    files = []
    for root, dirs, names in os.walk(PROJECT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith(".")]
        for n in names:
            if n.endswith((".qmd", ".md")) and not n.startswith("."):
                files.append(Path(root) / n)
    return sorted(files)


def cited_keys() -> dict[str, set[Path]]:
    """Map each cited key to the set of files citing it."""
    found: dict[str, set[Path]] = {}
    for f in source_files():
        text = f.read_text(encoding="utf-8", errors="replace")
        text = FENCED_RE.sub("", text)
        text = HTML_COMMENT_RE.sub("", text)
        text = INLINE_CODE_RE.sub("", text)
        text = EMAIL_RE.sub("", text)
        for m in CITE_RE.finditer(text):
            key = m.group(1)
            if is_xref(key):
                continue
            found.setdefault(key, set()).add(f.relative_to(PROJECT))
    return found


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--master", type=Path, default=DEFAULT_MASTER)
    ap.add_argument("--check", action="store_true", help="report only; write nothing")
    ap.add_argument("--strict", action="store_true", help="exit 1 on unresolved keys")
    args = ap.parse_args()

    if not args.master.exists():
        print(f"sync-refs: master bib not found: {args.master}", file=sys.stderr)
        print("sync-refs: check the Better BibTeX auto-export target in Zotero.",
              file=sys.stderr)
        return 1

    master = parse_bib(args.master)
    existing = parse_bib(OUTPUT)
    cites = cited_keys()

    resolved, preserved, missing = {}, {}, {}
    for key in sorted(cites):
        if key in master:
            resolved[key] = master[key]
        elif key in existing:
            preserved[key] = existing[key]
        else:
            missing[key] = cites[key]

    dropped = sorted(set(existing) - set(cites))

    out = {**resolved, **preserved}
    header = (
        "% references.bib -- GENERATED by scripts/sync-refs.py. Do not edit by hand.\n"
        "% Cited keys are mirrored from the Zotero Better BibTeX export:\n"
        f"%   {args.master}\n"
        "% Add or correct a source in Zotero, then re-render (or run the script).\n"
        "% Entries cited here but absent from the master are preserved verbatim.\n\n"
    )
    body = "\n".join(out[k] for k in sorted(out, key=str.lower))

    print(f"sync-refs: {len(cites)} keys cited across {len(source_files())} source files")
    print(f"sync-refs: {len(resolved)} refreshed from master, "
          f"{len(preserved)} preserved locally, {len(missing)} unresolved")
    if preserved:
        print("sync-refs: preserved (not in Zotero -- add them there when convenient):")
        for k in sorted(preserved):
            print(f"    {k}")
    if missing:
        print("sync-refs: UNRESOLVED -- no entry in master or references.bib:")
        for k in sorted(missing):
            where = ", ".join(sorted(str(p) for p in missing[k]))
            print(f"    {k}  (cited in {where})")
    if dropped:
        print(f"sync-refs: {len(dropped)} entry/entries no longer cited, removed:")
        for k in dropped:
            print(f"    {k}")

    if args.check:
        print("sync-refs: --check, no file written")
    else:
        new = header + body
        if OUTPUT.exists() and OUTPUT.read_text(encoding="utf-8") == new:
            print("sync-refs: references.bib already current")
        else:
            OUTPUT.write_text(new, encoding="utf-8")
            print(f"sync-refs: wrote {OUTPUT.relative_to(PROJECT)} ({len(out)} entries)")

    return 1 if (missing and args.strict) else 0


if __name__ == "__main__":
    sys.exit(main())

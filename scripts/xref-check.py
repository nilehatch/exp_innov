#!/usr/bin/env python3
"""Check that every internal pointer in the book resolves to something real.

This book links by filename, not by Quarto's `@sec-` cross-references:

    [What Makes a Good Pain Hypothesis](Hypothesize_Pain.qmd#sec-hypothesize-pain-section)

That convention buys stable links across a book with no required reading order.
It costs one thing: **Quarto does not validate it.** Rename a file and every
link to it dies silently — no warning, no build failure, just a 404 on the live
site. Pushing to main publishes, and there is no staging step, so nothing else
stands between a broken link and a reader. This script is that check.

Hard failures (exit 1) — these are shipped defects:

  - a `.qmd` link whose target file does not exist
  - a `#sec-` anchor whose target file exists but does not define it
  - an `@fig-` / `@tbl-` reference with no definition (renders as `?fig-name`)
  - an image path that does not resolve
  - a file listed in `_quarto.yml` but missing on disk
  - the same anchor id defined in two files
  - YAML front matter that is not at line 1, so it is not front matter

Soft findings (reported, exit 0) — judgment, not defects:

  - orphan `#sec-` anchors, defined and never linked
  - files on disk that no part of `_quarto.yml` includes
  - cross-book `../book-*` links, which resolve locally and never on the site
  - link text that no longer matches its target's title (`--drift`)

What is NOT checked, deliberately:

  - external URLs. No network calls; this must run offline and in CI.
  - rendered output. Everything here runs against source, so a link can pass
    and still land oddly once Quarto rewrites paths. Verify in `_book/`.
  - whether a link *should* exist. This finds bad pointers, never missing ones.

    python3 scripts/xref-check.py                    # hard checks, whole book
    python3 scripts/xref-check.py --all              # everything, soft findings in full
    python3 scripts/xref-check.py --drift            # link text vs target titles
    python3 scripts/xref-check.py --rename Old.qmd   # every link that a rename would break
    python3 scripts/xref-check.py --warn-only        # always exit 0 (for a pre-render hook)

Two patterns in here cost us something once, and are commented where they sit:
anchors may share a brace block with classes, and `_quarto.yml` names files in
several shapes. Both were written too strictly the first time and both produced
confident false positives.

Shared verbatim with Make the Call; fix bugs in both, or in neither.
"""
import os
import re
import sys
from collections import defaultdict

SKIP_DIRS = {"_book", "_freeze", ".git", "__pycache__", ".Rproj.user", ".quarto"}

# Quarto cross-reference prefixes. `sec-` is deliberately absent: this family
# links to sections by filename, so a bare @sec- is itself worth reporting.
XREF_PREFIXES = ("fig", "tbl", "eq", "lst", "thm")

# An attribute block may carry an id alongside classes, in any order:
#   {#sec-x}   {.method-header #sec-x}   {#sec-x .unnumbered}   {.a #sec-x .b}
# Matching `\{#...\}` finds only the first form and silently loses the rest.
# That error once reported three live anchors as broken.
BRACE = re.compile(r"\{[^{}\n]*\}")
IDENT = re.compile(r"#([a-zA-Z][\w:-]*)")

LINK = re.compile(r"\[([^\]]*)\]\(([^)\s]+?)(?:\s+\"[^\"]*\")?\)")
MD_IMG = re.compile(r"!\[[^\]]*\]\(([^)\s]+)")
HTML_IMG = re.compile(r'<img[^>]+src="([^"]+)"')

# Words too common to signal that link text matches a title.
STOPWORDS = {"the", "a", "an", "of", "to", "in", "for", "and", "on", "your",
             "this", "that", "is", "it", "with", "at", "as", "by", "from"}


def qmd_files():
    out = []
    for dirpath, dirnames, filenames in os.walk("."):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        out += [os.path.normpath(os.path.join(dirpath, f))
                for f in filenames if f.endswith(".qmd")]
    return sorted(out)


def _blank(m):
    return re.sub(r"[^\n]", " ", m.group(0))


def mask_comments(text):
    """Blank out HTML comments, preserving line numbers.

    Parked content is everywhere in this book — commented-out callouts, worked
    examples held back, front matter disabled in favour of an inline heading.
    An anchor or a link inside `<!-- -->` is not defined and not followed, and
    counting it produces false positives that look exactly like real defects.
    Newlines survive so every reported line number still points at the source.
    """
    return re.sub(r"<!--.*?-->", _blank, text, flags=re.S)


def mask_code(text):
    """Also blank fenced code, for scans that must not read code as prose.

    Kept separate from comment masking because **R chunk labels are real
    definitions and live inside fences**: `#| label: fig-tyranny-market` is how
    every generated figure declares itself. Masking fences before collecting
    labels reports every such figure as an undefined reference — which is
    exactly what happened the first time these two were one function.
    """
    return re.sub(r"^```.*?^```", _blank, text, flags=re.S | re.M)


def load(files):
    """Two views: `raw` has comments masked, `text` also has code masked."""
    raw = {f: mask_comments(open(f, encoding="utf-8", errors="replace").read())
           for f in files}
    return {f: mask_code(t) for f, t in raw.items()}, raw


def lineno(text, pos):
    return text.count("\n", 0, pos) + 1


def collect_anchors(text_of, raw_of):
    """anchor id -> [(file, line)]. Ids are global in a Quarto book."""
    anchors = defaultdict(list)
    per_file = defaultdict(set)
    for f, t in text_of.items():
        for bm in BRACE.finditer(t):
            for m in IDENT.finditer(bm.group(0)):
                anchors[m.group(1)].append((f, lineno(t, bm.start())))
                per_file[f].add(m.group(1))
    # R chunk labels declare figures and tables, and live INSIDE fences, so
    # this reads the code-unmasked view. See mask_code().
    for f, t in raw_of.items():
        for m in re.finditer(r"^\s*#\|\s*label:\s*([\w:-]+)", t, re.M):
            anchors[m.group(1)].append((f, lineno(t, m.start())))
            per_file[f].add(m.group(1))
    return anchors, per_file


def title_of(f, t):
    """Front-matter title if present, else the first H1."""
    m = re.match(r"---\n(.*?)\n---", t, re.S)
    if m:
        y = re.search(r'^title:\s*"?(.+?)"?\s*$', m.group(1), re.M)
        if y:
            return y.group(1).strip()
    h = re.search(r"^#\s+(.+?)\s*$", t, re.M)
    return BRACE.sub("", h.group(1)).strip() if h else None


def section_titles(text_of):
    out = {}
    for f, t in text_of.items():
        for m in re.finditer(r"^#{1,6}\s+(.+?)\s*$", t, re.M):
            head = m.group(1)
            for bm in BRACE.finditer(head):
                for im in IDENT.finditer(bm.group(0)):
                    out[(f, im.group(1))] = BRACE.sub("", head).strip()
    return out


def quarto_listed():
    """Files `_quarto.yml` includes.

    They appear as `- x.qmd`, `- part: x.qmd`, `file: x.qmd` and inside
    `appendices:`. Matching only the bare list form reports five real chapters
    as orphans, which is how this was written the first time.
    """
    if not os.path.exists("_quarto.yml"):
        return None
    listed = set()
    for raw in open("_quarto.yml", encoding="utf-8"):
        if raw.lstrip().startswith("#"):
            continue
        for m in re.finditer(r"([\w./-]+\.qmd)", raw.split(" #")[0]):
            listed.add(os.path.normpath("./" + m.group(1)))
    return listed


def iter_links(f, t):
    d = os.path.dirname(f) or "."
    for m in LINK.finditer(t):
        label, target = m.group(1), m.group(2)
        if target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        path, _, frag = target.partition("#")
        if not path:
            continue
        yield (lineno(t, m.start()), label, target,
               os.path.normpath(os.path.join(d, path)), frag)


def norm_words(s):
    s = re.sub(r"[*_`]", "", s.lower())
    s = re.sub(r"[^a-z0-9 ]", " ", s)
    return {w for w in s.split() if w not in STOPWORDS}


def main(argv):
    flags = {a for a in argv[1:] if a.startswith("--")}
    args = [a for a in argv[1:] if not a.startswith("--")]

    if not os.path.exists("_quarto.yml"):
        print("xref-check — no _quarto.yml here; run from the repo root")
        return 0

    files = qmd_files()
    text_of, raw_of = load(files)
    anchors, per_file = collect_anchors(text_of, raw_of)
    listed = quarto_listed()
    hard, soft = [], []

    # ---- rename worklist -------------------------------------------------
    if "--rename" in flags or args:
        target = args[0] if args else None
        if not target:
            print("xref-check --rename needs a filename")
            return 2
        base = os.path.basename(target)
        hits = []
        for f, t in text_of.items():
            for ln, label, link, resolved, frag in iter_links(f, t):
                if os.path.basename(resolved) == base:
                    hits.append((f, ln, f"[{label}]({link})"))
        # A worklist that lists only markdown links is worse than none: the
        # `_quarto.yml` entry is the one that removes the page from the book.
        for i, raw in enumerate(open("_quarto.yml", encoding="utf-8"), 1):
            if base in raw and not raw.lstrip().startswith("#"):
                hits.append(("_quarto.yml", i, raw.strip()))
        # Bare mentions in prose (no link) will not break, but they will read
        # wrong once the file is renamed, so they belong on the same list.
        for f, t in text_of.items():
            for m in re.finditer(re.escape(base), t):
                ln = lineno(t, m.start())
                if not any(h[0] == f and h[1] == ln for h in hits):
                    hits.append((f, ln, "bare mention: " + t.split("\n")[ln - 1].strip()[:70]))
        hits.sort()
        print(f"xref-check — {len(hits)} reference(s) to {base}\n")
        for f, ln, detail in hits:
            print(f"  {f}:{ln}\n      {detail}")
        if not hits:
            print("  none — safe to rename")
        return 0

    # ---- hard: link targets and anchors ----------------------------------
    for f, t in text_of.items():
        for ln, label, link, resolved, frag in iter_links(f, t):
            if "/book-" in link or "/app-" in link or "/paper-" in link:
                soft.append(("cross-book", f, ln, f"[{label}]({link})"))
                continue
            if not os.path.exists(resolved):
                hard.append(("missing target", f, ln, f"[{label}]({link}) -> {resolved}"))
            elif frag and resolved.endswith(".qmd") and frag not in per_file.get(resolved, ()):
                hard.append(("dead anchor", f, ln,
                             f"[{label}]({link}) -> {resolved} defines no #{frag}"))

    # ---- hard: images ----------------------------------------------------
    for f, t in text_of.items():
        d = os.path.dirname(f) or "."
        for rx in (MD_IMG, HTML_IMG):
            for m in rx.finditer(t):
                src = m.group(1)
                if src.startswith(("http://", "https://", "data:")):
                    continue
                r = os.path.normpath(os.path.join(d, src.partition("#")[0]))
                if not os.path.exists(r):
                    hard.append(("missing image", f, lineno(t, m.start()), f"{src} -> {r}"))

    # ---- hard: undefined @fig-/@tbl- refs --------------------------------
    ref_rx = re.compile(r"(?<![\w`])@((?:%s)-[\w:-]+)" % "|".join(XREF_PREFIXES))
    for f, t in text_of.items():
        # fenced code is already masked by load(); line numbers are intact
        for m in ref_rx.finditer(t):
            lab = m.group(1).rstrip(".,;:)")
            if lab not in anchors:
                hard.append(("undefined ref", f, lineno(t, m.start()), f"@{lab}"))

    # ---- hard: duplicate anchor ids --------------------------------------
    for a, locs in sorted(anchors.items()):
        seen = sorted({(f, ln) for f, ln in locs})
        if len({f for f, _ in seen}) > 1:
            where = "  ".join(f"{f}:{ln}" for f, ln in seen)
            hard.append(("duplicate id", seen[0][0], seen[0][1], f"#{a} also at {where}"))

    # ---- hard: front matter that is not front matter ---------------------
    for f, t in text_of.items():
        if "\n---\n" in t and not t.startswith("---"):
            m = re.search(r"^---\s*$", t, re.M)
            if m and re.search(r"^title:", t[m.end():m.end() + 400], re.M):
                hard.append(("front matter not at line 1", f, lineno(t, m.start()),
                             "title/subtitle will not take effect"))

    # ---- hard: listed but missing ----------------------------------------
    on_disk = {os.path.normpath(f) for f in files}
    for f in sorted(listed - on_disk):
        hard.append(("in _quarto.yml, absent on disk", f, 0, ""))

    # ---- soft ------------------------------------------------------------
    for f in sorted(on_disk - listed):
        soft.append(("not in _quarto.yml", f, 0, ""))
    for f, t in text_of.items():
        for m in re.finditer(r"(?<![\w`])@(sec-[\w:-]+)", t):
            soft.append(("@sec- ref; this family links by filename", f,
                         lineno(t, m.start()), f"@{m.group(1)}"))

    linked = set()
    for f, t in text_of.items():
        for ln, label, link, resolved, frag in iter_links(f, t):
            if frag:
                linked.add((resolved, frag))
    for f in files:
        for a in sorted(per_file.get(f, ())):
            if a.startswith("sec-") and (f, a) not in linked:
                soft.append(("orphan anchor", f, anchors[a][0][1], f"#{a}"))

    # ---- drift -----------------------------------------------------------
    drift = []
    if "--drift" in flags or "--all" in flags:
        sect = section_titles(text_of)
        titles = {f: title_of(f, t) for f, t in text_of.items()}
        for f, t in text_of.items():
            for ln, label, link, resolved, frag in iter_links(f, t):
                if resolved not in titles:
                    continue
                actual = sect.get((resolved, frag)) or titles[resolved]
                if not actual:
                    continue
                a, b = norm_words(label), norm_words(actual)
                if not a or not b:
                    continue
                ov = len(a & b) / max(1, min(len(a), len(b)))
                if ov < 0.5:
                    drift.append((ov, f, ln, label, link, actual))
        drift.sort()

    # ---- report ----------------------------------------------------------
    if "--drift" in flags and "--all" not in flags:
        print(f"xref-check --drift — {len(drift)} link(s) whose text may not match the target\n")
        for ov, f, ln, label, link, actual in drift:
            print(f"  {f}:{ln}\n      text   \"{label}\"\n      target {link}\n      titled \"{actual}\"")
        return 0

    print(f"xref-check — {len(files)} files, {len(anchors)} ids")

    if hard:
        print(f"\n{len(hard)} hard failure(s):\n")
        for kind, f, ln, detail in hard:
            loc = f"{f}:{ln}" if ln else f
            print(f"  {kind:<32} {loc}\n      {detail}" if detail else f"  {kind:<32} {loc}")
    else:
        print("\nno broken links, anchors, refs or images")

    if soft:
        groups = defaultdict(list)
        for kind, f, ln, detail in soft:
            groups[kind].append((f, ln, detail))
        print()
        for kind, rows in sorted(groups.items()):
            print(f"  {len(rows):>4}  {kind}")
            if "--all" in flags:
                for f, ln, detail in rows:
                    loc = f"{f}:{ln}" if ln else f
                    print(f"          {loc}  {detail}".rstrip())
        if "--all" not in flags:
            print("\n  (soft findings are judgment, not defects; --all lists them)")

    if "--all" in flags and drift:
        print(f"\n  {len(drift)}  link text that may not match its target")
        for ov, f, ln, label, link, actual in drift:
            print(f"          {f}:{ln}  \"{label}\" -> \"{actual}\"")

    if hard and "--warn-only" not in flags:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

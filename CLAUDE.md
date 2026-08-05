# CLAUDE.md — Before You Build

Quarto book. Live at <https://ei.nilehatch.com/>.

**The book is titled *Before You Build*. The method it teaches is *expeditionary
innovation*.** Those are different things and both names are load-bearing: when a
passage refers to the book, use the title; when it refers to the method, the chapter
and the process, use the method name. The `Expeditionary_Innovation.qmd` chapter title
and the Conclusion's headings are the method, and are correct as they stand.

Licensed CC BY-NC 4.0. `LICENSE`, the preface colophon and the demo notice must agree;
they contradicted each other until 2026-08-05, when `LICENSE` still said CC0.

This file covers what the repo cannot tell you on its own; for anything structural,
read `_quarto.yml` and the comments already in it.

## What this book is, and where it stops

*Before You Build* is the **exploration** book. It owns the front end —
choosing who to talk to, finding and validating pain, ideating and testing
solutions — across three diamonds.

It is one of a family of books that share a hub-and-spoke architecture:

| Book | Repo | Role |
|---|---|---|
| *Make the Call* (MtC) | `../book-make-the-call` | The hub. Owns the general logic of deciding under uncertainty. |
| ***Before You Build*** (EI) | here | A spoke. Applies that logic to the expedition front end. Teaches *expeditionary innovation*. |
| *Is This Worth Doing?* (ITWD) | `../book-is-this-worth-doing` | A spoke. Applies it to profit analytics. |

**The hard boundary: EI hands off to Make the Call at the moment of deciding.**
EI must not re-argue MtC's thesis. When a passage starts explaining *how to weigh
evidence and commit*, it has crossed the line — link to MtC instead. The same
applies at the other edge: profit analytics belongs to ITWD, and
`Test_Solution.qmd` currently overruns that boundary (a known, unfixed problem).

There is no required reading order. Each book must stand alone, which means
cross-references are pointers, not prerequisites.

If you notice a claim in EI that contradicts one in a sibling book, surface it
rather than quietly reconciling it.

## Prose

- Nile's voice. Do not smooth it toward textbook tone. Ask before an edit that
  changes rhythm rather than content.
- No emoji, anywhere, ever.
- Every factual claim needs a real citation from Zotero. **Never fabricate a
  source.** If a claim needs support that isn't in the bib, say what you would
  need — a collection, a starting paper, an author — and leave the claim flagged.
- The rivals (Ries, Blank, Popper, Plattner, Camuffo) are in the bibliography and
  largely uncited in the text. That is a known gap, not an oversight to fix
  silently.

## Cross-references: link by filename

**This book does not use Quarto's `@sec-` cross-references between files.** Use
markdown links to the `.qmd` path, with an optional anchor:

```markdown
[What Makes a Good Pain Hypothesis](Hypothesize_Pain.qmd#sec-hypothesize-pain-section)
[Test Pain Guide](../toolkit/Test_Pain_Guide.qmd)     <!-- from demo/ or toolkit/ -->
```

This is deliberate and matches Make the Call. `@fig-` and `@tbl-` refs are still
normal Quarto cross-references; only section links follow this convention.

## Citations

`scripts/sync-refs.py` runs as a Quarto pre-render hook. It mirrors cited entries
from the Zotero Better BibTeX master export into `references.bib`.

- **Do not hand-edit `references.bib`.** Fix metadata in Zotero; it propagates on
  the next render.
- Cite keys are Better BibTeX (author-year-shortname).
- Master export lives at `~/Documents/bibs/zotero.bib` — this is the live Better
BibTeX auto-export and the path `sync-refs.py` actually uses. **Do not use
`~/Documents/Claude/bibs/zotero.bib`**: it is a stale copy (frozen 2026-05-12,
221 entries behind) that will silently fail to resolve anything added since. If it is absent
  (fresh clone, CI), the script prints a notice and exits 0 — the build proceeds
  on the committed bib and never fails on this.
- The script is shared verbatim with Make the Call. Fix bugs in both, or in
  neither.

## Styling

- `base.css` is **canonical and shared with Make the Call** — same file, byte for
  byte. Structure only. Do not edit it for an EI-specific reason; a change here
  is a change to every book in the family.
- `custom_ei.css` is EI's skin: seven `--brand-*` variables and nothing that
  belongs in `base.css`. EI's palette is azure cerulean (`#0A659E` →
  `#0B5E86`) — deliberately bluer than MtC's, with the shared gold accent.

## Figures

`scripts/diamonds.R` generates all fourteen diamond SVGs into `images/`. Run it
from the repo root; `OUT` is optional and defaults to the working directory.
Regenerate the whole set rather than hand-editing an SVG — shape, colour ramp and
node geometry are all derived, and editing one breaks the family's consistency.

## Rendering and deploy

- **Pushing to `main` publishes to the live site.** There is no staging step.
- `execute: freeze` is `auto`, not `true`, for a reason documented in
  `_quarto.yml`. **Commit `_freeze/` after any render that touches a document
  containing a code chunk.** CI has no R: a stale freeze fails the build loudly
  instead of quietly shipping old output.
- Verify a deploy by capturing the run ID for the specific commit SHA. Do not
  `gh run list --limit 1` — that races the new run and reports the previous
  commit's result.

## Working rules that cost us something once

- **Run `python3 scripts/prose-check.py` after every writing pass, before you
  commit.** With no arguments it checks only the files this pass touched, which
  is the point: it is for new prose, not for relitigating a manuscript written
  before the rules existed. `--all` sweeps the book including the demos.
  It enforces the family style guide's §15 em-dash target (≤4.0 per 1000 words
  of prose) and §12a's ban on sentence-length bold. It exists because those
  rules were broken three times in one session by the same person who had just
  written them, twice within an hour of writing them. A habit did not work.
- **Assert before you patch.** Any scripted edit must verify the target string
  matches before writing. A silent no-match once shipped a change that never
  landed, and it was not caught until much later.
- **Before adding a rule to `base.css`, grep for `^\.classname {` specifically.**
  A pattern like `grep "\.trap"` matches the grouped selector and the
  `> :first-child` rule and looks like a hit, while the standalone block sits
  elsewhere in the file. That is how `.trap` ended up defined twice, in two
  different reds, and shipped to both books.
- **Regex over `.R` and `.qmd` is dangerous** — nested parens and callout fences
  break naive patterns. Prefer an explicit edit over a clever substitution.
- Run `git status` before starting. Surface anything uncommitted.
- Show `git diff --stat` after changes.
- Small commits, one logical unit each, message explaining *why*.

## Two things that look like bugs and are not

- `_solution_guides_separator.qmd` and `demo/_diamond3-separator.qmd` are the last
  entries in their parts because the content after them is unwritten. That is the
  book's largest gap, not a config error.
- `collapse-parts.html` exists but is commented out of `_quarto.yml`. Parked
  deliberately; leave it unless asked.

The editor is VS Code or Cursor. Do not assume RStudio or add `.Rproj` files.

## Notes and audits go to the vault, not here

Assessments, plans, audits, and project state live in `~/notes/`, not in this
repo. The EI overview is at `~/notes/10-Books/ent-innovation-ei/_overview.md`;
cross-book decisions at `~/notes/10-Books/cross-book-architecture-decisions.md`.
Read the overview for current status before proposing a direction.

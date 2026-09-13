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
applies at the other edge: profit analytics belongs to ITWD.

**Correction, 11 Sep 2026.** This file used to say `Test_Solution.qmd` *overran*
that boundary and called it a known unfixed problem. That was wrong, and it had
been repeated for weeks. Profit analytics is the seventh solution test, and the
chapter introduces what it does and when it belongs and then explicitly says
there is not space to cover it properly. **The overlap is deliberate**: the reader
should leave knowing the test exists and why it comes last, and should not try to
run it from what is written there. That is the boundary working, not failing.
What was genuinely wrong is now fixed: the hand-off pointed at *Hatchet or Hatch
It*, a title ITWD no longer uses, with no link. It now names the current book and
links to it.

There is no required reading order. Each book must stand alone, which means
cross-references are pointers, not prerequisites.

If you notice a claim in EI that contradicts one in a sibling book, surface it
rather than quietly reconciling it.

## Diamond 3 is different: the chapters are the source

For Diamonds 1 and 2, the guides hold procedure the chapters had lost, so revising a
chapter meant pulling judgment *up* out of its guide. **Diamond 3 inverts this and it
is a historical accident worth knowing.** The LaTeX originals mixed principle and
method together in the chapter. The ChatGPT-era pass split them, moving methods out
into guides — but only ever got as far as Diamonds 1 and 2. D3 guides were never
created, so nothing migrated out and **the three D3 chapters still carry their methods
in full**: 6-3-5 brainwriting, SCAMPER, SIT, the feasibility filter, dot voting, the
screening matrix with a worked demonstration, and all seven solution tests.

So `toolkit/Solution_Guides.qmd` must be **extracted from** the chapters, never written
beside them. Writing one independently produces drift, which already happened once:
a brainwriting guide written from scratch on 11 Sep said *pass left, two or three
rounds* while `Ideate_Solutions.qmd` says **6-3-5, pass right, six rounds**, with a
citation to `rohrbachCreativeRulesMethod1969`. Check the chapter first, every time.

**NWH's caveat was right, audited 11 Sep.** The D3 revision round dropped two things,
so the extraction rule above has an exception. Full detail in
`~/notes/10-Books/ent-innovation-ei/d3-latex-audit-2026-09-11.md`.

- **The Scoring Matrix is gone.** LaTeX `HH04` carried the standard pair: a *Screening*
  Matrix (coarse, +/0/- against a reference solution, unweighted) and then a *Scoring*
  Matrix (weighted -- assign weights, rate features, score). The book kept only the
  first, and "scoring matrix" / "assign weight" / "weighted" appear nowhere in it.
  Convergence has a filter designed to eliminate and nothing designed to choose.
- **Smoke testing is compressed about 90%**, from 3,844 LaTeX words to 380. Gone: domain,
  landing-page anatomy, conversion tracking, ad campaign, Google Ads setup. The whole of
  `Test_Solution.qmd` is now shorter than the LaTeX spent on this one test.

**So the exception: for smoke testing the source is `HH05.4 Smoke Testing.tex`, not the
chapter**, because the chapter no longer holds the procedure. Extract from the chapter
everywhere else in D3; check the LaTeX first here. Same in miniature for looks-like vs
works-like, which organized `HH05.3` and survives only as a clause inside "Rapid
Prototypes".

The LaTeX also carries commented-out outline notes -- intentions from 2018 never
written. Read them before writing D3 guides; they are NWH's own plans.

**The seven solution tests**, all in `Test_Solution.qmd`: validation, verification,
wow factor, \$100, Wizard of Oz, smoke, profit analytics. Wizard of Oz is also an
*input* to several of the others, since it is how a concept gets in front of someone
convincingly enough for the reaction to mean anything.

## The split is judgment/procedure, not principles/methods

A refinement from the Diamond 2 work, and it answers NWH's doubt about whether the
ChatGPT-era split was right. Principles-versus-methods sends everything operational to
the guide, including *operational judgment* — and that is where it goes wrong. Four
times in one session the guide turned out to hold judgment the chapter needed: the
*Saying* lens, urgency x feasibility, the fourth pain-test criterion, the sample
floors. Each one improved the chapter when moved up.

The working rule: **the chapter takes every judgment, including operational ones. The
guide keeps steps.** Gallery shows good beside bad; the layer is the machine rendering.

## The Halo Alert demonstration

**Provenance, and it must stay stated.** The concept and much of the framing come from a
**real innovation project** that never shipped -- promising, customer-tested, killed by team
dynamics. Its artifacts are gone except one: the **screening matrix** in
`Hypothesize_Solution.qmd` is the original team's own, recovered from course files. Everything
else in `demo/` is **reconstructed**, written with an AI.

That disclosure is load-bearing, not decorative. This book's standing order is that an AI can
work on your evidence and cannot *be* your evidence, so a demo of generated transcripts
presented as field records would contradict the method it teaches. The landing page says so and
turns it into the lesson: the demo may generate a record because its job is to show the shape of
one; the reader's own record may not, because it has to *be* the evidence. **Do not soften or
remove that.**

**Anonymity.** The origin story is told with no institution, year, course, roles, or
characterisation -- NWH has a former student who would recognise himself. The phrase is *real
innovation project*, never *student project*. Researchers carry pseudonyms (Dana, Ray) exactly
as respondents do; NWH's own name was in transcripts and observation logs until 13 Sep. Students
appear only as a **studied population**, never as the team's identity.

**Structure, since 13 Sep.** Nine entries, consolidated by diamond, no separators:
at-a-glance, D1, D2 explore, two full transcripts, D2 converge, D2 validate, D3. Every record
follows *Unknown → Design → Execution → Evidence → Knowledge update → Next steps*, which is the
operational form of the four-part record in the toolkit landing page.

**Where it stops, and why.** After the wow factor and \$100 tests. The team stopped there, and
NWH is preparing real student smoke-test landing pages on nilehatch.com as explorable demos,
because a landing page shown as screenshots cannot be clicked. Wiring those URLs in later is a
two-line change: the pointers already exist in the D3 page and the smoke-test guide.

## Two hazards that cost a render each

- **Bare `---` rules.** The demo sources used them as separators, and a rule followed
  immediately by text reads to pandoc as a YAML block -- `**Attribution:**` starts with an
  asterisk and fails as a YAML alias. Merges strip horizontal rules.
- **Lists that never become lists.** A bold label with no blank line before the list renders the
  dashes literally, and an **en-dash** used as a bullet marker never was a list at all. Both
  occurred in the ChatGPT-era demo text.

## prose-check: the demo exemption is inverted

`TRANSCRIPT_DIRS` skips `demo/` **only when `--all` is absent**. So a targeted run on a demo file
reports *clean by skipping it*, not by passing it. Check demo prose with `--all`, or by hand.
Its stub-bullet rule also strips bold as a run-in label, so mid-sentence bold leaves a fragment
and trips the count -- which is a §12a violation anyway, since bold is navigation and not stress.

## Prose

- Nile's voice. Do not smooth it toward textbook tone. Ask before an edit that
  changes rhythm rather than content.
- No emoji, anywhere, ever.
- Every factual claim needs a real citation from Zotero. **Never fabricate a
  source.** If a claim needs support that isn't in the bib, say what you would
  need — a collection, a starting paper, an author — and leave the claim flagged.
- **The rivals are now cited (13 Sep 2026), additively and at the points of
  divergence** rather than as a literature review. Ries and Blank in
  `Build_Solutions_part`, Sarasvathy and Kim/Mauborgne in `Choose_Community_part`,
  Ulwick and Plattner in `Explore_Community`, Popper in `Validate_Pain`, Camuffo in
  `Expeditionary_Innovation`, and all of them again in the Conclusion, which sets
  how each is characterized.

  **The tone is the rule here, set by NWH: acknowledge the work, name what is
  improved, never dismiss and never argue.** Each rival is credited with what it
  gets right before any divergence is stated, and Camuffo is treated as the ally he
  is rather than as a rival at all. If you add another, match that register.
  Effectuation gets the most care, because it is the genuine opposite.

### Salience assertions: whose claim is it?

**The test: if the sentence would need a citation under this book's own rules, it is
NWH's to make or it goes.** Structural claims are anyone's — *"this condition is easy
to omit"* is a property of the thing. **Frequency claims about people are NWH's** —
*"most people omit it"* asserts a vantage point over many practitioners, which he has
and a drafting assistant does not.

Caught 13 Sep: the formula *"the Nth is the one people skip"* had appeared **three times
in two days across three files**, each time an unsourced empirical claim in a book whose
thesis is that claims need evidence. Swept.

It exists because lists are flat and a flat list gives the reader no purchase. That is a
real problem, and hierarchy can be built three other ways at no cost:

| | |
|---|---|
| assertion | "The fourth is the one people skip." — incurs the debt |
| **mechanism** | "The fourth is what turns a record into something you can be wrong about." |
| **consequence** | "Skip the fourth and you have a diary." |
| **conditional** | "If you do only one of these, do the fourth, because…" |

Often the lead-in can simply go: the sentence after it was already carrying the argument.

**Two frequency claims stand deliberately**, confirmed by NWH 13 Sep as things he has
watched happen: *"most people spend their effort on route four"* (`Pain_Guides`) and
*"Most people set it too wide"* (`Community_Choice_Gallery`). These are his observations,
not inferences. Do not sweep them.

NWH is wary of superlatives and audits his own prose by asking whether he could justify
the claim if challenged. That is the book's own standard applied to its voice, and it is
a feature. Do not smooth it away, and do not pay for emphasis with claims when mechanism
is free.

## Cross-references: link by filename

**This book does not use Quarto's `@sec-` cross-references between files.** Use
markdown links to the `.qmd` path, with an optional anchor:

```markdown
[What Makes a Good Pain Hypothesis](Hypothesize_Pain.qmd#sec-hypothesize-pain-section)
[Pain Testing](../toolkit/Pain_Guides.qmd#sec-pain-testing)   <!-- from demo/ or toolkit/ -->
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

## The method layer and the toolkit: one method, two renderings

`method-layer.qmd` (appendix) is the procedure rendered for a machine. The toolkit guides
hold the same steps rendered for a person with a wall and sticky notes. **This is not an AI
path plus a manual alternative** — that framing rebuilds the two-track confusion and brands
the hand-worker's route as lesser. Nothing in the prose should suggest one is primary.

Why EI does this when ITWD deleted its toolkits: ITWD's toolkits measured zero executable
lines, and ITWD has the Profit Analytics **app** as its no-AI path. EI's guides carry real
steps and EI has no app. Also note ITWD's second rendering is code, which cannot silently
disagree with the layer. EI's is prose, which can.

**The drift rule, settled 10 Sep 2026: the guide is authoritative for steps. The layer is
derived from it.** When they disagree, the guide wins and the layer is corrected to match.
Never patch only one.

The AI/human trade is **per tool, and it is not always a trade.** Personas hand over with no
cost at all: a persona you write you believe, and belief is the failure. Clustering is a real
trade, because handling the notes is how you absorb them — so the chapter tells the reader to
cluster by hand and then hand the clustering to the AI for an audit. The full reasoning is in
`~/notes/10-Books/ent-innovation-ei/method-layer-and-the-ai-split.md` §4b.

**Open: the toolkit needs restructuring, not deleting.** Measured 9 Sep, only 38-52% of each
standard-form guide is Steps + Tips; the other half is Purpose / Why It Matters / Method
Options, which is chapter content sitting in the toolkit. Cutting each to a one-page procedure
card would halve the toolkit, return the framing to the chapters, and shrink the drift surface
to the only part that was ever operational. Twenty-three flat entries also want grouping by
diamond.

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

## Closed: stopping rules (9 Sep 2026)

Raised 17 Aug: the book stated aims without bars, and `Validate_Pain` settled for "enough
evidence that you're not chasing shadows". Closed by the 2.3 rewrite, which gives the stopping
rule **two arms** rather than a number, because a number alone would falsely precise a judgment
call: a floor on sample (8–15 to pilot wording, 25–50 for a prioritization worth acting on,
stated as floors and not targets) **and a falsification condition written before fielding**.
If the reader will not write one, the chapter says what they are running is a demonstration
rather than a test.

`.threshold` is now used throughout rather than once. `Explore_Community` also gained
*What Stopping Actually Means*: the entropy signal ends the broad sweep and does not prove
nobody would have surprised you, and four named triggers reopen the question. Each names a
question, a target and a finish line, which is what separates a return from unbounded churn.

## Closed: British spellings (swept 9 Sep 2026)

`scripts/prose-check.py` gained a US-spelling check on 17 Aug, added in the ITWD
session and copied here byte-identical. It found nineteen instances across eight
files; all are fixed and `--all` now reports none.

Worth keeping from the sweep. **Nine of the nineteen sat in the revised Diamond 1
chapters and six more in the Pain Statement Gallery** — the pages already assigned
to students, not the unrevised tail where they were assumed to be. A defect
introduced during careful revision is not less likely than one inherited; it is
just less expected.

Both `judgement` instances were the ordinary sense rather than the legal one, so
both took the US form.

Two traps if sweeping by hand rather than by the checker. A `\b` after the stem
misses compounds — `neighbourhood` and `Labelling` both survive a word-anchored
grep. And the obvious stem for some pairs matches correct US words: `analys` hits
*analysis* and *analyses*, `realis` hits *realism* and *realistic*. The checker's
BRITISH table already encodes both lessons, and it still missed `categorisable`
and `categorise`; a stem table is a list, not a rule, and it will keep having
holes.

One false positive to leave alone: `colour` in `demo/exp-08.a-experience-map`
is a ggplot2 argument name, not prose.

# Expeditionary Innovation

A Quarto book by Nile Hatch on finding and framing an innovation: how to reduce uncertainty
by choosing the right people, discovering an unmet need they actually live with, and
designing a solution that relieves it.

Live at **<https://ei.nilehatch.com>**.

Part of a family of books on using evidence to succeed in entrepreneurship, alongside
*Make the Call* (deciding under uncertainty) and *Is This Worth Doing?* (profit before
revenue exists).

## Build

```bash
quarto render          # output lands in _book/
quarto preview         # live reload while writing
```

R is required only to re-execute figures. `execute.freeze` is `true`, so an ordinary
project render reuses the committed `_freeze/` results.

**To refresh a figure:** render that single file — a single-file render always executes —
then commit the updated `_freeze/`.

```bash
quarto render Choose_People_part.qmd
```

## Citations

`references.bib` is **generated — do not edit it by hand.** `scripts/sync-refs.py` runs as a
pre-render hook and mirrors cited entries from the Zotero Better BibTeX auto-export at
`~/Documents/bibs/zotero.bib`.

Add or correct a source in Zotero, cite its Better BibTeX key, and render. Copy keys from
Zotero rather than guessing them.

If the master export is absent (a fresh clone, or CI), the script says so and the build
proceeds on the committed bibliography.

## Deployment

Pushing to `main` triggers `.github/workflows/publish.yml`, which renders the book and
deploys `_book/` to Netlify with the Netlify CLI. Requires the repo secret
`NETLIFY_AUTH_TOKEN`; the site id is public and inlined in the workflow.

Netlify should **not** also build this repo from git — the deploy is CLI-only, and a second
Netlify-side build would race this one.

## Layout

| Path | What it holds |
|---|---|
| `*.qmd` | Narrative chapters and part introductions |
| `toolkit/` | Templates and step-by-step guides for each method |
| `demo/` | The Halo Alert worked demonstration |
| `images/` | Figures and diagrams |
| `scripts/` | `sync-refs.py`, the citation pipeline |
| `_freeze/` | Committed R chunk results (keeps R out of CI) |

## License

Content is licensed [CC BY-NC-ND 3.0](https://creativecommons.org/licenses/by-nc-nd/3.0/us/).
See `LICENSE`.

# timurletter.com

Personal site for Redi Sunarta — analytics for consumer tech companies.

Static HTML and CSS, assembled by a small Python script. No npm, no dependencies, no framework. Hosted on GitHub Pages.

---

## How it works

**You edit `_partials/` and `_pages/`. Never the HTML at the repo root — that is generated and gets overwritten.**

```bash
python3 build.py        # assemble
python3 tools/check.py  # verify
```

`build.py` wraps each page body in the shared header and footer, fills in per-page metadata, appends the "Next →" block, and regenerates `sitemap.xml`.

The point is that the header, footer, `<head>` metadata, and next-page links exist in exactly one place each. Change the nav once and all ten pages update.

---

## Files

```
build.py              Assembles the site. Page config (titles, meta, next-links) lives here.
tools/
  check.py            Pre-deploy validation. Run before every push.
  extract-covers.py   Regenerates Timur cover thumbnails from the published PDFs.

_partials/            ← EDIT THESE
  head.html           <head>, site header, opening <main>
  foot.html           closing </main>, site footer
  next.html           the "Next →" block

_pages/               ← AND THESE (body content only, no header or footer)
  index.html          home
  work.html           project index
  work-poml.html      ┐
  work-free-shipping.html
  work-loyalty.html   │ one case study each
  work-loyalty-point.html
  viz.html            Tableau + Datawrapper
  writing.html        Timur archive
  about.html
  404.html

css/style.css         All styles. Design tokens at the top.
assets/
  timur-logo.png      homepage mark, 440×440
  redi-440.jpg        About portrait, 440×440
  og.png              social card, 1200×630
  favicon.svg
  covers/             Timur cover thumbnails, 480×270
  dw/                 Datawrapper chart exports
resume/               ← put the MASKED resume PDF here

CNAME                 custom domain for GitHub Pages
.nojekyll             stops GitHub running Jekyll — required
robots.txt
.gitignore            blocks spreadsheets, personal folders, scratch files

index.html            ┐
work*.html            │ GENERATED — do not edit
viz.html              │ your changes will be lost on the next build
writing.html          │
about.html            │
404.html              │
sitemap.xml           ┘
```

---

## Documentation

| File | Covers |
|---|---|
| `DEPLOY.md` | GitHub Pages setup, DNS, HTTPS, publishing changes |
| `EDITING.md` | Where every piece of text lives, line by line |
| `ADDING-CONTENT.md` | Adding a project or an article |
| `PROJECT-PAGES.md` | The case-study structure and how to add a fifth |
| `IMAGES-TUTORIAL.md` | Photo and cover sizing rules |
| `WORK-PAGE-TUTORIAL.md` | Step-by-step for the Work page |

---

## What makes it read as one site

- **Header and footer defined once.** `check.py` verifies they're byte-identical across all ten pages on every run.
- **One `.page-head` component** for the top of every page, so the rhythm never shifts.
- **Active nav state** via `aria-current="page"` — styled, and announced to screen readers.
- **A next-page chain.** Every page ends pointing somewhere instead of dead-ending.
- **Cross-document view transitions** where supported; inert elsewhere, off under `prefers-reduced-motion`.
- **No inline styles.** Every spacing decision is a class.
- **Sitemap generated from the same config** as the pages, so it can't drift.
- **On-page outline** in the left margin of index, work, writing, and about. Built from each page's own `<h2>` elements at build time, so it can't fall out of sync with the content. Appears only above 1180px; hidden on narrower screens where it would crowd the text.

---

## Before launch

Run `python3 tools/check.py`. It currently reports two blockers:

**1. Missing resume PDF.** `about.html` links to `resume/Redi-Sunarta-Resume.pdf`, which doesn't exist. Either add the masked PDF or remove the link — see `DEPLOY.md` §0.

**2. Twelve `[FILL]` placeholders** across the four project pages. They render as visible grey boxes. Fill them or delete the blocks — see `PROJECT-PAGES.md`.

Also worth doing before you publish:

- **Read the prose aloud.** It was drafted from your resume and Timur context pack. The Method sections on the project pages are the ones a hiring manager reads closely — verify they describe what you actually did.
- **Confirm the masking.** Absolute currency figures are `XX`; relative changes are as reported. If you add anything new, decide before publishing, not after.

---

## Deploy

GitHub Pages, custom domain `timurletter.com`. Full walkthrough in **`DEPLOY.md`**.

Publishing a change once live:

```bash
python3 build.py
python3 tools/check.py     # must pass
git add -A && git commit -m "what changed" && git push
```

---

## Local preview

Double-click `index.html`. All internal paths are relative, so it renders correctly straight off disk.

For something closer to production:

```bash
python3 -m http.server 8000
```

Paths are relative (`css/style.css`, not `/css/style.css`) — that's what makes `file://` work. If you ever move pages into subfolders, switch to absolute paths and preview via a server.

---

## Notes

- **Fonts** load from Google Fonts. To self-host: download Inter, put the woff2 files in `assets/fonts/`, replace the `<link>` tags in `_partials/head.html` with `@font-face`.
- **Contrast** verified: ink/paper 16.65:1, muted 6.60:1, accent 4.91:1 (AA — links only, never body text).
- **Chart palette** `--c1`…`--c6` in `style.css` is Okabe–Ito, colourblind-safe. Unused so far; there for when charts go inline.
- **Analytics** not installed. Plausible or GoatCounter — one script tag in `_partials/head.html` covers all ten pages.
- **No dark mode**, by choice.
- **`_partials/` and `_pages/` must be committed.** They are the source. Deploy only the built HTML and the next person to edit it — including future you — has nothing to work from.

---

## Editing quick reference

| What | Where |
|---|---|
| Colour, type, spacing | CSS custom properties at the top of `style.css` |
| Page titles, meta descriptions, OG tags, next-page chain | the `PAGES` dict in `build.py` |
| Domain | the `DOMAIN` constant in `build.py` — one line, feeds canonical URLs, OG tags, JSON-LD, and the sitemap |
| Header, footer, nav links | `_partials/` |
| Page content | `_pages/` |
| Which pages get an outline | `toc=True` in the `PAGES` dict |
| A shorter outline label | `data-toc="Short label"` on the `<h2>` |

**Adding a page:** create `_pages/newpage.html` with just the body, add an entry to `PAGES` in `build.py`, run the build. Nav link goes in `_partials/head.html`. The sitemap updates itself.

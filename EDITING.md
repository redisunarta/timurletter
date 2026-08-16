# How to change the text

Everything you see on the site comes from **six files in `_pages/`**. Open them in any text editor — TextEdit, VS Code, whatever.

> **Adding a new project or a new article?** See `ADDING-CONTENT.md` — it has copy-paste blocks for both.

**Two rules:**

1. Edit files in `_pages/`, never the ones at the top level. The top-level `index.html`, `work.html` etc. are generated and get overwritten.
2. Run `python3 build.py` afterwards, then refresh the browser. Nothing changes until you do.

```bash
cd "/Users/redisunarta/Documents/Personal Website/site"
python3 build.py
```

---

## The rule that matters

Change the words **between** the angle brackets. Leave the brackets alone.

```html
<h1>Analytics for consumer tech companies</h1>
    └────────── change this ──────────┘
```

The `<h1>` at the start and `</h1>` at the end are the container. If you delete one by accident, the page breaks and it's usually obvious — text suddenly renders huge or vanishes. Undo and try again.

Some paragraphs have `<strong>` inside them for the bold bits:

```html
<p><strong>Outcome:</strong> freeing <strong>$XX million</strong> in annual subsidy.</p>
```

Change the words freely. Keep the `<strong>` pair if you want it bold, delete both halves if you don't.

---

## Special characters

Some punctuation is written as codes so it renders identically in every browser. Leave these as-is, or copy them when you write new text:

| Code | Shows as | Where it's used |
|---|---|---|
| `&middot;` | · | separating items — "Allo Bank · Tokopedia" |
| `&ndash;` | – | number ranges — "2018–2022" |
| `&rsquo;` | ' | apostrophes — "Indonesia's" |
| `&amp;` | & | ampersands |
| `&rarr;` | → | arrows |
| `&darr;` | ↓ | download arrow |

You can also just type the real character (·, –, ', &) — the files are UTF-8 and it works. The codes are only there because they survive copy-paste better.

---

## Where everything lives

Line numbers verified against the current build. If they drift, search for the text instead — that always works.

### `_pages/index.html` — homepage

| Line | What it is |
|---|---|
| 5 | Main headline |
| 6 | The one-line positioning statement |
| 21–22 | Current role strip |
| 26 | "Selected work" heading + 3 cards |
| 54 | "Writing" heading + 3 post rows |

The Timur logo is `assets/timur-logo.png`. Swap it for a photo by changing that `<img>` to `class="portrait" src="assets/redi-440.jpg"`.

### `_pages/work.html` — projects

**Structure:** title → current-role strip → one `<article class="case">` per project.

| Line | What it is |
|---|---|
| 4–5 | Page title and intro |
| 8–9 | Current role strip |
| 13 | Project 01 — POML (`#poml`) |
| 21 | Project 02 — free shipping (`#free-shipping`) |
| 29 | Project 03 — loyalty points (`#loyalty`) |

**To add a project, see `ADDING-CONTENT.md`.** It covers the basic block plus the optional pieces — stat strips, labelled sections, charts, callouts — with the markup for each.

### `_pages/viz.html` — dashboards and charts

| Line | What it is |
|---|---|
| 3–4 | Page title and intro |
| 12 | "Datawrapper" heading |
| 15–48 | The 6 Datawrapper cards |
| 51 | "Tableau Public" heading |
| 54–75 | The 20 Tableau cards |

**Datawrapper** cards use local images in `assets/dw/<id>.jpg`. To add one: export the PNG from Datawrapper (the filename starts with the 5-character chart ID), drop it in `assets/dw/` named `<id>.jpg`, then copy an existing `<a class="dw-card">` block and swap the ID, title, and blurb.

**Tableau** cards hotlink thumbnails from Tableau Public, so they refresh automatically when you republish a viz. The image URL pattern is `static/images/<first-2-chars-of-repo>/<repo>/<view>/1.png`.

### `_pages/writing.html` — Timur

One flat list per series. Each row is: title across the top with a "Part N" chip, 160×90 thumbnail left, one-sentence summary right. About five rows fit a laptop screen.

| Line | What it is |
|---|---|
| 4–5 | Page title and lede |
| 14–16 | Build-note banner — **delete before launch** (search `todo-banner`) |
| 20 | "SEA Subsidy Wars" heading |
| 25–84 | Its 12 post rows |
| 90 | "The Great Extraction" heading — Series 2, add rows as you publish |

Each row:

```html
<a class="post" href="#TODO-LINK-1">
  <span class="post-head"><span class="post-n">Part 1</span><span class="post-t">The Rise and Fall of Burn Rate</span></span>
  <img class="post-thumb" src="assets/covers/sw-01.jpg" alt="" loading="lazy" width="480" height="270">
  <span class="post-sum">One or two sentences.</span>
</a>
```

- `href` — the LinkedIn permalink
- `post-n` — part chip · `post-t` — headline · `post-sum` — summary
- `alt=""` is deliberate: the thumbnail is decorative, the title already names the link

To add a series, copy a whole `<section>` block — the `sec-head` with its heading and count, then a `<div class="posts">` holding the rows.

**The 12 existing summaries are my drafts** — read them and make them yours before launch.

Thumbnails are in `assets/covers/` at 480px. Regenerate them with `python3 tools/extract-covers.py`.

### `_pages/about.html` — bio and CV

Kept deliberately short — a two-page-resume summary. Depth belongs on the work page.

| Line | What it is |
|---|---|
| 6–7 | "About" and the opening line |
| 21 | "Experience" heading |
| 31 | Allo Bank — role lede + 3 notable projects |
| 46 | Tokopedia — role lede + 3 notable projects |
| 91 | "Education and recognition" |
| 118 | Social volunteering |
| 132 | "Get in touch" |

Each job has an optional one-line `role-lede` summarising the role, then bullets for notable projects:

```html
<div class="role">
  <div class="role-head">
    <h3>Job title</h3>
    <div class="role-when">Dec 2023 &ndash; present</div>
  </div>
  <div class="role-org">Company &middot; Team</div>
  <p class="role-lede">One line on the role itself.</p>
  <ul>
    <li>Notable project.</li>
  </ul>
  <p class="stack">Products: …<br>Stack: …</p>
</div>
```

---

## Text that is NOT in `_pages/`

Three things live elsewhere, because they are shared across pages:

| What | Where |
|---|---|
| Nav links — Work, Viz, Writing, About | `_partials/head.html` |
| Footer — your name, tagline, email, link columns | `_partials/foot.html` |
| The "Next →" blocks at the bottom of each page | `build.py`, in the `PAGES` block, under `next=` |
| Browser tab titles and Google search descriptions | `build.py`, `title=` and `desc=` |

Editing `_partials/foot.html` once changes the footer on all six pages. That's the whole point of the setup.

---

## If something breaks

**The page looks unstyled** — you probably opened a file in `_pages/` directly in the browser. Those are fragments with no styling attached. Open the top-level `index.html` instead.

**Your change didn't appear** — you edited the top-level file instead of `_pages/`, or you forgot `python3 build.py`.

**The layout went strange** — you likely deleted half a tag. Undo (`Cmd+Z`) back to working and redo the edit more carefully.

**You want to start over on one page** — tell me and I'll regenerate it.

---

## The full loop

1. Edit a file in `_pages/`
2. Save
3. `python3 build.py`
4. Refresh the browser

Once you're happy, deploy per the README.

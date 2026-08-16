# Project pages

Each project now has its own page. The Work page is an index that links to them.

```
work.html                    index — one card per project
  work-poml.html             01 · Tokopedia · ML measurement
  work-free-shipping.html    02 · Tokopedia · Causal inference
  work-loyalty.html          03 · Allo Bank · Incentive design
  work-loyalty-point.html    04 · Allo Bank · New user reward
```

Sources are in `_pages/` with the same names.

---

## The structure

Every project page uses the same seven sections, in the same order:

| Section | What goes in it |
|---|---|
| **Context** | The situation, and what was actually at stake. Two or three paragraphs. |
| **My role** | What *you* did, as distinct from the team. Short. |
| **Method** | The named technique, explained in plain language. |
| **What made it hard** | The complication — the thing that made this more than a query. |
| **Evidence** | What the data showed. One concrete number beats three vague ones. |
| **Outcome** | What changed as a result. |
| **What I would do differently** | One honest thing. |

**Keep all seven, in this order, on every project.** That's what makes the set read as a method rather than four unrelated write-ups. If one page has "What made it hard" and the others don't, a reader assumes the others were easy.

"The strongest objection" is an optional eighth section — I've used it on the free-shipping page because synthetic control invites a specific technical objection worth answering head-on. Add it wherever a reader who knows the method would push back.

---

## Adding a new project page

### 1. Create the source file

Copy `_pages/work-loyalty.html` to `_pages/work-<slug>.html`. The slug is lowercase with hyphens — it becomes the URL.

### 2. Edit the header

```html
<div class="page-head page-head--case">
  <a class="back-link" href="work.html">&larr; Work</a>
  <div class="case-meta">05 &middot; Company &middot; Method &middot; Year</div>
  <h1>Outcome-led title</h1>
  <p class="lede">One or two sentences. The tension, not a summary.</p>
</div>
```

### 3. Fill the seven sections

```html
<div class="field">
  <div class="field-label">Context</div>
  <p>First paragraph.</p>
  <p>Second paragraph.</p>
</div>
```

Add as many `<p>` as you need. Spacing is automatic.

### 4. Optional — a stat strip

Goes between the page head and `<article class="case-detail">`:

```html
<div class="stats">
  <div class="stat"><div class="n">368,240</div><div class="l">reviews collected</div></div>
  <div class="stat"><div class="n">8</div><div class="l">banks tracked</div></div>
</div>
```

Two to four stats. Only when you have hard numbers — an empty-looking strip is worse than none.

### 5. Optional — a chart

```html
<img src="assets/my-chart.png" alt="What the chart shows — the finding, not 'bar chart'"
     loading="lazy" width="900" height="500">
```

Real pixel dimensions in `width`/`height` so the page doesn't jump while loading.

### 6. Register it in `build.py`

Find the `# --- individual project pages ---` block and copy an entry:

```python
"work-myslug.html": dict(
    canonical="work-myslug.html", nav="work",
    title="Short title — Redi Sunarta",
    desc="One sentence for Google, under 160 characters.",
    og_title="The headline as it appears on the page",
    og_desc="One sentence for LinkedIn previews.",
    og_type="article",
    next=("work.html", "All projects", "Back to the full list."),
),
```

`nav="work"` keeps **Work** highlighted in the header while a reader is on the page.

### 7. Fix the `next` chain

Pages currently chain in order and loop back:

```
work-poml → work-free-shipping → work-loyalty → work-loyalty-point → work
```

Inserting a page means changing the `next=` of the one before it. If you'd rather not maintain a chain, point every project's `next` at `work.html` — simpler, slightly less engaging.

### 8. Add a card to the Work index

In `_pages/work.html`:

```html
<a class="card" href="work-myslug.html">
  <div class="meta">05 &middot; Company &middot; Method</div>
  <h2>Same outcome-led title</h2>
  <p>One sentence.</p>
  <span class="card-out">The headline result</span>
</a>
```

### 9. Build

```bash
cd "/Users/redisunarta/Documents/Personal Website/site"
python3 build.py
```

The sitemap updates itself.

---

## Linking from the homepage

Homepage cards in `_pages/index.html` now point straight at project pages:

```html
<a class="card" href="work-poml.html">
```

Keep it to three. The homepage is a 30-second scan; the Work index is where the full list lives.

---

## The 12 `[FILL]` blocks

Three on each project page, marking what I couldn't write for you:

| Page | Missing |
|---|---|
| `work-poml` | How the comparison group was built · what the gap looked like · what you'd redo |
| `work-free-shipping` | The internal resistance · pre-period fit (RMSPE) and placebo tests · what you'd redo |
| `work-loyalty` | Abuser vs. heavy legitimate user boundary · how you showed reward ≠ retention · what you'd redo |
| `work-loyalty-point` | The competitive-parity objection · churn quantified around redemption · what you'd redo |

**The "What made it hard" blocks matter most.** Anyone can write "I used synthetic control." What separates a real case study from a claim is the specific complication and how you handled it. On the POML page, the comparison-group construction is load-bearing — a reader who knows measurement will look for it and notice its absence.

Search `_pages/` for `[FILL]`, replace the whole `<div class="callout">` with normal `<p>` paragraphs.

---

## A note on what I wrote

The Context and Method sections are drafted from your resume and the summaries on the old Work page. The reasoning is sound as far as I could infer it — but I inferred it. Read them before publishing and correct anything I got wrong about your actual approach.

Two places I reasoned rather than knew:

- **POML** — I framed it as targeting contaminating its own success metric. That's the standard problem with measuring a targeting engine, and it fits "post-analysis," but confirm it matches what you actually did.
- **Loyalty points** — I described the test as comparing otherwise-alike users. If you used a different design, say so; the method section is the part a hiring manager reads closely.

Commercial figures stay masked as `XX` throughout, per the rule we set.

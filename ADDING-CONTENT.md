# Adding content

> ## ⚠️ Do not use Chrome DevTools to edit the site
>
> DevTools edits **only change what's in the browser's memory**. Nothing is written to a file. Refresh the page and it's gone.
>
> And "Save page as…" makes it worse, not better: Chrome saves a *complete* HTML document — `<html>`, `<head>`, `<body>`, footer, the lot — and rewrites every link to `file:///Users/...`. But `_pages/` files must be **fragments**, just the middle section. Saving over one produces a page nested inside another page, with the stylesheet pointing at a folder that doesn't exist. The result is an unstyled, doubled-up page.
>
> DevTools is still useful for *looking* — inspecting spacing, testing a colour, checking mobile width. Just never save from it. Make the real change in `_pages/`.

---

## The only workflow that works

1. Open the file in `_pages/` with a **text editor** — TextEdit, VS Code, Sublime, anything
2. Edit
3. Save
4. Run the build
5. Refresh the browser

```bash
cd "/Users/redisunarta/Documents/Personal Website/site"
python3 build.py
```

### If you use TextEdit

TextEdit defaults to rich text, which will corrupt HTML. Before your first edit: **Format → Make Plain Text** (`⇧⌘T`). Or set it permanently in TextEdit → Settings → New Document → Plain text.

VS Code is a better fit and free — it colours the tags so mismatches are visible.

### What a `_pages/` file looks like

It starts mid-document, with no `<!DOCTYPE>`, no `<html>`, no `<head>`:

```html
  <div class="wrap">

    <div class="page-head">
      <h1>Work</h1>
      ...
```

If a file in `_pages/` ever starts with `<!DOCTYPE html>`, something has overwritten it with a full page. Tell me and I'll rescue the content.

---

Two things you'll do often: add a project to the **work** page, and add a part or series to the **writing** page. Both are copy-paste.

---

# 1. Adding a project to the Work page

Open `_pages/work.html`. Each project is one `<article class="case">` block. Copy an existing one, paste it where you want it in the order, and edit.

## The minimum

```html
<article class="case" id="short-name">
  <div class="case-num">04 &middot; Company &middot; Method</div>
  <h2>Outcome-led title, not a project name</h2>
  <p>What was at stake, in two sentences.</p>
  <p>What you did — the named method, in plain language.</p>
  <p class="case-out"><strong>Outcome:</strong> what changed.</p>
</article>
```

Four things to get right:

- **`id`** — lowercase, no spaces, unique on the page. This is the anchor: `work.html#short-name`. Link to it from the homepage cards.
- **`case-num`** — the number, the company, and the method. Update the numbers if you insert in the middle.
- **`<h2>`** — lead with the outcome. *"Killed a free-shipping subsidy in two cities"* beats *"Free Shipping Analysis."*
- **`case-out`** — one line, the result. This is the part people actually read.

## Going longer

Since you're writing these in more detail, here are the pieces you can drop inside an `<article>`. All the styling already exists.

### More paragraphs

Just add more `<p>` tags. No class needed. They're spaced automatically.

```html
<p>First paragraph.</p>
<p>Second paragraph.</p>
<p>Third paragraph.</p>
```

### A stat strip

Good directly under the `<h2>` when a project has hard numbers.

```html
<div class="stats">
  <div class="stat"><div class="n">368,240</div><div class="l">reviews collected</div></div>
  <div class="stat"><div class="n">8</div><div class="l">banks tracked</div></div>
  <div class="stat"><div class="n">64.3%</div><div class="l">classifier agreement</div></div>
</div>
```

Two to four stats. It reflows to fit. `n` is the number, `l` is the label under it.

### Labelled sections

When a project gets long enough that solid paragraphs stop being scannable, break it into labelled fields:

```html
<div class="field">
  <div class="field-label">Context</div>
  <p>Why this mattered.</p>
</div>

<div class="field">
  <div class="field-label">Method</div>
  <p>What you did, named plainly.</p>
</div>

<div class="field">
  <div class="field-label">The strongest objection</div>
  <p>The best argument against your conclusion, then your answer.</p>
</div>
```

Useful labels: Context · My role · Method · Evidence · The strongest objection · Outcome · What I would redo.

**Use the same labels in the same order across every project.** That consistency is what makes the page read as a method rather than a pile of write-ups. If one project has a "strongest objection" section and the others don't, it looks like the others have no objections.

### A quiet aside

```html
<div class="callout">
  <p class="small">A caveat, a limitation, or a note on what the data couldn't answer.</p>
</div>
```

### A chart

Save the image in `assets/`, then:

```html
<img src="assets/my-chart.png" alt="What the chart shows — the finding, not 'bar chart'"
     loading="lazy" width="900" height="500">
```

Set `width` and `height` to the real pixel dimensions so the page doesn't jump while loading. The alt text should state the **finding** — a screen reader user gets nothing from "chart."

### A bulleted list

```html
<ul class="prose-list">
  <li>First point.</li>
  <li>Second point.</li>
</ul>
```

## Linking a project from the homepage

Homepage cards are in `_pages/index.html` under "Selected work":

```html
<a class="card" href="work.html#short-name">
  <div class="meta">Method &middot; Company</div>
  <h3>Same outcome-led title</h3>
  <p>One sentence.</p>
</a>
```

Keep it to three cards. The homepage is a 30-second scan; the work page is where depth lives.

## Confidentiality

Mask absolute currency figures as `XX` — `Rp XX billion`, `$XX million`. Relative changes (`80%`, `12,000 transactions`) stay as they are, since a percentage reveals no commercial magnitude. If you add a project with figures you haven't masked before, decide before you publish, not after.

---

# 2. Adding to the Writing page

Open `_pages/writing.html`.

## Adding a part to an existing series

Copy one `<a class="post">` row and edit it:

```html
<a class="post" href="https://www.linkedin.com/pulse/your-article-url">
  <span class="post-head"><span class="post-n">Part 13</span><span class="post-t">The headline</span></span>
  <img class="post-thumb" src="assets/covers/sw-13.jpg" alt="" loading="lazy" width="480" height="270">
  <span class="post-sum">One or two sentences — the finding, not a teaser.</span>
</a>
```

- **`href`** — the LinkedIn permalink
- **`post-n`** — the part chip
- **`post-t`** — the headline
- **`post-sum`** — the summary. Say what the piece found. "Merchant density is a moat" beats "an interesting look at merchant dynamics."
- **`alt=""`** — leave it empty. The thumbnail is decorative; the title already names the link, and a screen reader reading both would repeat itself.

Then update the count in that series' header: `Series 1 &middot; 12 parts &middot; complete`.

## Adding a whole new series

Copy this block and put it above or below the existing ones — newest first is the usual order:

```html
<section id="series-slug">
  <div class="sec-head">
    <h2>Series title</h2>
    <span class="small muted">Series 3 &middot; 5 parts &middot; in progress</span>
  </div>

  <div class="posts">

    <a class="post" href="PASTE-LINKEDIN-URL">
      <span class="post-head"><span class="post-n">Part 1</span><span class="post-t">Headline</span></span>
      <img class="post-thumb" src="assets/covers/xx-01.jpg" alt="" loading="lazy" width="480" height="270">
      <span class="post-sum">One or two sentences.</span>
    </a>

  </div>
</section>
```

`id="series-slug"` is the anchor — lowercase, no spaces. Use it to link from the homepage: `writing.html#series-slug`.

## Cover thumbnails

Live in `assets/covers/`, 480px wide, 16:9.

**For a new part of the SEA Subsidy Wars series** — if you've published it to LinkedIn and saved the PDF to the Published Draft folder, regenerate everything at once:

```bash
python3 tools/extract-covers.py
```

**For a new series** — export the cover at 16:9 from wherever you design it, resize to 480px wide, and save it as `assets/covers/<prefix>-01.jpg`. Use a short prefix per series (`sw-` for Subsidy Wars, `ge-` for Great Extraction) so files stay grouped.

If you'd rather not resize by hand, drop the full-size image in `assets/covers/` and tell me — it's a one-line script.

## Featuring parts on the homepage

The homepage shows three. They're in `_pages/index.html` under "Writing", using the exact same `<a class="post">` markup. Copy the rows you want from `writing.html` and paste them in, replacing what's there.

---

# Before you publish

- [ ] `python3 build.py`
- [ ] Refresh and read it — check nothing overflows on a narrow window
- [ ] New figures masked per the rule above
- [ ] New links actually work
- [ ] For a new project: linked from the homepage if it deserves a card
- [ ] For a new part: series count updated in the header

If something looks broken after an edit, you've almost certainly deleted half a tag. Undo and redo the edit — the site rebuilds from `_pages/` every time, so nothing is ever permanently lost.

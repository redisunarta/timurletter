# Adding a project to the Work page

Step by step. Nothing else — just this one task.

---

## What went wrong last time

Nothing, actually. Your edit was correct. **You just didn't run the build.**

```
_pages/work.html   edited 21:01   ← 5 projects  (your source)
work.html          built  20:46   ← 4 projects  (what the browser shows)
```

The browser reads `work.html`. That file is *generated* from `_pages/work.html`. Until you run `build.py`, the generated file still holds the previous version — so your new project exists on disk but never reaches the page.

**Think of it as two files:**

| File | What it is | Who touches it |
|---|---|---|
| `_pages/work.html` | Your writing. The source. | **You** |
| `work.html` | The finished page with header and footer added. | **`build.py`** |

I've run the build for you now, so all 5 projects are live. From here it's yours.

---

## The five steps

### 1. Open the file

In VS Code: **File → Open Folder** → select the `site` folder. Then in the sidebar open `_pages` → `work.html`.

Opening the whole folder rather than the single file means the sidebar stays there and you can jump between files.

### 2. Find where projects live

Press `⌘F` and search for `article class="case"`. You'll find five. Each one is a complete project, top to bottom:

```html
<article class="case" id="loyalty-point">
  <div class="case-num">04 &middot; Allo Bank &middot; New user reward</div>
  <h2>Sunset the loyalty point programme</h2>
  <p>First paragraph.</p>
  <p>Second paragraph.</p>
  <p class="case-out"><strong>Outcome:</strong> what changed.</p>
</article>
```

### 3. Copy one and paste it

Click anywhere inside a project. Put your cursor on the `<article` line, then hold **Shift** and click at the end of the `</article>` line — that selects the whole block. Copy it, move to where you want the new project, and paste.

Leave a blank line between projects so the file stays readable.

### 4. Change five things

```html
<article class="case" id="fraud-network">        ← 1. new id, lowercase, no spaces
  <div class="case-num">05 &middot; Allo Bank &middot; Fraud detection</div>   ← 2. number · company · method
  <h2>Found the ring gaming a new-user campaign</h2>                          ← 3. outcome-led title
  <p>What was at stake.</p>                                                   ← 4. your paragraphs
  <p>What you did about it.</p>
  <p class="case-out"><strong>Outcome:</strong> <strong>Rp XX billion</strong> saved.</p>  ← 5. the result
</article>
```

**The `id` must be unique on the page.** It's the anchor — `work.html#fraud-network` jumps straight to it. If two projects share an id, links break silently.

Add as many `<p>` paragraphs as you want. Spacing is automatic.

### 5. Save, build, refresh

Save in VS Code: `⌘S`.

Then open Terminal and run:

```bash
cd "/Users/redisunarta/Documents/Personal Website/site"
python3 build.py
```

You should see:

```
  work.html       7,987 bytes
Built 6 pages.
```

Then refresh the browser. **This step is not optional** — it's the one that was missing.

---

## Making the build easier

Typing that `cd` every time gets old. Two better options.

### Option A — Terminal inside VS Code

With the `site` folder open in VS Code, press **`` ⌃` ``** (Control + backtick). A terminal opens *already in the right folder*. Then you only ever type:

```bash
python3 build.py
```

Edit → `⌘S` → click terminal → `↑` then Enter (the up arrow recalls the last command) → refresh browser.

### Option B — one command that does everything

Paste this into Terminal once. It creates a shortcut called `buildsite`:

```bash
echo 'alias buildsite="cd \"/Users/redisunarta/Documents/Personal Website/site\" && python3 build.py"' >> ~/.zshrc
source ~/.zshrc
```

After that, from any folder, just type:

```bash
buildsite
```

---

## Checking your work before you build

VS Code tells you about broken HTML if you know where to look.

- **Colour** — tags are one colour, your text another. If a whole paragraph suddenly turns tag-coloured, you've left a `<` or `>` unclosed.
- **Matching tags** — click a `<article>` tag and VS Code highlights its `</article>`. If nothing highlights, one is missing.
- **Fold arrows** — the small `⌄` in the left margin collapses a block. If a project won't fold as one unit, its tags don't match.
- **Problems panel** — `⇧⌘M` lists syntax errors.

If the page looks wrong after building, you've almost certainly deleted half a tag. `⌘Z` back to working and redo the edit.

---

## The one rule that prevents every disaster

**Never edit `work.html` at the top level.** Only `_pages/work.html`.

The top-level file is overwritten on every build. Any edit you make there is destroyed the next time you run `build.py`, with no warning.

If you're unsure which file you have open, look at the top of it:

- Starts with `<div class="wrap">` → **`_pages/`**, correct, edit away
- Starts with `<!DOCTYPE html>` → generated file, close it without saving

---

## Your project 05 placeholder

It's live on the page right now as `XXXXX XXXX XXXXX`. When you're ready to write it:

1. Open `_pages/work.html`
2. Search for `xxx-xxx`
3. Replace the id, the `case-num`, the `<h2>`, the paragraphs, and the outcome
4. Save, `python3 build.py`, refresh

Keep `Rp XX billion` masked if the real figure is an internal Allo Bank number — that's the rule we set, and it's easier to keep than to walk back after publishing.

---

## Quick reference

```bash
# every single time, after editing _pages/work.html
cd "/Users/redisunarta/Documents/Personal Website/site"
python3 build.py
```

| Symptom | Cause |
|---|---|
| Change doesn't appear | Build not run, or you edited the top-level file |
| Page unstyled / doubled | A full HTML document was saved over a `_pages/` file |
| Layout broken after an edit | Half a tag deleted — undo and retry |
| Anchor link goes nowhere | Two projects share the same `id` |

# Images: the About photo and Writing covers

Two tasks, each with a size rule. Read the rule once and you'll never have to think about it again.

---

# The one rule behind both

**Export at 2× the size it's displayed. Never larger.**

A Retina screen packs two physical pixels into every CSS pixel. So an image shown at 200px needs 400px of real data to look sharp. Anything beyond that is bytes the visitor downloads and never sees.

| Where | Displayed at | Export at | Shape |
|---|---|---|---|
| About page photo | 200 × 200 | **440 × 440** | square, 1:1 |
| Writing cover | 160 × 90 | **480 × 270** | widescreen, 16:9 |

That's the whole thing. The rest is mechanics.

---

# 1. Changing the About page photo

**Done — your new headshot is live.** Refresh `about.html`. Here's how to do it yourself next time.

## Step 1 — prepare the image

The photo must be **square**. The site crops to a circle-ish square frame, and anything not square gets its edges cut off unpredictably.

Open your photo in **Preview** (double-click it):

1. **Tools → Adjust Size…** — check the current dimensions
2. Drag a selection box over your face and shoulders, keeping it square. Hold **Shift** while dragging to lock the square.
   - The Preview toolbar shows the selection size live — aim for a square at least 440 × 440
   - Leave a little space above your head; a face jammed against the top edge looks cramped
3. **Tools → Crop** (`⌘K`)
4. **Tools → Adjust Size…** → set Width to **440**, make sure "Scale proportionally" is ticked → OK
5. **File → Export…** → Format **JPEG**, Quality around 80–90%

## Step 2 — save it in the right place

Save it as:

```
site/assets/redi-440.jpg
```

**Overwrite the existing file, keeping the same name.** That way you don't have to touch any HTML at all — it just picks up the new picture.

If you'd rather use a new filename, you also have to edit `_pages/about.html` and change:

```html
<img class="portrait" src="assets/redi-440.jpg" width="200" height="200" alt="Redi Sunarta">
                           ^^^^^^^^^^^^^^^^^^^^ this
```

Keeping the same filename is simpler. I'd stick with it.

## Step 3 — build and check

```bash
cd "/Users/redisunarta/Documents/Personal Website/site"
python3 build.py
```

Then refresh. If the old photo still shows, your browser cached it — hit **`⇧⌘R`** (hard refresh).

## Composition notes

At 200px, detail disappears. What survives is the shape of your head and whether you're looking at the camera.

- **Crop tight.** Head and shoulders. A full-body shot at 200px is an unrecognisable smudge.
- **Face in the upper third.** That's how portraits are conventionally composed and it reads as more assured than a dead-centre face.
- **Plain background.** Busy backgrounds turn to noise at small sizes. Yours is a plain warm wall — ideal.

That's exactly how I cropped the current one: 600 × 600 pulled from your 698 × 831 original, face sitting around a third down, then scaled to 440.

---

# 2. Adding an article to the Writing page

Two parts: the cover image, then the HTML row.

## Step 1 — prepare the cover

Covers are **16:9** — the same shape as a widescreen video.

Your existing ones are 480 × 270. Match that.

**If you already have a LinkedIn cover** (1280 × 720 or similar), it's already 16:9. Just resize:

Preview → **Tools → Adjust Size…** → Width **480** → Export as JPEG, quality 80–85.

**If your image isn't 16:9**, crop first: drag a selection that's roughly twice as wide as it is tall, then Crop, then resize to 480 wide.

**Don't skip the resize.** A 1280px file where 480 will do is roughly 4× the bytes for zero visible gain. Twelve of those is a slow page.

### Naming

```
site/assets/covers/sw-13.jpg
```

The prefix groups a series:

| Prefix | Series |
|---|---|
| `sw-` | SEA Subsidy Wars |
| `ge-` | The Great Extraction (when you start adding covers) |

Numbers are two digits — `sw-09`, not `sw-9` — so they sort correctly in Finder.

### Shortcut for Subsidy Wars parts

If you've published the article to LinkedIn and saved its PDF into your **Published Draft** folder, skip Preview entirely:

```bash
cd "/Users/redisunarta/Documents/Personal Website/site"
python3 tools/extract-covers.py
```

That pulls the cover out of every PDF and writes all of them at the correct size automatically.

## Step 2 — add the row

Open `_pages/writing.html` in VS Code. Find the series, copy any existing `<a class="post">` block, paste it in position, and edit four things:

```html
<a class="post" href="https://www.linkedin.com/pulse/your-article">
  <span class="post-head"><span class="post-n">Part 13</span><span class="post-t">Your headline here</span></span>
  <img class="post-thumb" src="assets/covers/sw-13.jpg" alt="" loading="lazy" width="480" height="270">
  <span class="post-sum">One or two sentences saying what the piece found.</span>
</a>
```

| Edit | What |
|---|---|
| `href` | The LinkedIn permalink |
| `post-n` | The part label |
| `post-t` | The headline |
| `src` | Your new cover filename |
| `post-sum` | The summary |

**Leave `width="480" height="270"` alone.** Those aren't the display size — CSS handles that. They tell the browser the shape in advance so the page doesn't jump around while images load.

**Leave `alt=""` empty too.** The thumbnail is decorative; the headline right next to it already names the link. A screen reader would otherwise announce the same thing twice.

## Step 3 — update the count

In the series header, bump the number:

```html
<span class="small muted">Series 1 &middot; 13 parts &middot; complete</span>
```

## Step 4 — build and check

```bash
cd "/Users/redisunarta/Documents/Personal Website/site"
python3 build.py
```

Refresh, and confirm the thumbnail actually appears. A broken image icon means the filename in `src` doesn't match the file on disk — usually a capital letter or a `.png` vs `.jpg` mismatch. Filenames are case-sensitive once the site is online, even though your Mac is forgiving locally.

---

# Quick reference

```
site/assets/redi-440.jpg          About photo      440 × 440   square
site/assets/covers/sw-NN.jpg      Writing cover    480 × 270   16:9
site/assets/timur-logo.png        Homepage logo    440 × 440   square
```

**Format:** JPEG for photos and covers, quality 80–90. PNG only for logos and line art.

**Target file size:** 20–50 KB each. If a cover comes out over 100 KB, it's bigger than it needs to be — resize it down.

**Every time, after any change:**

```bash
cd "/Users/redisunarta/Documents/Personal Website/site"
python3 build.py
```

| Problem | Cause |
|---|---|
| Old photo still showing | Browser cache — hard refresh with `⇧⌘R` |
| Broken image icon | Filename mismatch — check spelling and extension |
| Photo looks squashed | Source wasn't square — recrop to 1:1 |
| Cover looks cropped oddly | Source wasn't 16:9 — recrop |
| Photo looks blurry | Exported under 440px — re-export larger |
| Page loads slowly | Images over ~100 KB — resize down |

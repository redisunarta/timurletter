# Deploying to timurletter.com with GitHub Pages

Free, HTTPS included, auto-deploys on every push.

---

## Step 0 — fix the two blockers first

Run the checker:

```bash
cd "/Users/redisunarta/Documents/Personal Website/site"
python3 tools/check.py
```

Right now it reports **6 errors**. Both are real and would be visible to anyone who visits.

### Blocker 1 — the resume link is broken

`about.html` links to `resume/Redi-Sunarta-Resume.pdf`, and that folder is empty. Live, it's a 404.

**Either** export the masked resume (see §1.5 of the checklist — currency figures as `XX`) and save it exactly as:

```
site/resume/Redi-Sunarta-Resume.pdf
```

**Or** remove the link for now. In `_pages/about.html`, change:

```html
<div class="sec-head">
  <h2>Experience</h2>
  <a href="resume/Redi-Sunarta-Resume.pdf">Resume (PDF) &darr;</a>
</div>
```

to just:

```html
<div class="sec-head">
  <h2>Experience</h2>
</div>
```

Add it back when the PDF is ready.

### Blocker 2 — 12 `[FILL]` placeholders

Three on each of the four project pages. They render as visible grey boxes reading "**[FILL]** How did you construct the comparison group?" — clearly unfinished.

**Either** fill them (see `PROJECT-PAGES.md`), **or** delete the `<div class="callout">…</div>` blocks so the section simply ends after the paragraphs above it.

**Don't publish with them showing.** A visible editorial note undoes the credibility the page is meant to build.

Rerun `python3 tools/check.py` until it passes.

---

## Step 1 — create the repository

1. Go to [github.com/new](https://github.com/new)
2. Repository name: **`timurletter`**
3. **Public** — GitHub Pages requires public on the free plan
4. Do **not** tick "Add a README" — the folder already has one
5. Click **Create repository**

Leave the page open; you'll need the URL.

---

## Step 2 — push the site

```bash
cd "/Users/redisunarta/Documents/Personal Website/site"

python3 build.py
python3 tools/check.py        # must pass

git init
git add -A
git status                    # ← READ THIS BEFORE COMMITTING
```

**Check `git status` carefully.** You should see about 61 files: the HTML, `css/`, `assets/`, `_pages/`, `_partials/`, `build.py`, `tools/`, and the `.md` guides.

You should **not** see any `.csv`, `.xlsx`, `.DS_Store`, or anything from `QRIS/` or `Data Raw/`. The `.gitignore` blocks those, but verify — git history is permanent, and a file deleted in a later commit is still readable from an earlier one.

If it looks right:

```bash
git commit -m "Personal site: work, writing, viz, about"
git branch -M main
git remote add origin https://github.com/redisunarta/timurletter.git
git push -u origin main
```

Git will ask you to sign in. Use a **personal access token**, not your password — GitHub stopped accepting passwords for git operations. Create one at **Settings → Developer settings → Personal access tokens → Tokens (classic)**, tick the `repo` scope, and paste it when prompted for a password.

---

## Step 3 — turn on Pages

1. In your repo: **Settings → Pages**
2. Under "Build and deployment", Source: **Deploy from a branch**
3. Branch: **`main`**, folder: **`/ (root)`**
4. **Save**

Wait a minute or two, then check `https://redisunarta.github.io/timurletter/`. It should load — possibly without styling, because the CSS path assumes the site sits at a domain root. That resolves itself once the custom domain is attached, so don't panic at this stage.

---

## Step 4 — attach the domain

**Do this on GitHub before touching DNS.** Configuring DNS toward GitHub before claiming the domain in your repo leaves a window where someone else could claim it.

1. **Settings → Pages → Custom domain**
2. Type `timurletter.com`
3. **Save**

The repo already contains a `CNAME` file with that domain, so this should match immediately.

---

## Step 5 — DNS

Wherever `timurletter.com` is registered, open its DNS settings and add these.

**Four `A` records** — name `@` (or blank, depending on the provider):

```
185.199.108.153
185.199.109.153
185.199.110.153
185.199.111.153
```

**Four `AAAA` records** — also name `@`, for IPv6:

```
2606:50c0:8000::153
2606:50c0:8001::153
2606:50c0:8002::153
2606:50c0:8003::153
```

**One `CNAME` record** for the www variant:

| Type | Name | Value |
|---|---|---|
| CNAME | `www` | `redisunarta.github.io` |

That last value is your GitHub username plus `.github.io` — **not** the repository name. With both configured, GitHub redirects `www.timurletter.com` to `timurletter.com` automatically.

**Delete any existing A, AAAA, or CNAME record on `@` or `www` first.** A leftover parking record from your registrar will conflict.

Verify after 10–30 minutes:

```bash
dig timurletter.com +noall +answer -t A
```

You should see the four GitHub IPs. DNS can take up to 24 hours to propagate fully, though it's usually much faster.

---

## Step 6 — HTTPS

Once DNS resolves, go back to **Settings → Pages** and tick **Enforce HTTPS**.

The option may be greyed out for up to 24 hours while GitHub provisions a certificate. That's normal — check back later. Don't skip it: the site declares `https://` in its canonical URLs, and serving over plain HTTP would contradict that.

---

## Publishing changes after launch

```bash
cd "/Users/redisunarta/Documents/Personal Website/site"

# 1. edit files in _pages/ or _partials/
# 2. rebuild
python3 build.py

# 3. check
python3 tools/check.py

# 4. publish
git add -A
git commit -m "what changed"
git push
```

Live in about a minute. If it doesn't update, check the **Actions** tab in your repo — a failed deploy shows there.

---

## What each deploy file does

| File | Why it exists |
|---|---|
| `CNAME` | Tells GitHub Pages this repo serves `timurletter.com`. Deleting it breaks the custom domain. |
| `.nojekyll` | **Essential.** GitHub runs Jekyll by default, which ignores any folder starting with `_`. Without this file, `_pages/` and `_partials/` are skipped and Jekyll may mangle the HTML. The file is empty — its presence is the signal. |
| `.gitignore` | Blocks spreadsheets, personal folders, and scratch images from ever being committed. |
| `robots.txt` | Points crawlers at the sitemap. |
| `sitemap.xml` | Regenerated by `build.py` on every run, so it can't drift. |

---

## After launch

- **Google Search Console** — add `timurletter.com`, submit `https://timurletter.com/sitemap.xml`
- **Update your bios** — LinkedIn, GitHub, Tableau should point at the new domain
- **Test the OG preview** — paste the URL into a LinkedIn message to yourself and check the card renders
- **`redisunarta.xyz`** — you still own it. Either redirect it to `timurletter.com` at the registrar, or leave it parked. Don't serve the same site on both: duplicate content splits your search ranking.

---

## If something breaks

| Symptom | Cause |
|---|---|
| Site loads but unstyled | Custom domain not attached yet — the CSS path assumes a domain root |
| 404 on every page | Pages source set to the wrong branch or folder |
| "Domain already taken" | The domain is attached to another repo — remove it there first |
| HTTPS checkbox greyed out | Certificate still provisioning; wait, up to 24 hours |
| `_pages/` contents showing publicly | `.nojekyll` missing |
| Changes not appearing | Forgot `python3 build.py` before committing |

---

## One honest caveat

The repo is public, which means **anyone can read your source** — including the `_pages/` files and these guide documents. Nothing there is sensitive, and the commercial figures are masked. But it does mean the `XX` masking is visible as a deliberate choice rather than looking like the numbers never existed.

That's fine, and arguably to your credit. Just know it's public before you push.

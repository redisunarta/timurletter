#!/usr/bin/env python3
"""
Pre-deploy check. Run before every push.

    python3 tools/check.py

Catches the things that are invisible locally but obvious once the site is
public: broken internal links, missing images, unclosed tags, leftover
placeholders, and files that should never be committed.

Exits non-zero if anything is wrong, so it can gate a deploy.
"""

import glob
import hashlib
import os
import re
import sys
from html.parser import HTMLParser

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

errors, warnings = [], []
VOID = {'meta', 'link', 'img', 'br', 'hr', 'input', 'source',
        'area', 'base', 'col', 'embed', 'param', 'track', 'wbr'}


class Page(HTMLParser):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.stack, self.ids, self.imgs, self.links, self.heads = [], set(), [], [], []
        self.title = self.desc = None
        self._in_title = False

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag == 'title':
            self._in_title = True
        if tag == 'meta' and d.get('name') == 'description':
            self.desc = d.get('content')
        if 'id' in d:
            self.ids.add(d['id'])
        if tag == 'img':
            self.imgs.append(d)
        if tag == 'a' and 'href' in d:
            self.links.append(d['href'])
        if tag in ('h1', 'h2', 'h3', 'h4'):
            self.heads.append(tag)
        if tag not in VOID:
            self.stack.append((tag, self.getpos()[0]))

    def handle_endtag(self, tag):
        if tag == 'title':
            self._in_title = False
        if tag in VOID:
            return
        if self.stack and self.stack[-1][0] == tag:
            self.stack.pop()
        elif tag in [t for t, _ in self.stack]:
            open_tag, line = self.stack[-1]
            errors.append(f"{self.name}: </{tag}> closed while <{open_tag}> "
                          f"(opened line {line}) is still open")
            while self.stack and self.stack.pop()[0] != tag:
                pass
        else:
            errors.append(f"{self.name}: stray </{tag}> at line {self.getpos()[0]}")

    def handle_data(self, data):
        if self._in_title:
            self.title = (self.title or '') + data


pages = sorted(glob.glob("*.html"))
if not pages:
    sys.exit("no built pages found — run python3 build.py first")

parsed, ids_by_page = {}, {}
for name in pages:
    p = Page(name)
    p.feed(open(name, encoding='utf-8').read())
    parsed[name], ids_by_page[name] = p, p.ids

    if p.stack:
        errors.append(f"{name}: never closed {[t for t, _ in p.stack]}")
    if p.heads.count('h1') != 1:
        errors.append(f"{name}: {p.heads.count('h1')} <h1> (should be exactly 1)")
    if not p.title:
        errors.append(f"{name}: no <title>")
    if not p.desc:
        errors.append(f"{name}: no meta description")
    elif len(p.desc) > 160:
        warnings.append(f"{name}: meta description {len(p.desc)} chars (Google cuts ~160)")
    seen = set()
    for h in p.heads:
        lvl = int(h[1])
        if lvl > 1 and (lvl - 1) not in seen:
            errors.append(f"{name}: heading jumps to <{h}> with no <h{lvl-1}> before it")
        seen.add(lvl)
    for im in p.imgs:
        if 'alt' not in im:
            errors.append(f"{name}: <img> with no alt attribute — {im.get('src', '?')[:60]}")

# links and local files
for name, p in parsed.items():
    for href in p.links:
        if href.startswith(('http://', 'https://', 'mailto:')):
            continue
        if href.startswith('#'):
            if href[1:] not in p.ids:
                errors.append(f"{name}: link to #{href[1:]} but no element has that id")
            continue
        path = href.split('#')[0]
        frag = href.split('#')[1] if '#' in href else None
        if path and not os.path.exists(path):
            errors.append(f"{name}: links to {path} — that file does not exist")
        elif frag and path in ids_by_page and frag not in ids_by_page[path]:
            errors.append(f"{name}: links to {path}#{frag} — no such id on that page")

# every referenced local asset exists
for name in pages:
    src = open(name, encoding='utf-8').read()
    for ref in set(re.findall(r'(?:href|src)="(?!https?://|mailto:|#)([^"]+)"', src)):
        f = ref.split('#')[0]
        if f and not os.path.exists(f):
            errors.append(f"{name}: missing asset {f}")

# placeholders that must not go live
for name in pages:
    src = open(name, encoding='utf-8').read()
    if '[FILL]' in src:
        errors.append(f"{name}: still contains {src.count('[FILL]')} [FILL] placeholder(s)")
    if 'TODO-LINK' in src:
        errors.append(f"{name}: still contains TODO-LINK placeholders")
    if 'todo-banner' in src:
        errors.append(f"{name}: build-note banner still present — delete it")
    if re.search(r'\bXXXXX\b', src):
        warnings.append(f"{name}: contains XXXXX — an unfinished draft?")

# shared chrome must be identical everywhere
foots = set()
for name in pages:
    s = open(name, encoding='utf-8').read()
    i, j = s.index('<footer class="site-foot">'), s.index('</footer>') + 9
    foots.add(hashlib.md5(s[i:j].encode()).hexdigest())
if len(foots) != 1:
    errors.append(f"footer differs across pages ({len(foots)} variants) — rerun build.py")

# every class used has a rule
css = open("css/style.css", encoding='utf-8').read()
used = set()
for name in pages:
    for c in re.findall(r'class="([^"]+)"', open(name, encoding='utf-8').read()):
        used.update(c.split())
for c in sorted(used):
    if not re.search(r'\.' + re.escape(c) + r'(?=[\s,{:.\[])', css):
        warnings.append(f"class .{c} used in HTML but has no CSS rule")

# the resume PDF must follow the same masking rule as the pages
for pdf_path in glob.glob("resume/*.pdf"):
    try:
        import pdfplumber
    except ImportError:
        warnings.append(f"{pdf_path}: install pdfplumber to check masking "
                        f"(pip3 install pdfplumber)")
        break
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = "\n".join((pg.extract_text() or "") for pg in pdf.pages)
    except Exception as e:
        warnings.append(f"{pdf_path}: could not read ({e})")
        continue
    found = re.findall(r'(?:Rp\s?\d[\d.,]*\s?(?:billion|million|bn|mn)'
                       r'|\$\s?\d[\d.,]*\s?(?:billion|million|bn|mn))', text)
    if found:
        errors.append(f"{pdf_path}: contains UNMASKED figures {sorted(set(found))} "
                      f"— the site masks these as XX. Publishing the raw PDF "
                      f"undoes that decision.")

# The OG card is a baked PNG, not rendered from the page, so editing the site
# copy does NOT update it. It shipped once showing the old domain and the old
# tagline for exactly this reason. Two guards:
#   1. the copy constants in make-og.py must still match the live site
#   2. the PNG must be newer than the sources that describe it
OG = "assets/og.png"
if not os.path.exists(OG):
    errors.append(f"{OG} missing — run python3 tools/make-og.py")
elif os.path.exists("tools/make-og.py"):
    gen = open("tools/make-og.py", encoding='utf-8').read()

    def const(name):
        m = re.search(rf'^{name}\s*=\s*(.+?)(?:\s*#.*)?$', gen, re.M)
        if not m:
            return None
        try:
            return eval(m.group(1), {}, {})
        except Exception:
            return None

    build_src = open("build.py", encoding='utf-8').read()
    m = re.search(r'^DOMAIN\s*=\s*["\']([^"\']+)', build_src, re.M)
    site_domain = re.sub(r'^https?://', '', m.group(1)).rstrip('/') if m else None
    og_domain = const("DOMAIN")
    if site_domain and og_domain and og_domain != site_domain:
        errors.append(f"OG card shows domain '{og_domain}' but the site is "
                      f"'{site_domain}' — rerun tools/make-og.py")

    tagline = const("TAGLINE")
    if tagline and os.path.exists("index.html"):
        home = open("index.html", encoding='utf-8').read()
        m = re.search(r'<meta property="og:title" content="([^"]*)"', home)
        if m and tagline.lower() not in m.group(1).lower():
            warnings.append(f"OG card tagline '{tagline}' does not appear in the "
                            f"home og:title '{m.group(1)}' — is the card stale?")

    newest = max((os.path.getmtime(f) for f in
                  ("_pages/index.html", "_partials/head.html",
                   "build.py", "tools/make-og.py")
                  if os.path.exists(f)), default=0)
    if os.path.getmtime(OG) < newest - 1:
        warnings.append(f"{OG} is older than the page sources — the card may "
                        f"show outdated copy. Rerun tools/make-og.py")

# deploy plumbing
if not os.path.exists("CNAME"):
    warnings.append("no CNAME file — custom domain will not work on GitHub Pages")
if not os.path.exists(".nojekyll"):
    errors.append("no .nojekyll file — GitHub will run Jekyll and skip _pages/ and _partials/")

print(f"checked {len(pages)} pages\n")
for e in errors:
    print(f"  ERROR    {e}")
for w in warnings:
    print(f"  warning  {w}")
if not errors and not warnings:
    print("  all clear")
print()
if errors:
    print(f"{len(errors)} error(s) — fix before deploying.")
    sys.exit(1)
print(f"{len(warnings)} warning(s), no errors. Safe to deploy.")

#!/usr/bin/env python3
"""
Assemble the site from _partials/ + _pages/ into root-level HTML.

Single source of truth:
  _partials/head.html   <head>, site header, opening <main>
  _partials/foot.html   closing </main>, site footer, closing tags
  _partials/next.html   the "keep reading" block appended to each page
  _pages/*.html         the unique body of each page — nothing else

Run after editing anything. No dependencies.

    python3 build.py

Never edit the generated files at the root — they are overwritten.
"""

import datetime
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).parent
YEAR = datetime.date.today().year

# Change this one line if the domain ever moves. It feeds canonical URLs,
# Open Graph tags, the JSON-LD block, and the sitemap.
DOMAIN = "https://timurletter.com"

JSONLD = """<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Person",
  "name": "Redi Sunarta",
  "url": "__DOMAIN__/",
  "image": "__DOMAIN__/assets/redi-440.jpg",
  "jobTitle": "Business Intelligence Analyst, Manager",
  "worksFor": { "@type": "Organization", "name": "Allo Bank" },
  "alumniOf": { "@type": "CollegeOrUniversity", "name": "Universitas Indonesia" },
  "address": { "@type": "PostalAddress", "addressLocality": "Jakarta", "addressCountry": "ID" },
  "email": "mailto:redi.sunarta@gmail.com",
  "knowsAbout": ["Promotional economics", "Incentive design", "Fraud detection",
                 "Causal inference", "Consumer tech", "Digital banking", "E-commerce"],
  "sameAs": [
    "https://www.linkedin.com/in/redisunarta",
    "https://x.com/redi_sunarta",
    "https://github.com/redisunarta",
    "https://public.tableau.com/app/profile/redi.sunarta"
  ]
}
</script>
"""

# slug -> page config. `next` chains the pages together so every page ends
# with somewhere to go; set to None to omit the block.
PAGES = {
    "index.html": dict(
        toc=True,
        canonical="",
        nav=None,
        title="Redi Sunarta — Analytics for consumer tech companies",
        desc="I help consumer tech companies make promotional and incentive spend "
             "actually profitable. Business intelligence manager in Jakarta.",
        og_title="Redi Sunarta — Analytics for consumer tech companies",
        og_desc="I help consumer tech companies make promotional and incentive "
                "spend actually profitable.",
        og_type="website",
        extra_head=JSONLD,
        next=("work.html", "Work",
              "Projects in promotional economics, fraud detection, and causal "
              "inference."),
    ),
    "work.html": dict(
        toc=True,
        canonical="work.html",
        nav="work",
        title="Work — Redi Sunarta",
        desc="Notable projects in promotional and incentive economics, fraud "
             "detection, and causal inference at Allo Bank and Tokopedia.",
        og_title="Work — Redi Sunarta",
        og_desc="Notable projects in promotional economics, fraud detection, and "
                "causal inference.",
        og_type="website",
        next=("viz.html", "Data visualization",
              "Sixteen Tableau dashboards and the Datawrapper charts behind Timur."),
    ),
    # --- individual project pages -------------------------------------------
    # Each is a full case study. `nav="work"` keeps Work highlighted in the
    # header. The `next` chain walks a reader through all four in order and
    # then returns them to the index.
    "work-poml.html": dict(
        canonical="work-poml.html", nav="work",
        title="Measuring an ML coupon engine — Redi Sunarta",
        desc="Post-distribution measurement of Tokopedia's POML coupon-targeting "
             "engine: separating incremental conversion from conversion it would "
             "have got anyway.",
        og_title="Measured what an ML coupon engine actually saved",
        og_desc="A targeting engine reported the conversion of the buyers it "
                "targeted. That is not the same as what it caused.",
        og_type="article",
        next=("work-free-shipping.html", "Killed a free-shipping subsidy",
              "Synthetic control on a weight-based program in Surabaya and Makassar."),
    ),
    "work-free-shipping.html": dict(
        canonical="work-free-shipping.html", nav="work",
        title="Terminating a free-shipping subsidy — Redi Sunarta",
        desc="Synthetic control applied to a weight-based free-shipping program in "
             "Surabaya and Makassar, and the case for terminating it.",
        og_title="Killed a free-shipping subsidy in two cities",
        og_desc="Synthetic control built a counterfactual Surabaya and Makassar. The "
                "subsidy was not buying the volume it was credited with.",
        og_type="article",
        next=("work-loyalty.html", "Cut a retention program's cost",
              "Behavioural segmentation on a discount program leaking in two directions."),
    ),
    "work-loyalty.html": dict(
        canonical="work-loyalty.html", nav="work",
        title="Redesigning a retention program — Redi Sunarta",
        desc="Behavioural segmentation on a discount program leaking spend to promo "
             "abusers and to customers who needed no incentive to stay.",
        og_title="Cut a retention program's cost, kept its customers",
        og_desc="The program was paying two groups it never intended to: people "
                "gaming it, and people who needed no incentive at all.",
        og_type="article",
        next=("work-loyalty-point.html", "Sunset the loyalty point program",
              "Points were not making customers loyal. Most churned at redemption."),
    ),
    "work-loyalty-point.html": dict(
        canonical="work-loyalty-point.html", nav="work",
        title="Sunsetting a loyalty point program — Redi Sunarta",
        desc="Every major Indonesian fintech runs a points mechanism. Ours was "
             "paying customers who were already staying.",
        og_title="Sunset the loyalty point program",
        og_desc="Points were not making customers loyal. Most users churned once "
                "their points became redeemable.",
        og_type="article",
        next=("work.html", "All projects",
              "Back to the full list."),
    ),
    "viz.html": dict(
        canonical="viz.html",
        nav="viz",
        title="Data visualization — Redi Sunarta",
        desc="Sixteen public Tableau dashboards and six Datawrapper charts by Redi "
             "Sunarta — Indonesian poverty, income, labor, and markets.",
        og_title="Data visualization — Redi Sunarta",
        og_desc="Tableau dashboards and Datawrapper charts on Indonesian poverty, "
                "income, labor, and markets.",
        og_type="website",
        next=("writing.html", "Writing",
              "Timur — the same habit of mind applied to Southeast Asian tech."),
    ),
    "writing.html": dict(
        toc=True,
        canonical="writing.html",
        nav="writing",
        title="Writing — Timur, by Redi Sunarta",
        desc="Timur — a newsletter on Indonesian and Southeast Asian fintech by Redi "
             "Sunarta. Series 1: SEA Subsidy Wars, 12 parts. Series 2: The Great "
             "Extraction.",
        og_title="Timur — Indonesian and SEA fintech, by Redi Sunarta",
        og_desc="Mechanism-led, counterfactual writing on Southeast Asian tech. What "
                "would have happened without the intervention?",
        og_type="website",
        next=("about.html", "About",
              "Where the habit came from, and the five years of work behind it."),
    ),
    "about.html": dict(
        toc=True,
        canonical="about.html",
        nav="about",
        title="About — Redi Sunarta",
        desc="Analyst in Jakarta. Five years across digital banking at Allo Bank and "
             "marketplace promotions at Tokopedia — incentive economics and causal "
             "inference.",
        og_title="About — Redi Sunarta",
        og_desc="Business intelligence analyst in Jakarta. Promotional economics, fraud "
                "detection, causal inference.",
        og_type="profile",
        next=("work.html", "Work",
              "The projects that show the method rather than describe it."),
    ),
    "404.html": dict(
        canonical="404.html",
        nav=None,
        title="Not found — Redi Sunarta",
        desc="No page at this address.",
        og_title="Not found — Redi Sunarta",
        og_desc="No page at this address.",
        og_type="website",
        robots='<meta name="robots" content="noindex">',
        next=None,
    ),
}

CURRENT = ' aria-current="page"'


def slugify(text):
    """Heading text -> url-safe id."""
    t = re.sub(r"<[^>]+>", "", text)
    t = (t.replace("&middot;", " ").replace("&ndash;", "-").replace("&mdash;", "-")
           .replace("&rsquo;", "").replace("&amp;", "and").replace("&nbsp;", " "))
    t = re.sub(r"[^a-zA-Z0-9\s-]", "", t).strip().lower()
    return re.sub(r"[\s-]+", "-", t)[:60]


def build_toc(body):
    """Give every <h2> an id and return (body, toc_html).

    The outline is generated from the page's own headings, so it can never
    drift from the content. An h2 can carry data-toc="Short label" when its
    real heading is too long for a 180px sidebar.

    Returns ('', body) unchanged if the page has fewer than two headings —
    an outline listing one item is just clutter.
    """
    heads = list(re.finditer(r'<h2([^>]*)>(.*?)</h2>', body, re.S))
    if len(heads) < 2:
        return body, ""

    items, seen = [], set()
    for m in heads:
        attrs, text = m.group(1), m.group(2)
        label = re.search(r'data-toc="([^"]*)"', attrs)
        label = label.group(1) if label else re.sub(r"<[^>]+>", "", text).strip()

        existing = re.search(r'\bid="([^"]+)"', attrs)
        if existing:
            hid = existing.group(1)
        else:
            hid = slugify(text) or f"section-{len(items)+1}"
            n, base = 2, hid
            while hid in seen:
                hid, n = f"{base}-{n}", n + 1
            body = body.replace(m.group(0),
                                f'<h2 id="{hid}"{attrs}>{text}</h2>', 1)
        seen.add(hid)
        items.append(f'        <li><a href="#{hid}">{label}</a></li>')

    toc = ('    <nav class="toc" aria-label="On this page">\n'
           '      <p class="toc-h">On this page</p>\n'
           '      <ul>\n' + "\n".join(items) + '\n      </ul>\n'
           '    </nav>\n\n')
    return body, toc


def read(p):
    return (ROOT / p).read_text(encoding="utf-8")


def build():
    head_t = read("_partials/head.html")
    foot_t = read("_partials/foot.html")
    next_t = read("_partials/next.html")

    built = []
    for slug, cfg in PAGES.items():
        body = read(f"_pages/{slug}").rstrip("\n")

        if cfg.get("toc"):
            body, toc_html = build_toc(body)
            body = toc_html + body

        if cfg["next"]:
            nhref, nlabel, nblurb = cfg["next"]
            body += "\n" + (next_t
                            .replace("{{HREF}}", nhref)
                            .replace("{{LABEL}}", nlabel)
                            .replace("{{BLURB}}", nblurb)).rstrip("\n")

        head = (head_t
                .replace("{{DOMAIN}}", DOMAIN)
                .replace("{{TITLE}}", cfg["title"])
                .replace("{{DESC}}", cfg["desc"])
                .replace("{{SLUG}}", cfg["canonical"])
                .replace("{{OGTYPE}}", cfg["og_type"])
                .replace("{{OGTITLE}}", cfg["og_title"])
                .replace("{{OGDESC}}", cfg["og_desc"])
                .replace("{{ROBOTS}}", cfg.get("robots", ""))
                .replace("{{EXTRAHEAD}}", cfg.get("extra_head", "").replace("__DOMAIN__", DOMAIN))
                .replace("{{NAV_WORK}}", CURRENT if cfg["nav"] == "work" else "")
                .replace("{{NAV_VIZ}}", CURRENT if cfg["nav"] == "viz" else "")
                .replace("{{NAV_WRITING}}", CURRENT if cfg["nav"] == "writing" else "")
                .replace("{{NAV_ABOUT}}", CURRENT if cfg["nav"] == "about" else ""))

        foot = foot_t.replace("{{YEAR}}", str(YEAR))

        out = head + body + "\n\n" + foot
        out = re.sub(r"\n{3,}", "\n\n", out)
        (ROOT / slug).write_text(out, encoding="utf-8")
        built.append((slug, len(out)))

    # sitemap follows PAGES so it can never drift out of sync
    today = datetime.date.today().isoformat()
    urls = []
    for slug, cfg in PAGES.items():
        if cfg.get("robots"):
            continue
        loc = DOMAIN + "/" + cfg["canonical"]
        pri = "1.0" if slug == "index.html" else "0.8"
        urls.append(f"  <url><loc>{loc}</loc><lastmod>{today}</lastmod>"
                    f"<priority>{pri}</priority></url>")
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(urls) + "\n</urlset>\n", encoding="utf-8")

    for slug, n in built:
        print(f"  {slug:14} {n:6,} bytes")
    print(f"  sitemap.xml    {len(urls)} urls")
    print(f"\nBuilt {len(built)} pages.")


if __name__ == "__main__":
    try:
        build()
    except FileNotFoundError as e:
        sys.exit(f"missing file: {e.filename}")

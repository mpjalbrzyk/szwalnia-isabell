#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""MDX -> static HTML converter for Szwalnia ISABELL blog.
Self-contained (no external deps). Replicates the template structure of
ile-kosztuje-uszycie-partii-odziezy.html with inline styles.
"""
import re
import sys
import os
import math

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

HERO = {
    "jak-wybrac-szwalnie-10-pytan": "szycie-dla-marek-odziezowych-szwalnia.webp",
    "szycie-z-powierzonego-materialu": "krojownia-uslugowa-krojenie-tkanin.webp",
    "minimalne-zamowienie-szwalnia-moq": "male-serie-produkcja-testowa-szwalnia.webp",
    "kontrola-jakosci-szwalnia": "kontrola-jakosci-szycie-odziez.webp",
    "szwalnia-polska-vs-chiny": "hero-szwalnia-zabki-warsztat.webp",
    "jak-zamowic-odziez-firmowa-hr": "firmowa-bluzy-z-logo.webp",
    "probka-przeszyciowa-szwalnia": "male-serie-testowanie-prototyp-odziez.webp",
    "szycie-polska-oplacalnosc-2026": "szwlania-z-pokolenia-na-pokolenie.webp",
}

P_STYLE = "margin-bottom: 24px; line-height: 1.8; color: var(--text-body); font-size: 1.1rem;"
H2_STYLE = "margin-top: 48px; margin-bottom: 24px; font-family: 'DM Serif Display', serif; font-size: 2rem; color: var(--primary);"
H3_STYLE = "margin-top: 36px; margin-bottom: 16px; font-family: 'DM Serif Display', serif; font-size: 1.6rem; color: var(--primary);"
A_STYLE = "color: var(--accent); text-decoration: underline;"
LI_STYLE = "margin-bottom: 12px;"
UL_STYLE = "margin-bottom: 24px; padding-left: 20px;"


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def inline(t):
    t = esc(t)
    t = re.sub(r"\[([^\]]+)\]\(([^)]+)\)",
               lambda m: '<a href="%s" style="%s">%s</a>' % (m.group(2), A_STYLE, m.group(1)),
               t)
    t = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", t)
    return t


def slugify(t):
    t = t.lower().strip()
    t = re.sub(r"[^\w\sąćęłńóśźż-]", "", t, flags=re.UNICODE)
    t = re.sub(r"\s+", "-", t)
    return t


def parse_frontmatter(raw):
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", raw, re.DOTALL)
    fm_raw, body = m.group(1), m.group(2)
    fm = {"questions": [], "related": []}
    lines = fm_raw.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i]
        m2 = re.match(r"^(\w+):\s*(.*)$", line)
        if line.strip() == "schema:":
            i += 1
            while i < len(lines):
                ql = lines[i]
                qm = re.match(r"\s*-\s*question:\s*\"(.*)\"\s*$", ql)
                if qm:
                    q = qm.group(1)
                    i += 1
                    am = re.match(r"\s*answer:\s*\"(.*)\"\s*$", lines[i])
                    fm["questions"].append((q, am.group(1)))
                elif re.match(r"^\w+:", ql):
                    break
                i += 1
            continue
        if line.strip() == "relatedPosts:":
            i += 1
            while i < len(lines):
                rl = lines[i]
                sm = re.match(r"\s*-\s*slug:\s*\"(.*)\"\s*$", rl)
                if sm:
                    s = sm.group(1)
                    i += 1
                    lm = re.match(r"\s*label:\s*\"(.*)\"\s*$", lines[i])
                    fm["related"].append((s, lm.group(1)))
                elif re.match(r"^\w+:", rl):
                    break
                i += 1
            continue
        if m2:
            key, val = m2.group(1), m2.group(2).strip()
            if val.startswith('"') and val.endswith('"'):
                val = val[1:-1]
            fm[key] = val
        i += 1
    return fm, body


def render_table(rows):
    # rows: list of lists of raw cell strings; rows[0]=header, rows[1]=separator skipped
    header = rows[0]
    body_rows = rows[2:]
    out = ['<div style="overflow-x: auto; margin-top: 24px; margin-bottom: 32px;"><table style="width: 100%; border-collapse: collapse; text-align: left; border: 1px solid var(--border);">']
    out.append('<thead><tr style="background: var(--surface); border-bottom: 2px solid var(--border);">')
    for c in header:
        out.append('<th style="padding: 16px; font-weight: 700; color: var(--primary);">%s</th>' % inline(c.strip()))
    out.append("</tr></thead><tbody>")
    for r in body_rows:
        out.append('<tr style="border-bottom: 1px solid var(--border);">')
        for c in r:
            out.append('<td style="padding: 16px; color: var(--text-body);">%s</td>' % inline(c.strip()))
        out.append("</tr>")
    out.append("</tbody></table></div>")
    return "\n".join(out)


def split_row(line):
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]
    return line.split("|")


def render_body(body):
    lines = body.split("\n")
    html = []
    headings = []  # (id, text) for h2 TOC
    body_questions = []  # (q, a) parsed from a body "Najczęściej zadawane pytania" section
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]
        s = line.strip()
        if not s:
            i += 1
            continue
        # H1 -> skip (title goes to hero)
        if s.startswith("# "):
            i += 1
            continue
        # code fence
        if s.startswith("```"):
            i += 1
            buf = []
            while i < n and not lines[i].strip().startswith("```"):
                buf.append(lines[i])
                i += 1
            i += 1  # closing fence
            code = esc("\n".join(buf))
            html.append('<pre style="background: var(--surface); border: 1px solid var(--border); border-radius: 12px; padding: 24px; overflow-x: auto; font-size: 0.95rem; line-height: 1.6; margin-bottom: 24px;"><code>%s</code></pre>' % code)
            continue
        # headings
        if s.startswith("### "):
            txt = s[4:].strip()
            hid = slugify(txt)
            html.append('<h3 id="%s" style="%s">%s</h3>' % (hid, H3_STYLE, inline(txt)))
            i += 1
            continue
        if s.startswith("## "):
            txt = s[3:].strip()
            hid = slugify(txt)
            headings.append((hid, txt))
            html.append('<h2 id="%s" style="%s">%s</h2>' % (hid, H2_STYLE, inline(txt)))
            i += 1
            if hid == "najczęściej-zadawane-pytania":
                # Parse **Q** / answer blocks until next h2; render as accordion via placeholder
                while i < n and not lines[i].strip().startswith("## "):
                    ls = lines[i].strip()
                    if not ls:
                        i += 1
                        continue
                    qm = re.match(r"^\*\*(.+?)\*\*$", ls)
                    if qm:
                        q = qm.group(1).strip()
                        i += 1
                        while i < n and not lines[i].strip():
                            i += 1
                        ans = []
                        while (i < n and lines[i].strip()
                               and not lines[i].strip().startswith("## ")
                               and not re.match(r"^\*\*(.+?)\*\*$", lines[i].strip())):
                            ans.append(lines[i].strip())
                            i += 1
                        body_questions.append((q, " ".join(ans)))
                    else:
                        i += 1
                html.append("<!--FAQ_HERE-->")
            continue
        # table
        if s.startswith("|") and (i + 1 < n) and re.match(r"^\s*\|?[\s:|-]+\|?\s*$", lines[i + 1]):
            rows = []
            while i < n and lines[i].strip().startswith("|"):
                rows.append(split_row(lines[i]))
                i += 1
            html.append(render_table(rows))
            continue
        # list
        if re.match(r"^[-*]\s+", s):
            items = []
            while i < n and re.match(r"^[-*]\s+", lines[i].strip()):
                it = re.sub(r"^[-*]\s+", "", lines[i].strip())
                cb = re.match(r"^\[([ xX])\]\s+(.*)$", it)
                if cb:
                    mark = "☑" if cb.group(1).lower() == "x" else "☐"
                    it = mark + " " + cb.group(2)
                items.append('<li style="%s">%s</li>' % (LI_STYLE, inline(it)))
                i += 1
            html.append('<ul style="%s">%s</ul>' % (UL_STYLE, "".join(items)))
            continue
        # paragraph (gather until blank)
        buf = [s]
        i += 1
        while i < n and lines[i].strip() and not re.match(r"^(#{1,3}\s|[-*]\s|\||```)", lines[i].strip()):
            buf.append(lines[i].strip())
            i += 1
        para = " ".join(buf)
        html.append('<p style="%s">%s</p>' % (P_STYLE, inline(para)))
    return "\n".join(html), headings, body_questions


def build_toc(headings):
    if not headings:
        return ""
    items = []
    for hid, txt in headings:
        items.append('<li><a href="#%s" style="color:var(--text); text-decoration:none; border-bottom:1px dashed var(--border); transition:0.2s;">%s</a></li>' % (hid, inline(txt)))
    return ('<div class="blog-toc" style="background:var(--surface); padding:32px; border-radius:12px; border:1px solid var(--border); margin:48px 0;">'
            '<h3 style="font-family:\'DM Serif Display\', serif; font-size:1.5rem; color:var(--primary); margin-top:0; margin-bottom:16px;">Spis treści</h3>'
            '<ol style="margin-bottom:0; color:var(--text); line-height:1.8; padding-left:20px;">' + "".join(items) + "</ol></div>")


def build_related(related):
    if not related:
        return ""
    items = []
    for slug, label in related:
        items.append('<li><a href="/%s.html" style="color: var(--accent); text-decoration: underline;">%s</a></li>' % (slug, esc(label)))
    return ('<div style="background: var(--accent-light); padding: 24px; border-radius: 12px; margin: 32px 0;">'
            '<p style="font-weight: 700; color: var(--primary); margin-bottom: 8px;">Przeczytaj też:</p>'
            '<ul style="list-style: disc; padding-left: 20px; display: flex; flex-direction: column; gap: 8px;">' + "".join(items) + "</ul></div>")


def build_faq_html(questions):
    out = ['<div class="faq-container">']
    for q, a in questions:
        out.append('''                    <details class="faq-item" style="background: var(--surface); padding: 24px; border-radius: 12px; margin-bottom: 16px; border: 1px solid var(--border); cursor: pointer;">
                        <summary style="font-weight: 700; color: var(--primary); list-style: none; display: flex; justify-content: space-between; align-items: center; font-size: 1.1rem;">
                            %s

                        </summary>
                        <p style="margin-top: 16px; color: var(--text-body); line-height: 1.6;">%s</p>
                    </details>
                ''' % (esc(q), inline(a)))
    out.append("</div>")
    return "\n".join(out)


def json_escape(t):
    return t.replace("\\", "\\\\").replace('"', '\\"')


def strip_md(t):
    # Markdown links/bold -> plain text (for JSON-LD answers)
    t = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", t)
    t = re.sub(r"\*\*([^*]+)\*\*", r"\1", t)
    return t


def build_faq_jsonld(questions):
    items = []
    for q, a in questions:
        items.append('{"@type": "Question", "name": "%s", "acceptedAnswer": {"@type": "Answer", "text": "%s"}}' % (json_escape(strip_md(q)), json_escape(strip_md(a))))
    return '{"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [' + ",".join(items) + "]}"


def reading_time(body):
    words = len(re.findall(r"\w+", body, flags=re.UNICODE))
    return max(4, math.ceil(words / 200))


def convert(mdx_path):
    with open(mdx_path, encoding="utf-8") as f:
        raw = f.read()
    fm, body = parse_frontmatter(raw)
    slug = fm["slug"]
    title = fm["title"]
    meta_title = fm.get("metaTitle", title)
    meta_desc = fm.get("metaDescription", "")
    canonical = fm.get("canonical", "https://szwalnia-isabell.pl/%s.html" % slug)
    date = fm.get("date", "")
    updated = fm.get("updated", date)
    hero = HERO[slug]

    body_html, headings, body_questions = render_body(body)
    toc = build_toc(headings)
    related = build_related(fm["related"])
    all_questions = fm["questions"] + body_questions
    faq_html = build_faq_html(all_questions)
    faq_jsonld = build_faq_jsonld(all_questions)
    rt = reading_time(body)
    url = "https://szwalnia-isabell.pl/%s.html" % slug

    # split intro paragraph(s) before first h2 already included in body_html; insert TOC after first <p>?
    # Template: intro paragraphs, then TOC, then first h2. We insert TOC right before first <h2>.
    if "<h2" in body_html and toc:
        idx = body_html.index("<h2")
        body_html = body_html[:idx] + toc + "\n" + body_html[idx:]
    if "<!--FAQ_HERE-->" in body_html:
        # Accordion replaces the in-body FAQ section; related box goes at the very end
        article_inner = body_html.replace("<!--FAQ_HERE-->", faq_html) + "\n" + related
    else:
        # Fallback: FAQ heading + accordion appended after the related box
        faq_heading = '<h2 id="najczęściej-zadawane-pytania" style="%s">Najczęściej zadawane pytania</h2>' % H2_STYLE
        article_inner = body_html + "\n" + related + "\n" + faq_heading + "\n" + faq_html

    html = TEMPLATE.format(
        meta_title=esc(meta_title),
        meta_desc=esc(meta_desc),
        url=url,
        canonical=canonical,
        breadcrumb_name=esc(title),
        headline=json_escape(title),
        desc_json=json_escape(meta_desc),
        date=date,
        updated=updated,
        faq_jsonld=faq_jsonld,
        title=esc(title),
        author="Michał Jałbrzykowski",
        reading_time=rt,
        hero=hero,
        hero_alt=esc(fm.get("featuredImageAlt", title)),
        article=article_inner,
    )
    out_path = os.path.join(REPO, "%s.html" % slug)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    print("Wrote", out_path, "(%d min, %d h2)" % (rt, len(headings)))


TEMPLATE = r'''<!DOCTYPE html>
<html lang="pl">
<head>
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-WGN33C5N6D"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', 'G-WGN33C5N6D');
</script>

<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{meta_title}</title>
<meta name="description" content="{meta_desc}">
<meta property="og:title" content="{meta_title}">
<meta property="og:description" content="{meta_desc}">
<meta property="og:type" content="article">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=DM+Serif+Display&display=swap" rel="stylesheet" media="print" onload="this.media='all'">
<noscript><link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=DM+Serif+Display&display=swap" rel="stylesheet"></noscript>
<link rel="stylesheet" href="/style.css">
<style>
  .blog-post-header {{
    max-width: 800px;
    margin: 0 auto 60px;
    text-align: center;
  }}
  .blog-post-body {{
    max-width: 720px;
    margin: 0 auto;
    font-size: 1.15rem;
    line-height: 1.8;
    color: var(--text-body);
  }}
  .blog-post-body h2 {{
    font-family: 'DM Serif Display', serif;
    font-size: 2rem;
    color: var(--primary);
    margin: 48px 0 24px;
    scroll-margin-top: 100px;
  }}
  .blog-post-body h3 {{
    font-family: 'DM Serif Display', serif;
    font-size: 1.6rem;
    color: var(--primary);
    margin: 36px 0 16px;
  }}
  .blog-post-body p {{
    margin-bottom: 24px;
  }}
  .blog-post-body ul {{
    margin-bottom: 24px;
    padding-left: 20px;
  }}
  .blog-post-body li {{
    margin-bottom: 12px;
  }}
  .cross-sell-banner {{
    background: rgba(230,126,34,0.05);
    border-left: 4px solid var(--accent);
    padding: 32px;
    margin: 48px 0;
    border-radius: 0 16px 16px 0;
    display: flex;
    flex-direction: column;
    gap: 16px;
  }}
  .blog-soft-cta {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 60px 5%;
    max-width: 800px;
    margin: 80px auto;
    text-align: center;
    box-shadow: 0 10px 40px rgba(0,0,0,0.03);
    scroll-margin-top: 100px;
  }}
</style>

  <!-- Breadcrumb Schema -->
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
      {{
        "@type": "ListItem",
        "position": 1,
        "name": "Strona główna",
        "item": "https://szwalnia-isabell.pl/"
      }},
      {{
        "@type": "ListItem",
        "position": 2,
        "name": "Blog",
        "item": "https://szwalnia-isabell.pl/blog.html"
      }},
      {{
        "@type": "ListItem",
        "position": 3,
        "name": "{breadcrumb_name}",
        "item": "{url}"
      }}
    ]
  }}
  </script>

<meta property="og:image" content="https://szwalnia-isabell.pl/assets/og-cover.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:url" content="{url}">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/assets/favicon.ico" sizes="64x64">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<link rel="canonical" href="{canonical}" />
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "headline": "{headline}",
  "description": "{desc_json}",
  "datePublished": "{date}",
  "dateModified": "{updated}",
  "author": {{"@type": "Organization", "name": "Szwalnia ISABELL", "url": "https://szwalnia-isabell.pl"}},
  "publisher": {{"@type": "Organization", "name": "Szwalnia ISABELL", "logo": {{"@type": "ImageObject", "url": "https://szwalnia-isabell.pl/assets/og-cover.png"}}}},
  "mainEntityOfPage": "{url}",
  "image": "https://szwalnia-isabell.pl/assets/og-cover.png"
}}
</script>
<script type="application/ld+json">
{faq_jsonld}
</script>
</head>
<body>

  <a href="#main" class="skip-link">Przejdź do treści</a>

  <!-- NAVBAR -->
  <div class="navbar-wrapper">
    <nav class="navbar">
      <a href="/" class="logo"><img src="/assets/logo-szwalnia-isabell-v21.webp" alt="Szwalnia ISABELL" width="160" height="auto"></a>
      <ul class="nav-links">
        <li class="nav-dropdown">
          <a href="/uslugi.html" class="nav-dropdown-trigger">Usługi <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="6 9 12 15 18 9"/></svg></a>
          <div class="dropdown-menu">
            <a href="/uslugi/szycie-odziez-damska.html">Szycie odzieży damskiej</a>
            <a href="/uslugi/odziez-firmowa.html">Odzież firmowa na zamówienie</a>
            <a href="/uslugi/krojenie-wykonczenie.html">Krojenie i wykończenie</a>
            <a href="/uslugi/male-serie.html">Małe serie</a>
            <a href="/szwalnia-warszawa.html">Szwalnia Warszawa</a>
            <a href="/szwalnia-zabki.html">Szwalnia Ząbki</a>
          </div>
        </li>
        <li><a href="/realizacje.html">Realizacje</a></li>
        <li><a href="/o-nas.html">O nas</a></li>
        <li><a href="/kontakt.html">Kontakt</a></li>
        <li><a href="/blog.html">Blog</a></li>
      </ul>
      <a href="/kontakt.html" class="btn-nav">Wyślij zapytanie</a>
      <button class="hamburger" aria-label="Menu" aria-expanded="false">
        <span></span><span></span><span></span>
      </button>
    </nav>
  </div>

  <!-- MOBILE MENU -->
  <div class="mobile-menu" id="mobile-menu">
    <ul>
      <li class="mobile-dropdown">
        <button class="mobile-dropdown-trigger">Usługi <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="6 9 12 15 18 9"/></svg></button>
        <ul class="mobile-dropdown-menu">
          <li><a href="/uslugi/szycie-odziez-damska.html">Szycie odzieży damskiej</a></li>
          <li><a href="/uslugi/odziez-firmowa.html">Odzież firmowa</a></li>
          <li><a href="/uslugi/krojenie-wykonczenie.html">Krojenie i wykończenie</a></li>
          <li><a href="/uslugi/male-serie.html">Małe serie</a></li>
          <li><a href="/szwalnia-warszawa.html">Szwalnia Warszawa</a></li>
          <li><a href="/szwalnia-zabki.html">Szwalnia Ząbki</a></li>
        </ul>
      </li>
      <li><a href="/realizacje.html">Realizacje</a></li>
      <li><a href="/o-nas.html">O nas</a></li>
      <li><a href="/kontakt.html">Kontakt</a></li>
      <li><a href="/blog.html">Blog</a></li>
      <li><a href="/kontakt.html" class="btn-nav">Wyślij zapytanie</a></li>
    </ul>
  </div>

  <main id="main">
    <nav class="breadcrumbs" aria-label="breadcrumb">
      <ul>
        <li><a href="/">Strona główna</a></li>
        <li><span class="separator">/</span></li>
        <li><a href="/blog.html">Blog</a></li>
        <li><span class="separator">/</span></li>
        <li aria-current="page">{title}</li>
      </ul>
    </nav>

  <!-- BLOG HERO HEADER -->
  <header style="padding: 180px 5% 40px;">
    <div class="blog-post-header">
      <a href="/blog.html" style="display: inline-block; margin-bottom: 24px; font-weight: 700; color: var(--accent); text-transform: uppercase; letter-spacing: 0.1em; text-decoration: none;">&larr; Powrót do artykułów</a>
      <h1 style="font-family: 'DM Serif Display', serif; font-size: 3.5rem; color: var(--primary); line-height: 1.2; margin-bottom: 24px;">{title}</h1>
      <div style="font-size: 1.05rem; color: var(--text-muted); display: flex; align-items: center; justify-content: center; gap: 16px;">
        <span><strong>{author}</strong></span>
        <span>•</span>
        <span>Opublikowano: {date}</span>
        <span>•</span>
        <span>{reading_time} minut czytania</span>
      </div>
    </div>

    <div style="max-width: 1000px; margin: 0 auto 80px; height: 500px; border-radius: 16px; overflow: hidden; border: 1px solid var(--border); box-shadow: 0 10px 40px rgba(0,0,0,0.06);">
      <img src="/assets/{hero}" alt="{hero_alt}" style="width: 100%; height: 100%; object-fit: cover;">
    </div>
  </header>

  <!-- BODY CONTENT -->
  <article class="blog-post-body" style="padding: 0 5%;">
{article}
</article>

  <!-- SOFT CTA FORM -->
  <section id="niezobowiazujacy-kontakt" class="blog-soft-cta" style="margin-top: 60px;">
    <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 12px; margin-bottom: 24px;">
      <img src="/assets/michal-jalbrzykowski-isabell.webp" alt="Michał z zespołem ISABELL" style="width: 80px; height: 80px; border-radius: 50%; object-fit: cover; border: 3px solid #fff; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
      <span style="font-weight: 700; color: var(--accent); text-transform: uppercase; letter-spacing: 0.05em; font-size: 0.9rem;">Michał z ISABELL</span>
    </div>

    <h3 style="font-family: 'DM Serif Display', serif; font-size: 2.2rem; margin-bottom: 16px; color: var(--primary);">Złapmy niezobowiązujący kontakt!</h3>
    <p style="font-size: 1.15rem; color: var(--text-body); margin-bottom: 40px; line-height: 1.6;">Masz pytania o swój projekt albo chcesz poznać wycenę? Napisz wiadomość. Przeanalizujemy Twój pomysł i przygotujemy rzetelne informacje dla Twojego projektu, bez ukrytych opłat i zobowiązań.</p>

    <form class="contact-form" id="contact-form" action="https://hook.eu1.make.com/iuy4kuiieqqawf3bfw9iq0jxgjh75ggr" method="POST" style="display: grid; gap: 24px; text-align: left;">
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 24px;">
        <div class="input-group">
          <label for="blog-name">Jak masz na imię?</label>
          <input type="text" id="blog-name" name="name" class="input-field" placeholder="Jan" required>
        </div>
        <div class="input-group">
          <label for="blog-contact">Twój telefon lub e-mail</label>
          <input type="text" id="blog-contact" name="contact" class="input-field" placeholder="Gdzie mamy odpowiedzieć?" required>
        </div>
      </div>
      <div class="input-group">
        <label for="blog-message">Co chodzi Ci po głowie? (Luźny opis pomysłów, wątpliwości na temat projektu)</label>
        <textarea id="blog-message" name="message" class="input-field" rows="4" placeholder="Cześć! Ostatnio myślałem nad autorską linią..." required></textarea>
      </div>
      <button type="submit" class="submit-btn" style="width: 100%; background: var(--primary); margin-top: 8px;">Wyślij wiadomość i porozmawiajmy</button>
      <p style="font-size: 0.85rem; color: var(--text-muted); text-align: center; margin-top: 8px;">Odpowiem najszybciej jak to możliwe (maksymalnie w ciągu 24h). Nie przesyłamy spamu.</p>
    </form>
  </section>

  </main>

  <!-- FOOTER -->
  <footer class="footer">
    <div class="footer-grid">
      <div class="footer-brand">
        <a href="/" class="logo"><img src="/assets/logo-szwalnia-isabell-v21.webp" alt="Szwalnia ISABELL" width="160" height="auto"></a>
        <p>Rodzinna szwalnia z tradycją w Ząbkach pod Warszawą. Krojenie, szycie i wykończenie pod jednym dachem.</p>
      </div>
      <div class="footer-col">
        <h4>Usługi</h4>
        <ul>
          <li><a href="/uslugi/szycie-odziez-damska.html">Szycie odzieży damskiej</a></li>
          <li><a href="/uslugi/odziez-firmowa.html">Odzież firmowa</a></li>
          <li><a href="/uslugi/krojenie-wykonczenie.html">Krojenie i wykończenie</a></li>
          <li><a href="/uslugi/male-serie.html">Małe serie</a></li>
          <li><a href="/szwalnia-warszawa.html">Szwalnia Warszawa</a></li>
          <li><a href="/szwalnia-zabki.html">Szwalnia Ząbki</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>Strony informacyjne</h4>
        <ul>
          <li><a href="/realizacje.html">Realizacje</a></li>
          <li><a href="/o-nas.html">O nas</a></li>
          <li><a href="/kontakt.html">Kontakt</a></li>
          <li><a href="/blog.html">Blog</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>Kontakt</h4>
        <ul>
          <li>Ząbki, ul. Batorego 44</li>
          <li>Pon-Pt: 8:00-15:00</li>
          <li><a href="tel:+48730851555">+48 730 851 555</a></li>
          <li><a href="mailto:kontakt@isabell.pl">kontakt@isabell.pl</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <p>© 2026 Szwalnia ISABELL. Wszelkie prawa zastrzeżone.</p>
      <a href="/polityka-prywatnosci.html">Polityka prywatności</a>
    </div>
  </footer>

  <script>
    const hamburger = document.querySelector('.hamburger');
    const mobileMenu = document.getElementById('mobile-menu');
    hamburger.addEventListener('click', () => {{
      hamburger.classList.toggle('active');
      mobileMenu.classList.toggle('active');
      hamburger.setAttribute('aria-expanded', mobileMenu.classList.contains('active'));
      document.documentElement.classList.toggle('menu-open', mobileMenu.classList.contains('active'));
    }});

    mobileMenu.querySelectorAll('a').forEach(link => {{
      link.addEventListener('click', () => {{
        hamburger.classList.remove('active');
        mobileMenu.classList.remove('active');
        document.documentElement.classList.remove('menu-open');
      }});
    }});

    const mobileDropdownTrigger = document.querySelector('.mobile-dropdown-trigger');
    if (mobileDropdownTrigger) {{
      mobileDropdownTrigger.addEventListener('click', () => {{
        mobileDropdownTrigger.closest('.mobile-dropdown').classList.toggle('active');
      }});
    }}

    const contactForm = document.getElementById('contact-form');
    if (contactForm && !contactForm.dataset.ajaxLoaded) {{
      contactForm.dataset.ajaxLoaded = 'true';
      contactForm.addEventListener('submit', function(e) {{
        e.preventDefault();
        const btn = contactForm.querySelector('button[type="submit"]');
        btn.innerHTML = 'Wysyłanie...';
        btn.disabled = true;

        const formData = new FormData(contactForm);

        fetch(contactForm.action, {{
          method: 'POST',
          headers: {{
            'Accept': 'application/json'
          }},
          body: formData
        }})
        .then(response => {{
          if (response.ok) {{
            contactForm.innerHTML = '<div style="text-align:center; padding: 40px 0;"><svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="var(--primary)" stroke-width="2" style="margin-bottom:16px"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg><h3 style="margin-bottom:8px">Wiadomość wysłana!</h3><p style="color:var(--text-body)">Dziękuję za wiadomość. Przeanalizuję zapytanie i odezwę się do Ciebie najszybciej, jak to możliwe.</p></div>';
          }} else {{
            btn.innerHTML = 'Wystąpił błąd. Spróbuj ponownie.';
            btn.disabled = false;
          }}
        }})
        .catch(error => {{
          btn.innerHTML = 'Błąd połączenia sieciowego.';
          btn.disabled = false;
        }});
      }});
    }}
</script>
<script src="/assets/form-handler.js"></script>
</body>
</html>
'''


if __name__ == "__main__":
    for path in sys.argv[1:]:
        convert(path)

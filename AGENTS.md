# AGENTS.md — Tech Cottage

**Mission**: Migrate [rbsomeg.blogspot.com](https://rbsomeg.blogspot.com/) to
[ratulb.github.io/techcottage/](https://ratulb.github.io/techcottage/) — Jekyll + GitHub Pages,
blue-green gradient (`#0650b1` → `rgb(0,128,0)`), minima theme.

## Data source (changed from old instructions)

NOT a Blogger XML export. Source is **Google Takeout**:

```
takeout-20260628T114727Z-3-001.zip
  └── Takeout/Blogger/Blogs/tech cottage/feed.atom   ← Atom feed with ALL posts
```

Contains **28 LIVE posts** + **27 DRAFT posts** (total 55 entries in feed).

Images are **base64 data URIs** embedded in the Atom feed, not external URLs.
The old `scripts/blogger_to_jekyll.py` expects the old Blogger export XML
format — **it will NOT work** on this Atom feed. Needs to be rewritten to:
1. Parse Atom (`xml.etree.ElementTree` + `blogger:` namespace)
2. Extract + save base64 images to `assets/images/`
3. Emit standard Jekyll front-matter + markdown

## Key commands

```bash
# Extract the Atom feed
python3 -c "import zipfile; z=zipfile.ZipFile('takeout-*.zip'); open('feed.atom','wb').write(z.read('Takeout/Blogger/Blogs/tech cottage/feed.atom'))"

# After converter is written
python3 scripts/blogger_to_jekyll.py feed.atom

# No local testing needed — GitHub Pages builds on push
```

## What's done / what's left

| Done | Needs work |
|------|-----------|
| `_config.yml` — minima, feed/seo, `/techcottage` baseurl | **Converter script** — must parse Atom + extract base64 images |
| `Gemfile` — `github-pages` gem | **Wire CSS into layout** — minima needs `_includes/head.html` override or `extra_css` config |
| `assets/css/style.css` — gradient palette | **Image handling** — base64 → `assets/images/` files |
| `index.md`, `about.md` — basic pages | **Draft posts** — 27 drafts exist; decide include or skip |
| `references/` — mojo/rust CSS references | **Git init + push** — `gh repo create ratulb/techcottage --public --push` |

## CSS gradient summary (style.css)

Palette: `linear-gradient(120deg, #0650b1, rgb(0, 128, 0))`
- `html, body` — gradient with `background-attachment: fixed`
- `.wrapper, .site-header, .site-footer` — transparent
- `.post, .post-content, .post-list > li` — white `rgba(255,255,255,0.95)` cards
- Text on gradient: `#d4d4d8` / `#e6edf3` with `text-shadow`
- Code blocks: `#161B22` bg, `#E6EDF3` fg

## Repo structure

```tree
/
├── _config.yml          # Jekyll config (baseurl: /techcottage)
├── Gemfile              # github-pages gem
├── index.md             # layout: home
├── about.md             # layout: page
├── assets/css/style.css # gradient overrides
├── scripts/
│   └── blogger_to_jekyll.py  # STALE — expects old Blogger XML, not Atom
├── references/          # Mojo/Rust CSS for reference
├── _posts/              # (empty — to be generated)
├── _drafts/             # (empty)
└── takeout-*.zip        # actual data source
```

## Conventions

- `_config.yml` uses `include: - assets/css` — verify minima picks it up
- Permalink: `/:year/:month/:title/`
- Each post footer: `*Originally published on [rbsomeg.blogspot.com](...)*`
- No test/lint/typecheck commands exist — this is a static site

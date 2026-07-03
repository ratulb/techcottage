# AGENTS.md — Tech Cottage

Static blog: [ratulb.github.io/techcottage](https://ratulb.github.io/techcottage/) — Jekyll + minima + blue-green gradient. Migrated from Blogger via Google Takeout.

## Data source

```bash
# Extract Atom feed from Google Takeout zip
python3 -c "import zipfile; z=zipfile.ZipFile('takeout-*.zip'); open('feed.atom','wb').write(z.read('Takeout/Blogger/Blogs/tech cottage/feed.atom'))"

# Regenerate all posts/drafts/images
pip install html2text
python3 scripts/blogger_to_jekyll.py feed.atom    # -> _posts/, _drafts/, assets/images/
```

- `takeout-*.zip` and `feed.atom` are gitignored.
- Converter parses Atom (`xml.etree.ElementTree` + `blogger:` namespace), extracts base64 images to `assets/images/`, emits Jekyll front-matter + markdown.
- DRAFTS go to `_drafts/`, LIVE to `_posts/`. `_config.yml` has `future: true` so future-dated posts render locally.
- 28 live posts + 28 drafts generated. 12 images extracted. Running the converter again is a safe full-regenerate — it overwrites.

## Local dev

```bash
bundle install            # github-pages + jekyll-include-cache
bundle exec jekyll serve  # -> http://localhost:4000/techcottage/
```

## CI

`.github/workflows/jekyll.yml` — builds & deploys to GitHub Pages on push to `main`.

## Customizations (beyond minima defaults)

- `_includes/head.html` — loads `assets/css/style.css`, adds **MathJax** (`$...$` inline, `$$...$$` display)
- `_includes/footer.html` — empty (ships blank)
- `_layouts/home.html` — supports `post.tenmo_link` → renders a `[Tenmo]` link
- `_layouts/post.html` — same `tenmo_link` support in title
- `assets/css/style.css` — gradient palette: `linear-gradient(120deg, #0650b1, rgb(0,128,0))`, card-style posts, amber links (#fbbf24), dark code blocks (#161B22)

## Post conventions

- Footer: `*Originally published on [rbsomeg.blogspot.com](...)*` (added by converter for LIVE posts)
- Two recent posts (2026-06-30) use `tenmo_link: https://github.com/ratulb/tenmo` in front matter — linked in layout title and home page list item
- Permalink: `/:year/:month/:title/`
- Tags and categories in front matter (both used)

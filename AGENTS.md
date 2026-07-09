# AGENTS.md — Tech Cottage

Static blog: [ratulb.github.io/techcottage](https://ratulb.github.io/techcottage/) — Jekyll + minima + blue-green gradient. Migrated from Blogger via Google Takeout.

## Local dev

```bash
bundle install
bundle exec jekyll serve  # -> http://localhost:4000/techcottage/
```

`_config.yml` has `future: true` — future-dated posts render locally.

## Regenerating from Google Takeout

```bash
python3 -c "import zipfile; z=zipfile.ZipFile('takeout-*.zip'); open('feed.atom','wb').write(z.read('Takeout/Blogger/Blogs/tech cottage/feed.atom'))"
pip install html2text
python3 scripts/blogger_to_jekyll.py feed.atom    # -> _posts/, _drafts/, assets/images/
```

- `takeout-*.zip` and `feed.atom` are gitignored.
- DRAFTS go to `_drafts/`, LIVE to `_posts/`. Converter is idempotent — safe to re-run.

## CI

`.github/workflows/jekyll.yml` — builds & deploys to GitHub Pages on push to `main`.

## Customizations (beyond minima defaults)

- `_includes/head.html` — loads `assets/css/style.css`, adds **MathJax** (`$...$` inline, `$$...$$` display)
- `_includes/footer.html` — empty (overrides minima default)
- `_layouts/home.html` & `_layouts/post.html` — support `post.tenmo_link` front matter → renders `[Tenmo]` link
- `assets/css/style.css` — gradient `linear-gradient(120deg, #0650b1, rgb(0,128,0))`, card-style posts, amber links (`#fbbf24`), dark code blocks (`#161B22`)
- `_config.yml` excludes `AGENTS.md` and `README.md` from the built site

## Post front-matter conventions

- Permalink: `/:year/:month/:title/` (set in `_config.yml`)
- Tags and categories in front matter (both used)
- `tenmo_link: https://github.com/ratulb/tenmo` — renders a `[Tenmo]` link in post title and home page item
- Footer: `*Originally published on [rbsomeg.blogspot.com](...)*` — added by converter for LIVE posts only
- Older posts from converter use `layout: post` explicitly; newer posts rely on default
# Tech Cottage

Rust, Kubernetes, and systems programming — originally published on [rbsomeg.blogspot.com](https://rbsomeg.blogspot.com/).

## About

Migrated from Blogger to Jekyll + GitHub Pages. Built with the [minima](https://github.com/jekyll/minima) theme and a blue-green gradient palette.

## Local development

```bash
git clone https://github.com/ratulb/techcottage.git
cd techcottage
bundle install
bundle exec jekyll serve
```

The site will be at `http://localhost:4000/techcottage/`.

## Regenerating from source data

The Google Takeout export (`takeout-*.zip`) contains the original posts as an Atom feed
with embedded base64 images. To regenerate:

```bash
python3 -c "import zipfile; z=zipfile.ZipFile('takeout-*.zip'); open('feed.atom','wb').write(z.read('Takeout/Blogger/Blogs/tech cottage/feed.atom'))"
python3 scripts/blogger_to_jekyll.py feed.atom
```

## License

Content and code &copy; rbsomeg.

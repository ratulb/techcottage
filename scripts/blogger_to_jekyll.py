"""
Convert Google Takeout Atom feed to Jekyll markdown files.

Usage:
    pip install html2text
    python3 scripts/blogger_to_jekyll.py <feed.atom>

Input:  Atom feed from Google Takeout (Takeout/Blogger/Blogs/*/feed.atom)
Output: _posts/YYYY-MM-DD-slug.md  (LIVE posts)
        _drafts/slug.md            (DRAFT posts)
        assets/images/             (extracted base64 images)
"""

import sys
import re
import html
import base64
import uuid
from pathlib import Path
from xml.etree import ElementTree as ET

try:
    import html2text
except ImportError:
    print("Install html2text: pip install html2text")
    sys.exit(1)

NS = {
    "atom": "http://www.w3.org/2005/Atom",
    "blogger": "http://schemas.google.com/blogger/2018",
}

BLOG_URL = "https://rbsomeg.blogspot.com"
IMG_DIR = Path("assets/images")


def slugify(text):
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[-\s]+", "-", text)
    return text.strip("-")


def parse_iso_date(date_str):
    return date_str.replace("T", " ").replace("Z", "+00:00")


def extract_base64_images(html_content, slug):
    images = []
    pattern = r'src="data:image/([^;]+);base64,([^"]+)"'

    def replacer(match):
        ext = match.group(1)
        b64_data = match.group(2)
        img_name = f"{slug}-{len(images) + 1}.{ext}"
        images.append((img_name, b64_data))
        return f'src="{{{{ site.baseurl }}}}/assets/images/{img_name}"'

    new_html = re.sub(pattern, replacer, html_content)
    return new_html, images


def convert_html_to_md(html_content):
    h = html2text.HTML2Text()
    h.body_width = 0
    h.ignore_links = False
    h.ignore_images = False
    h.ignore_emphasis = False
    h.protect_links = True
    h.unicode_snob = True
    h.skip_internal_links = False
    h.escape_snob = True
    return h.handle(html_content)


def main():
    if len(sys.argv) < 2:
        print(f"Usage: python3 {sys.argv[0]} <feed.atom>")
        sys.exit(1)

    xml_path = Path(sys.argv[1])
    if not xml_path.exists():
        print(f"File not found: {xml_path}")
        sys.exit(1)

    posts_dir = Path("_posts")
    drafts_dir = Path("_drafts")
    posts_dir.mkdir(exist_ok=True)
    drafts_dir.mkdir(exist_ok=True)
    IMG_DIR.mkdir(parents=True, exist_ok=True)

    tree = ET.parse(xml_path)
    root = tree.getroot()

    entries = root.findall("atom:entry", NS)
    post_count = 0
    draft_count = 0

    for entry in entries:
        type_el = entry.find("blogger:type", NS)
        status_el = entry.find("blogger:status", NS)
        content_elem = entry.find("atom:content", NS)

        if type_el is None or type_el.text != "POST":
            continue
        if content_elem is None or content_elem.get("type") != "html":
            continue

        title_el = entry.find("atom:title", NS)
        published_el = entry.find("atom:published", NS)

        if title_el is None or published_el is None or title_el.text is None:
            continue

        title_text = html.unescape(title_el.text.strip())
        date_str = parse_iso_date(published_el.text.strip())
        date_part = date_str[:10]
        body_html = content_elem.text or ""

        tags = []
        for cat in entry.findall("atom:category", NS):
            term = cat.get("term", "").strip()
            if term:
                tags.append(term)

        slug = slugify(title_text)

        body_html, images = extract_base64_images(body_html, slug)
        body_md = convert_html_to_md(body_html)
        body_md = body_md.strip()

        # Save extracted images
        for img_name, b64_data in images:
            img_path = IMG_DIR / img_name
            try:
                img_bytes = base64.b64decode(b64_data)
                img_path.write_bytes(img_bytes)
            except Exception as e:
                print(f"  WARN: failed to save {img_name}: {e}")

        front_matter = [
            "---",
            f'layout: post',
            f'title: "{title_text}"',
            f"date: {date_str}",
            f'tags: [{", ".join(tags)}]',
            "---",
            "",
            body_md,
            "",
        ]

        is_live = status_el is not None and status_el.text == "LIVE"

        if is_live:
            filename = f"{date_part}-{slug}.md"
            filepath = posts_dir / filename
            original_link = f"*Originally published on [{BLOG_URL}]({BLOG_URL}/{date_part[:4]}/{date_part[5:7]}/{slug}.html)*"
            front_matter.append(original_link)
            front_matter.append("")
            filepath.write_text("\n".join(front_matter), encoding="utf-8")
            post_count += 1
            print(f"  [{date_part}] {title_text}")
        else:
            filename = f"{slug}.md"
            filepath = drafts_dir / filename
            filepath.write_text("\n".join(front_matter), encoding="utf-8")
            draft_count += 1
            print(f"  [DRAFT] {title_text}")

    print(
        f"\nDone — {post_count} posts + {draft_count} drafts written"
        f" ({len(list(IMG_DIR.iterdir()))} images extracted)"
    )


if __name__ == "__main__":
    main()

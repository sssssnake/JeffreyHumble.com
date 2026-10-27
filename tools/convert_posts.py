"""
One-time conversion: Squarespace WordPress export -> Markdown blog posts.

Usage: python3 tools/convert_posts.py <export.xml> <out_dir>

Each post becomes src/content/blog/<slug>.md with frontmatter. Plain text,
headings, lists, links and images become Markdown; things Markdown can't
express (centred text, large/small text, galleries, video embeds) stay as
small HTML snippets inside the Markdown, which Astro renders as-is.
"""
import html as htmllib
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from bs4 import BeautifulSoup, NavigableString, Tag
from markdownify import MarkdownConverter

sys.path.insert(0, str(Path(__file__).parent))
from sqs_common import cdn_to_local, rewrite_cdn_urls  # noqa: E402

NS = {
    'wp': 'http://wordpress.org/export/1.2/',
    'content': 'http://purl.org/rss/1.0/modules/content/',
    'excerpt': 'http://wordpress.org/export/1.2/excerpt/',
}


class MD(MarkdownConverter):
    def convert_img(self, el, text, parent_tags):
        alt = (el.get('alt') or '').replace('[', '').replace(']', '')
        return f"![{alt}]({el.get('src')})"


def md(node) -> str:
    return MD(heading_style='ATX', bullets='-', strong_em_symbol='*', escape_underscores=False,
              escape_misc=False).convert(str(node)).strip()


def clean_attrs(soup: BeautifulSoup):
    for el in soup.find_all(True):
        cls = el.get('class') or []
        style = re.sub(r'white-space:\s*pre-wrap;?', '', el.get('style') or '').strip()
        keep_cls = []
        if 'sqsrte-large' in cls:
            keep_cls.append('text-large')
        if 'sqsrte-small' in cls:
            keep_cls.append('text-small')
        if 'sqsrte-text-highlight' in cls:
            keep_cls.append('highlight')
        if el.name in ('p', 'h1', 'h2', 'h3', 'h4') and 'text-align:center' in style.replace(' ', ''):
            keep_cls.append('center')
        if el.name == 'span' and 'underline' in style:
            el.name = 'u'
        if el.name == 'span' and 'line-through' in style:
            el.name = 's'
        for a in list(el.attrs):
            if a in ('href', 'src', 'alt', 'title', 'target', 'rel'):
                continue
            del el[a]
        if keep_cls:
            el['class'] = keep_cls
        if el.name == 'a' and el.get('target') == '_blank':
            el['rel'] = 'noopener'


def youtube_from_embedly(src: str):
    q = parse_qs(urlparse(src if src.startswith('http') else 'https:' + src).query)
    inner = (q.get('src') or [''])[0]
    m = re.search(r'youtube\.com/embed/([\w-]+)', inner) or re.search(r'v=([\w-]+)', (q.get('url') or [''])[0])
    return m.group(1) if m else None


def video_html(vid: str) -> str:
    return (f'<div class="video"><iframe src="https://www.youtube-nocookie.com/embed/{vid}" '
            f'title="YouTube video" loading="lazy" allow="accelerometer; clipboard-write; encrypted-media; '
            f'gyroscope; picture-in-picture" allowfullscreen></iframe></div>')


def convert_body(raw: str) -> str:
    soup = BeautifulSoup(rewrite_cdn_urls(raw), 'html.parser')
    for d in soup.select('div.sqs-html-content'):
        d.unwrap()
    # plain <div> wrappers (captions etc.)
    for d in soup.find_all('div'):
        if not d.get('class'):
            d.unwrap()
    for img in soup.find_all('img'):
        img['src'] = img['src'].split('?')[0]
    clean_attrs(soup)

    out = []
    for node in list(soup.children):
        if isinstance(node, NavigableString):
            if node.strip():
                out.append(htmllib.escape(node.strip()))
            continue
        if not isinstance(node, Tag):
            continue
        if node.name == 'iframe':
            vid = youtube_from_embedly(node.get('src', ''))
            out.append(video_html(vid) if vid else str(node))
        elif 'image-gallery-wrapper' in (node.get('class') or []) or node.name == 'div' and node.find('img') and len(node.find_all('img')) > 1:
            imgs = ''.join(f'<img src="{i["src"]}" alt="{htmllib.escape(i.get("alt", ""))}" loading="lazy" />' for i in node.find_all('img'))
            out.append(f'<div class="gallery">{imgs}</div>')
        elif node.get('class') or node.find(class_=True):
            # centred / sized text, highlights: keep as HTML so nothing is lost
            out.append(str(node))
        else:
            out.append(md(node))
    text = '\n\n'.join(x for x in out if x.strip())
    return re.sub(r'\n{3,}', '\n\n', text).strip() + '\n'


def excerpt_text(raw: str) -> str:
    t = BeautifulSoup(raw or '', 'html.parser').get_text(' ', strip=True)
    return re.sub(r'\s+', ' ', t)


def yaml_str(s: str) -> str:
    return json.dumps(s, ensure_ascii=False)


def main(export_path: str, out_dir: str):
    items = ET.parse(export_path).getroot().find('channel').findall('item')
    attachments = {i.findtext('wp:post_id', namespaces=NS): i.findtext('wp:attachment_url', namespaces=NS)
                   for i in items if i.findtext('wp:post_type', namespaces=NS) == 'attachment'}
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    report = []
    for it in items:
        if it.findtext('wp:post_type', namespaces=NS) != 'post':
            continue
        link = it.findtext('link')
        slug = link.rstrip('/').split('/')[-1]
        status = it.findtext('wp:status', namespaces=NS)
        title = htmllib.unescape(it.findtext('title') or '')
        date = it.findtext('wp:post_date_gmt', namespaces=NS) or it.findtext('wp:post_date', namespaces=NS)
        cats = [c.text for c in it.findall('category') if c.get('domain') == 'category' and c.text]
        tags = [c.text for c in it.findall('category') if c.get('domain') == 'post_tag' and c.text]
        thumb_id = next((pm.findtext('wp:meta_value', namespaces=NS) for pm in it.findall('wp:postmeta', NS)
                         if pm.findtext('wp:meta_key', namespaces=NS) == '_thumbnail_id'), None)
        thumb = attachments.get(thumb_id)
        body_raw = it.findtext('content:encoded', namespaces=NS) or ''
        body = convert_body(body_raw)
        excerpt = excerpt_text(it.findtext('excerpt:encoded', namespaces=NS))
        fm = ['---', f'title: {yaml_str(title)}', f'date: {date.replace(" ", "T")}Z']
        if link != f'/blog/{slug}':
            fm.append(f'path: {yaml_str(link)}')  # keeps an unusual old URL working exactly
        if excerpt:
            fm.append(f'excerpt: {yaml_str(excerpt)}')
        if thumb:
            fm.append(f'image: {yaml_str(cdn_to_local(thumb))}')
        if cats:
            fm.append(f'categories: {json.dumps(cats)}')
        if tags:
            fm.append(f'tags: {json.dumps(tags)}')
        if status != 'publish':
            fm.append('draft: true')
        fm.append('---')
        (out / f'{slug}.md').write_text('\n'.join(fm) + '\n\n' + body, encoding='utf-8')
        report.append((status, slug, len(body)))
    for r in sorted(report):
        print(*r)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])

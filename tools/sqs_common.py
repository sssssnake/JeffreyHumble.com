"""Shared helpers for the one-time Squarespace conversion."""
import re
from urllib.parse import unquote, urlparse

CDN_RE = re.compile(r'(?:https?:)?//images\.squarespace-cdn\.com/content/v1/[^\s"\'<>)]+')


def safe_name(name: str) -> str:
    name = unquote(unquote(name)).replace('+', ' ')
    stem, dot, ext = name.rpartition('.')
    if not dot:
        stem, ext = name, ''
    stem = re.sub(r'[^A-Za-z0-9_-]+', '-', stem).strip('-') or 'image'
    ext = re.sub(r'[^A-Za-z0-9]', '', ext).lower()
    return f"{stem}.{ext}" if ext else stem


def cdn_to_local(url: str) -> str:
    """https://images.squarespace-cdn.com/content/v1/<site>/<id>/<file>?x -> /images/<id>/<file>"""
    path = urlparse(url if url.startswith('http') else 'https:' + url).path
    parts = path.split('/')  # ['', 'content', 'v1', site, id, file]
    if len(parts) < 6:
        return url
    return f"/images/{parts[4]}/{safe_name(parts[5])}"


def local_rel_from_download(rel: str) -> str:
    """images/<site>/<id>/<file> (as downloaded) -> <id>/<safe file>"""
    parts = rel.split('/')
    return f"{parts[2]}/{safe_name(parts[3])}"


def rewrite_cdn_urls(html: str) -> str:
    return CDN_RE.sub(lambda m: cdn_to_local(m.group(0)), html)

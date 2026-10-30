"""
One-time conversion: saved Squarespace page HTML -> Astro pages.

Usage: python3 tools/convert_pages.py <pages dir> <src/pages dir> [scaled.json]

Keeps Squarespace's grid layout (every block at the same row/column on mobile
and desktop) and turns each block into plain HTML or one of our components.
The output is meant to be readable and hand-editable afterwards.
"""
import html as htmllib
import json
import re
import sys
from pathlib import Path

from bs4 import BeautifulSoup, Tag

sys.path.insert(0, str(Path(__file__).parent))
from sqs_common import cdn_to_local, rewrite_cdn_urls  # noqa: E402

PAGES = {
    '_root': ('index', 'Home'),
    'about': ('about', None),
    'services': ('services', None),
    'resources': ('resources', None),
    'portfolio': ('portfolio', None),
    'curriculum-vitae': ('curriculum-vitae', None),
    'speaking-requests': ('speaking-requests', None),
    'imprint': ('imprint', None),
    'privacy-policy': ('privacy-policy', None),
    '404': ('404', None),
    'thanks-for-the-coffee': ('thanks-for-the-coffee', None),
}
SITE = re.compile(r'https?://(www\.)?jeffreyhumble\.com(?=/|")')
COLORS = {'black': 'var(--black)', 'white': 'var(--white)', 'accent': 'var(--accent)',
          'lightAccent': 'var(--light-bg)', 'safeLightAccent': 'var(--light-bg)',
          'darkAccent': 'var(--accent)', 'safeDarkAccent': 'var(--accent)'}

warnings: list[str] = []
uses: set[str] = set()


def ind(s: str, n: int) -> str:
    pad = ' ' * n
    return '\n'.join(pad + line if line.strip() else '' for line in s.splitlines())


def attr(s) -> str:
    return htmllib.escape(str(s), quote=True)


# ---------- grid positions ----------

def parse_positions(section: Tag):
    """Read Squarespace's per-block grid CSS. Returns (rows, {block_id: info})."""
    css = '\n'.join(s.get_text() for s in section.select('.fluid-engine style, style')
                    if 'grid-area' in s.get_text() or 'grid-template-rows' in s.get_text())
    m_rows = re.search(r'grid-template-rows:\s*repeat\((\d+),\s*minmax\(24px', css)
    d_rows = re.findall(r'grid-template-rows:\s*repeat\((\d+),\s*minmax\(calc', css)
    scale = re.search(r'--row-height-scaling-factor:\s*([\d.]+)', css)
    rows = {'mobile': int(m_rows.group(1)) if m_rows else 1,
            'desktop': int(d_rows[0]) if d_rows else 1,
            'scale': float(scale.group(1)) if scale else 0.0215}
    pos = {}
    for bid in set(re.findall(r'\.fe-block-([\w-]+)\s*\{\s*grid-area', css)):
        areas = re.findall(r'\.fe-block-%s\s*\{\s*grid-area:\s*([\d/ -]+);\s*z-index:\s*(\d+)' % re.escape(bid), css)
        just = re.findall(r'\.fe-block-%s \.sqs-block \{\s*justify-content:\s*([\w-]+)' % re.escape(bid), css)
        if not areas:
            continue
        mobile, desktop = areas[0], areas[-1]
        va = {'flex-start': 'top', 'center': 'middle', 'flex-end': 'bottom'}
        pos[bid] = {
            'm': mobile[0].replace(' ', ''), 'zm': int(mobile[1]),
            'd': desktop[0].replace(' ', ''), 'z': int(desktop[1]),
            'valignM': va.get(just[0], 'middle') if just else 'middle',
            'valign': va.get(just[-1], 'middle') if just else 'middle',
        }
    return rows, pos


# ---------- content cleaning ----------

def clean_rich(fragment: Tag) -> str:
    soup = BeautifulSoup(rewrite_cdn_urls(str(fragment)), 'html.parser')
    for el in soup.select('.sqsrte-scaled-text-container, .sqsrte-scaled-text'):
        el.unwrap()
    for el in soup.find_all(True):
        cls = el.get('class') or []
        style = (el.get('style') or '').replace(' ', '')
        keep = []
        if 'sqsrte-large' in cls: keep.append('text-large')
        if 'sqsrte-small' in cls: keep.append('text-small')
        if 'sqsrte-text-highlight' in cls: keep.append('highlight')
        if any(c.startswith('sqsrte-text-color--accent') for c in cls): keep.append('accent')
        if any(c.startswith('sqsrte-text-color--white') for c in cls): keep.append('white')
        if any(c.startswith('sqsrte-text-color--black') for c in cls): keep.append('black')
        if 'text-align:center' in style: keep.append('center')
        if 'text-align:right' in style: keep.append('right')
        if el.name == 'span' and 'underline' in style: el.name = 'u'
        if el.name == 'span' and 'line-through' in style: el.name = 's'
        for a in list(el.attrs):
            if a not in ('href', 'src', 'alt', 'title', 'target', 'id'):
                del el[a]
        if keep:
            el['class'] = keep
        if el.name == 'a':
            if el.get('href'):
                el['href'] = SITE.sub('', el['href']) or '/'
            if el.get('target') == '_blank':
                el['rel'] = 'noopener'
        if el.name == 'span' and not el.attrs:
            el.unwrap()
    out = str(soup)
    out = re.sub(r'<p>\s*</p>', '', out)
    # Astro treats { } as code; escape them in text
    return out.replace('{', '&#123;').replace('}', '&#125;').strip()


def text_box_style(block: Tag) -> str:
    st = block.select_one('style#container-styles')
    if not st or 'sqs-background-enabled' not in (block.get('class') or []):
        return ''
    css = st.get_text()
    bg = re.search(r'--tweak-text-block-background-color:\s*hsla\(var\(--(\w+)-hsl\),\s*([\d.]+)\)', css)
    pad = re.search(r'--tweak-text-block-padding:\s*([\d.% ]+);\s*padding', css)
    parts = []
    if bg:
        parts.append(f"background:{COLORS.get(bg.group(1), 'var(--black)')}")
        if bg.group(1) in ('black', 'accent', 'darkAccent', 'safeDarkAccent'):
            parts.append('color:var(--white)')
    if pad:
        parts.append(f'padding:{pad.group(1).strip()}')
    return ';'.join(parts)


# ---------- blocks ----------

def block_text(block, scaled):
    content = block.select_one('.sqs-html-content')
    if not content:
        return None
    inner = clean_rich(content.decode_contents()) if True else ''
    style = text_box_style(block)
    bid = block.get('id', '').replace('block-', '')
    if bid in scaled:
        style = (style + ';' if style else '') + f"--scaled:{scaled[bid]}"
        cls = 'rich text-block scaled'
    else:
        cls = 'rich text-block'
    sty = f' style="{style}"' if style else ''
    return f'<div class="{cls}"{sty}>\n{ind(inner, 2)}\n</div>'


def block_image(block):
    img = block.select_one('img[data-src], img[src]')
    if not img:
        return None
    src = img.get('data-src') or img.get('src')
    local = cdn_to_local(src.split('?')[0])
    alt = img.get('alt', '')
    fit = 'contain' if block.select_one('.content-fit') else 'cover'
    focal = (img.get('data-image-focal-point') or '0.5,0.5').split(',')
    pos = f"{float(focal[0]) * 100:.0f}% {float(focal[1]) * 100:.0f}%"
    w, h = ((img.get('data-image-dimensions') or 'x').split('x') + ['', ''])[:2]
    link = block.select_one('a[href]')
    clip = block.select_one('clipPath path, clippath path')
    uses.add('Img')
    tag = (f'<Img src="{attr(local)}" alt="{attr(alt)}" fit="{fit}"'
           + (f' position="{pos}"' if pos != '50% 50%' else '')
           + (f' width={{{w}}} height={{{h}}}' if w.isdigit() and h.isdigit() else '')
           + (f' clip="{clip["d"]}"' if clip is not None and block.select_one('[data-is-mask-applied="true"]') else '') + ' />')
    if link:
        href = SITE.sub('', link['href']) or '/'
        ext = ' target="_blank" rel="noopener"' if link.get('target') == '_blank' else ''
        tag = f'<a class="img-link" href="{attr(href)}"{ext}>{tag}</a>'
    cap = block.select_one('figcaption, .image-caption')
    if cap and cap.get_text(strip=True):
        tag += f'\n<p class="caption">{clean_rich(cap.decode_contents())}</p>'
    return tag


def block_button(block):
    a = block.select_one('a')
    if not a:
        return None
    cont = block.select_one('.sqs-block-button-container') or block
    align = 'center'
    for c in cont.get('class') or []:
        if c.startswith('sqs-block-button-container--'):
            align = c.split('--')[1]
    size = cont.get('data-button-size', 'medium')
    kind = cont.get('data-button-type', 'primary')
    cls = 'btn' + (f' btn--{size}' if size != 'medium' else '') + (f' btn--{kind}' if kind != 'primary' else '')
    href = SITE.sub('', a.get('href', '#')) or '/'
    ext = ' target="_blank" rel="noopener"' if a.get('target') == '_blank' else ''
    return f'<div class="btn-wrap" style="text-align:{align}"><a class="{cls}" href="{attr(href)}"{ext}>{htmllib.escape(a.get_text(strip=True))}</a></div>'


def block_marquee(block):
    m = block.select_one('.Marquee')
    if not m:
        return None
    items = [htmllib.unescape(i['text']) for i in json.loads(m.get('data-marquee-items') or '[]')]
    uses.add('Marquee')
    props = [f'items={{{json.dumps(items, ensure_ascii=False)}}}',
             f'textStyle="{m.get("data-text-style", "heading-1")}"',
             f'speed={{{m.get("data-animation-speed", "0.5")}}}',
             f'direction="{m.get("data-animation-direction", "left")}"']
    st = block.select_one('style')
    fsv = re.search(r'font-size-value:\s*([\d.]+)', st.get_text()) if st else None
    if fsv:
        props.append(f'size={{{fsv.group(1)}}}')
    wave = m.get('data-wave-intensity')
    path_type = m.get('data-path-type') or ''
    if wave and float(wave) > 0 and 'straight' not in path_type.lower():
        props += [f'wave={{{wave}}}', f'waveFrequency={{{m.get("data-wave-frequency", "4")}}}']
    if m.get('data-link-to'):
        props.append(f'href="{attr(SITE.sub("", m["data-link-to"]))}"')
    return f'<Marquee {" ".join(props)} />'


def block_accordion(block):
    uses.add('Accordion')
    items = []
    for li in block.select('li.accordion-item'):
        title = li.select_one('.accordion-item__title')
        desc = li.select_one('.accordion-item__description')
        items.append({'title': title.get_text(strip=True) if title else '',
                      'html': clean_rich(desc.decode_contents()) if desc else ''})
    large = bool(block.select_one('.accordion-item__title-wrapper.sqsrte-large'))
    return f'<Accordion large={{{str(large).lower()}}} items={{{json.dumps(items, ensure_ascii=False, indent=2)}}} />'


def block_embed(block):
    c = block.select_one('.sqs-embed-container, .embed-block-wrapper') or block
    raw = c.decode_contents()
    if 'cal.com' in raw:
        link = re.search(r'calLink:\s*"([^"]+)"', raw)
        uses.add('CalEmbed')
        return f'<CalEmbed calLink="{link.group(1) if link else ""}" />'
    vid = re.search(r'youtube(?:-nocookie)?\.com(?:%2F|/)embed(?:%2F|/)([\w-]{6,})', raw) or \
        re.search(r'youtube\.com(?:%2F|/)watch(?:%3F|\?)v(?:%3D|=)([\w-]{6,})', raw)
    if vid:
        uses.add('YouTube')
        return f'<YouTube id="{vid.group(1)}" />'
    json_attr = block.get('data-block-json')
    warnings.append(f'unrecognised embed {block.get("id")}')
    return f'<Fragment set:html={{{json.dumps(raw.strip())}}} />'


def block_code(block):
    c = block.select_one('.sqs-code-container')
    raw = c.decode_contents().strip() if c else ''
    raw = re.sub(r'<style class="transform-overrides-vars">\s*</style>', '', raw).strip()
    if not raw:
        return None
    return f'<Fragment set:html={{{json.dumps(rewrite_cdn_urls(raw))}}} />'


def block_social(block):
    uses.add('SocialIcons')
    links = []
    for a in block.select('a[href]'):
        href = a['href']
        icon = 'linkedin' if 'linkedin' in href else 'youtube' if 'youtube' in href else None
        if icon:
            links.append({'label': icon.title(), 'href': href, 'icon': icon})
    return f'<div class="social-block"><SocialIcons links={{{json.dumps(links)}}} /></div>'


def block_form(block, page):
    uses.add('ContactForm')
    fields = []
    for fs in block.select('.form-item, fieldset'):
        pass
    # Field definitions are rendered client-side by Squarespace; these were read from the live page.
    if page in ('speaking-requests', 'resources'):
        fields = [
            {'name': 'name', 'label': 'Name', 'type': 'name', 'required': True},
            {'name': 'email', 'label': 'Email', 'type': 'email', 'required': True},
            {'name': 'message', 'label': 'Message', 'type': 'textarea', 'required': True},
            {'name': 'event_date', 'label': 'Expected date of event', 'type': 'date', 'required': True},
            {'name': 'budget', 'label': 'Expected budget', 'type': 'text', 'required': True},
        ]
        name = 'speaking-request'
    else:
        fields = [
            {'name': 'name', 'label': 'Name', 'type': 'name', 'required': True},
            {'name': 'email', 'label': 'Email', 'type': 'email', 'required': True},
            {'name': 'message', 'label': 'Message', 'type': 'textarea', 'required': True},
        ]
        name = f'{page}-form'
        warnings.append(f'form on {page}: used the standard 3-field form, check it')
    return f'<ContactForm name="{name}" fields={{{json.dumps(fields, indent=2)}}} />'


def convert_block(block: Tag, page: str, scaled):
    kind = block.get('data-sqsp-block')
    if kind == 'text':
        return block_text(block, scaled)
    if kind == 'image':
        return block_image(block)
    if kind == 'button':
        return block_button(block)
    if kind == 'line':
        return '<hr />'
    if kind == 'scrolling':
        return block_marquee(block)
    if kind == 'accordion':
        return block_accordion(block)
    if kind == 'embed':
        return block_embed(block)
    if kind == 'code':
        return block_code(block)
    if kind == 'social-links':
        return block_social(block)
    if kind == 'form':
        return block_form(block, page)
    warnings.append(f'unknown block type {kind} on {page}')
    return None


# ---------- sections ----------

def section_props(sec: Tag):
    styles = json.loads(sec.get('data-current-styles') or '{}')
    theme = sec.get('data-section-theme') or styles.get('sectionTheme') or 'white'
    h = styles.get('sectionHeight', 'section-height--small').replace('section-height--', '')
    height = styles.get('customSectionHeight', 1) if h == 'custom' else h
    props = {'theme': theme, 'height': height}
    bgimg = sec.select_one('.section-background img')
    if bgimg and (bgimg.get('data-src') or bgimg.get('src')):
        props['bg'] = cdn_to_local((bgimg.get('data-src') or bgimg.get('src')).split('?')[0])
        props['overlay'] = styles.get('imageOverlayOpacity', 0)
    vid = sec.select_one('.section-background [data-config-native-video]')
    if vid is not None:
        name = re.search(r'"filename":\s*"([^"]+)"', vid.get('data-config-native-video') or '')
        if name:
            props['bgVideo'] = f'/media/{name.group(1)}'
            warnings.append(f'background video needs the file public/media/{name.group(1)}')
    return props


def testimonials(sec: Tag) -> str:
    ctx = json.loads(sec.select_one('[data-current-context]')['data-current-context'])
    items = []
    for it in ctx.get('userItems', []):
        img = it.get('image') or {}
        src = img.get('assetUrl') if isinstance(img, dict) else None
        items.append({
            'quote': htmllib.unescape(it.get('title', '')).strip(),
            'author': BeautifulSoup(it.get('description', ''), 'html.parser').get_text(' ', strip=True),
            **({'image': cdn_to_local(src)} if src else {}),
        })
    opts = ctx.get('options', {})
    minh = opts.get('minSlideHeight', {}).get('value', 30)
    pad = opts.get('verticalPaddingTop', {}).get('value', 0)
    theme = sec.get('data-section-theme') or 'white'
    uses.add('Testimonials')
    return (f'<Testimonials theme="{theme}" minHeight="{minh}vh" padding="{pad}vmax" '
            f'items={{{json.dumps(items, ensure_ascii=False, indent=2)}}} />')


def convert_page(path: Path, page: str, scaled) -> tuple[str, str, str]:
    soup = BeautifulSoup(path.read_text(encoding='utf-8'), 'lxml')
    title = (soup.title.get_text() if soup.title else '').split(' — ')[0].strip()
    desc_tag = soup.find('meta', attrs={'name': 'description'})
    desc = desc_tag['content'] if desc_tag else ''
    og = soup.find('meta', property='og:image')
    sections_out = []
    for sec in soup.select('main section.page-section'):
        if sec.find_parent('footer'):
            continue
        if 'content-collection' in (sec.get('class') or []):
            sections_out.append('<!--COLLECTION-->')
            continue
        if 'user-items-list-section' in (sec.get('class') or []):
            sections_out.append(testimonials(sec))
            continue
        rows, pos = parse_positions(sec)
        props = section_props(sec)
        blocks_out = []
        for fe in sec.select('.fe-block'):
            bid = next((c.replace('fe-block-', '') for c in fe['class'] if c.startswith('fe-block-')), None)
            block = fe.select_one('.sqs-block')
            if not block or bid not in pos:
                continue
            body = convert_block(block, page, scaled)
            if not body:
                continue
            p = pos[bid]
            extra = ''
            if p['zm'] != p['z']:
                extra += f' zm={{{p["zm"]}}}'
            if p['valignM'] != p['valign']:
                extra += f' valignM="{p["valignM"]}"'
            va = f' valign="{p["valign"]}"' if p['valign'] != 'middle' else ''
            blocks_out.append(f'<Block m="{p["m"]}" d="{p["d"]}" z={{{p["z"]}}}{extra}{va}>\n{ind(body, 2)}\n</Block>')
        if not blocks_out:
            continue
        sp = [f'theme="{props["theme"]}"']
        h = props['height']
        sp.append(f'height={{{h}}}' if isinstance(h, (int, float)) else f'height="{h}"')
        sp.append(f'rows={{{{ mobile: {rows["mobile"]}, desktop: {rows["desktop"]}, scale: {rows["scale"]} }}}}')
        if props.get('bg'):
            sp.append(f'bg="{props["bg"]}"')
            if props.get('overlay'):
                sp.append(f'overlay={{{props["overlay"]}}}')
        if props.get('bgVideo'):
            sp.append(f'bgVideo="{props["bgVideo"]}"')
        sections_out.append(f'<Section {" ".join(sp)}>\n' + '\n\n'.join(ind(b, 2) for b in blocks_out) + '\n</Section>')
    return title, desc, '\n\n'.join(sections_out)


def write_blog_parts(pages_dir: str, out_dir: str, scaled):
    """The blog page's own sections (above and below the post list) become two components."""
    uses.clear()
    _, _, body = convert_page(Path(pages_dir) / 'blog.html', 'blog', scaled)
    before, _, after = body.partition('<!--COLLECTION-->')
    comp_dir = Path(out_dir).parent / 'components'
    for name, part in (('BlogIntro', before), ('BlogOutro', after)):
        imports = ['import Section from "./Section.astro";', 'import Block from "./Block.astro";']
        imports += [f'import {u} from "./{u}.astro";' for u in sorted(uses)]
        (comp_dir / f'{name}.astro').write_text('---\n' + '\n'.join(imports) + '\n---\n' + part.strip() + '\n', encoding='utf-8')
        print(f'{name}.astro', len(part))


def main(pages_dir: str, out_dir: str, scaled_path: str | None = None):
    scaled = json.loads(Path(scaled_path).read_text()) if scaled_path else {}
    out = Path(out_dir)
    write_blog_parts(pages_dir, out_dir, scaled)
    for src, (dst, forced_title) in PAGES.items():
        f = Path(pages_dir) / f'{src}.html'
        if not f.exists():
            warnings.append(f'missing {f}')
            continue
        uses.clear()
        title, desc, body = convert_page(f, src, scaled)
        title = forced_title or title
        imports = ['import BaseLayout from "../layouts/BaseLayout.astro";',
                   'import Section from "../components/Section.astro";',
                   'import Block from "../components/Block.astro";']
        imports += [f'import {u} from "../components/{u}.astro";' for u in sorted(uses)]
        # Astro does not decode entities in attribute strings and escapes them again on output,
        # so these two props take plain text with only the double quote escaped.
        def plain(v):
            return str(v).replace('"', '&quot;')
        layout_props = ([] if title == 'Home' else [f'title="{plain(title)}"']) + ([f'description="{plain(desc)}"'] if desc else [])
        if dst == '404':
            layout_props.append('noindex')
        page = ('---\n' + '\n'.join(imports) + '\n---\n'
                f'<BaseLayout {" ".join(layout_props)}>\n{ind(body, 2)}\n</BaseLayout>\n')
        (out / f'{dst}.astro').write_text(page, encoding='utf-8')
        print(f'{dst}.astro', len(page))
    for w in warnings:
        print('WARN', w)


if __name__ == '__main__':
    main(*sys.argv[1:])

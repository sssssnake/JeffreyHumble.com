"""
One-time: turn the original Squarespace downloads into web-sized copies.

Usage: python3 optimize_images.py <downloaded images dir> <output dir>

Keeps the format (so URLs stay predictable), shrinks anything wider than
2400px, recompresses JPEGs at quality 82, leaves animated GIFs untouched.
The originals stay in the archive folder.
"""
import shutil
import sys
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).parent))
from sqs_common import safe_name  # noqa: E402

MAX_W = 2400
src, dst = Path(sys.argv[1]), Path(sys.argv[2])
before = after = n = 0
for f in sorted(src.rglob('*')):
    if not f.is_file() or '&quot;' in f.name:
        continue
    rel = f.relative_to(src).parts  # (site, id, file)
    if len(rel) != 3:
        continue
    out = dst / rel[1] / safe_name(rel[2])
    out.parent.mkdir(parents=True, exist_ok=True)
    before += f.stat().st_size
    ext = out.suffix.lower()
    try:
        im = Image.open(f)
        animated = getattr(im, 'is_animated', False)
        if ext in ('.jpg', '.jpeg') and not animated:
            im = im.convert('RGB')
            if im.width > MAX_W:
                im = im.resize((MAX_W, round(im.height * MAX_W / im.width)), Image.LANCZOS)
            im.save(out, 'JPEG', quality=82, optimize=True, progressive=True)
        elif ext == '.png' and not animated:
            if im.width > MAX_W:
                im = im.resize((MAX_W, round(im.height * MAX_W / im.width)), Image.LANCZOS)
            im.save(out, 'PNG', optimize=True)
            if out.stat().st_size > f.stat().st_size:
                shutil.copy2(f, out)
        else:
            shutil.copy2(f, out)
    except Exception as e:  # not an image Pillow understands: copy as-is
        print('copied as-is:', f.name, e)
        shutil.copy2(f, out)
    after += out.stat().st_size
    n += 1
print(f'{n} images, {before/1e6:.0f} MB -> {after/1e6:.0f} MB')

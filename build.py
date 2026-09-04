#!/usr/bin/env python3
"""Generate index.html from brand-guide.html plus the site chrome.

brand-guide.html is the guide itself, exported from the Claude artifact that is
its source of truth. It carries no <head> and no navigation, because the
artifact host supplies those. This script wraps it into the standalone page
that GitHub Pages serves.

Never hand-edit index.html. Edit brand-guide.html (or re-export it) and re-run:

    python3 build.py
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent
SRC = ROOT / "brand-guide.html"
OUT = ROOT / "index.html"

FAVICON = (
    "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' "
    "viewBox='0 0 100 100'%3E%3Ctext y='.9em' font-size='90'%3E%F0%9F%A5%82%3C/text%3E%3C/svg%3E"
)

SITENAV_CSS = """<style>
  .sitenav {
    max-width: 1000px; margin: 0 auto; padding: 14px clamp(20px,4vw,60px) 0;
    display: flex; gap: 18px; flex-wrap: wrap; align-items: baseline;
    font-family: Montserrat, Arial, sans-serif; font-size: 11.5px;
    letter-spacing: .07em; text-transform: uppercase; font-weight: 500;
  }
  .sitenav a { color: var(--accent, #7C5F26); text-decoration: none; border-bottom: 1px solid transparent; }
  .sitenav a:hover { border-bottom-color: currentColor; }
  .sitenav span { color: var(--ink-soft, #6F767C); }
</style>"""

SITENAV = (
    '<nav class="sitenav"><span>BOLLE</span>'
    '<span style="color:var(--ink)">Brand guide</span>'
    '<a href="./colour-spec.html">Colour &amp; type specification</a></nav>'
)


def build() -> str:
    src = SRC.read_text(encoding="utf-8")

    # The version on the cover drives the meta descriptions, so they can never
    # drift from the document they describe.
    m = re.search(r"<span>Version <b>([\d.]+)</b></span>", src)
    if not m:
        sys.exit("build: no version found on the cover of brand-guide.html")
    version = m.group(1)

    split = src.find('<div class="wrap">')
    if split == -1:
        sys.exit('build: no <div class="wrap"> found in brand-guide.html')
    head_src, body_src = src[:split].rstrip("\n"), src[split:]

    # <title> and the font links live in the source; lift the title out so the
    # generated <head> keeps a conventional order.
    t = re.search(r"<title>(.*?)</title>", head_src, re.S)
    title = t.group(1).strip() if t else "BOLLE Brand Guide"
    head_src = head_src.replace(t.group(0), "", 1).lstrip("\n") if t else head_src

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="BOLLE Brand Guide v{version}. Download the logos, export the palette, and reference the full brand definition.">
<meta name="robots" content="noindex, nofollow">
<meta property="og:title" content="{title}">
<meta property="og:description" content="BOLLE Brand Guide v{version}. Logos and palette downloadable.">
<meta property="og:type" content="website">
<link rel="icon" href="{FAVICON}">
<style>
  img, svg, video {{ max-width: 100%; height: auto; }}
  table {{ border-spacing: 0; }}
</style>
{head_src}
{SITENAV_CSS}
</head>
<body>
{SITENAV}
{body_src.rstrip()}
</body>
</html>
"""


if __name__ == "__main__":
    html = build()
    with open(OUT, "w", encoding="utf-8", newline="") as fh:
        fh.write(html)
    v = re.search(r"Version <b>([\d.]+)</b>", html).group(1)
    print(f"built {OUT.name} from {SRC.name}: v{v}, {len(html.encode('utf-8'))} bytes")

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

FAVICON = "data:image/png;base64,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"  # bubble icon, white on BOLLE Black (guide section 07)

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
<link rel="icon" type="image/png" href="{FAVICON}">
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


def assert_versions_agree(html: str) -> str:
    """Refuse to write when the 4 version surfaces disagree. See FINDINGS.md, BG-01.

    The guide carries its version in 4 places: the cover meta, the footer line, the
    meta description and the og description. Three of those are derived from the
    cover by this script, so they cannot drift from each other, and that is exactly
    why the drift went unnoticed: every generated surface agreed while the hand
    authored footer sat a version behind for 3 days on a live document. Read all 4
    back out of the finished document and compare them, rather than trusting the
    inputs that produced it.
    """
    # Version numbers are matched as digits and dots with a lookahead, because the
    # meta strings end in a full stop and a greedy [\d.]+ swallows it. The footer is
    # located inside its own element first: the same string appears earlier in the
    # head, so a document wide search silently reads the meta tag twice and reports
    # the footer as agreeing when it does not.
    VER = r"(\d+(?:\.\d+)+)(?=[.\s<])"
    footer = re.search(r"<footer>.*?</footer>", html, re.S)
    if not footer:
        sys.exit("build: no <footer> element found. Refusing to write.")
    found = {
        "cover": re.search(r"<span>Version <b>" + VER + r"</b></span>", html),
        "footer": re.search(r"BOLLE Brand Guide v" + VER, footer.group(0)),
        "meta description": re.search(r'name="description" content="BOLLE Brand Guide v' + VER, html),
        "og:description": re.search(r'og:description" content="BOLLE Brand Guide v' + VER, html),
    }
    missing = [k for k, m in found.items() if not m]
    if missing:
        sys.exit(f"build: no version string found on: {', '.join(missing)}. Refusing to write.")
    values = {k: m.group(1) for k, m in found.items()}
    if len(set(values.values())) != 1:
        lines = "\n".join(f"  {k:<18} v{v}" for k, v in values.items())
        sys.exit(
            "build: the version surfaces disagree, so nothing was written.\n"
            f"{lines}\n"
            "A version bump has to name every surface carrying the number. The footer in\n"
            "brand-guide.html is authored by hand and is the one that drifts."
        )
    return next(iter(values.values()))


if __name__ == "__main__":
    html = build()
    version = assert_versions_agree(html)
    with open(OUT, "w", encoding="utf-8", newline="") as fh:
        fh.write(html)
    print(f"built {OUT.name} from {SRC.name}: v{version}, {len(html.encode('utf-8'))} bytes")
    print("  all 4 version surfaces agree: cover, footer, meta description, og:description")

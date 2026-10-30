#!/usr/bin/env python3
"""Build public/llms-full.txt: the essential docs pages as one plain-Markdown file.

Run from the project root before `astro build` (or let `npm run build` do it):

    python scripts/build_llms_full.py [--header-url https://perms.io/llms-header.md]

With --header-url, the shared header perms.io publishes (summary, when to use Permio, current SDK versions,
pricing) is fetched and put at the top of llms-full.txt, and public/llms.txt is written as that header plus
llms-index.md. The deploy does this; the committed llms-full.txt keeps the plain HEADER below, so `--check`
needs no network.

Pages are taken in sidebar order from astro.config.mjs. MDX is turned into plain Markdown: the
hosts snippet (<Hosts />) is inlined once, asides (:::kind[Title] and <Aside>) and tabs become bold
labels followed by their content, <Endpoint> becomes `METHOD /path`, cards become plain text or
link lists, imports and other markup are dropped, and site-relative links become absolute URLs.
Pass `--check` to fail (exit 1) if the committed file is out of date instead of writing it.
"""

from __future__ import annotations

import argparse
import html
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "src" / "content" / "docs"
SNIPPETS = ROOT / "src" / "snippets"
OUTPUT = ROOT / "public" / "llms-full.txt"
INDEX = ROOT / "llms-index.md"
LLMS = ROOT / "public" / "llms.txt"

# Background material that isn't specific to Permio. It stays in llms.txt under "Optional".
EXCLUDE = {"iam-basics"}

HEADER = """\
# Permio documentation (full text)

> Permio (perms.io) is permissions as a service: resource-level role-based access control (RBAC) behind an API.
> You define permissions and roles, grant them to principals (and groups) on hierarchical resource URIs, and ask
> from your backend whether a principal may do something on a resource. Grants are inherited by every URI beneath
> them. Permio only does authorisation; principals are the user IDs your own login system already uses.

This file is generated from the pages at {site} by `scripts/build_llms_full.py`. Do not edit it by hand.
A page index is at {site}llms.txt.
"""

# Aside labels, matching the MkDocs admonition names the file used before.
ASIDE_LABEL = {"note": "Note", "tip": "Tip", "caution": "Warning", "danger": "Danger"}

FRONTMATTER = re.compile(r"^---\n(?P<yaml>.*?)\n---\n", re.S)
ASIDE_OPEN = re.compile(r"^:::(?P<kind>\w+)(?:\[(?P<title>[^\]]*)\])?\s*$")
ASIDE_TAG = re.compile(r'^<Aside type="(?P<kind>\w+)"(?: title="(?P<title>[^"]*)")?>\s*$')
TAB_ITEM = re.compile(r'^<TabItem label="(?P<label>[^"]*)">\s*$')
ENDPOINT = re.compile(r'^<Endpoint method="(?P<method>\w+)" path="(?P<path>[^"]*)" />\s*$')
CARD = re.compile(r'^\s*<Card title="(?P<title>[^"]*)"[^>]*>\s*$')
LINK_CARD = re.compile(r'^\s*<LinkCard title="(?P<title>[^"]*)" description="(?P<desc>[^"]*)" href="(?P<href>[^"]*)" />\s*$')
DROP = re.compile(r"^\s*(import .* from .*;|</?(Tabs|CardGrid)\b[^>]*>|</(TabItem|Aside)>|:::)\s*$")
FENCE_META = re.compile(r"^(?P<fence>\s*(?:```|~~~)\w*)\s+.*$")
LINK = re.compile(r"(?<!!)\[(?P<text>[^\]]+)\]\((?P<href>[^)\s]+)\)")
FENCE = re.compile(r"^\s*(```|~~~)")


def sidebar_slugs() -> list[str]:
    """Page slugs in sidebar order ('' is the home page)."""
    config = (ROOT / "astro.config.mjs").read_text(encoding="utf-8")
    sidebar = config[config.index("sidebar:") :]
    return [m["slug"] if m["slug"] is not None else m["link"].strip("/")
            for m in re.finditer(r"(?:slug: '(?P<slug>[^']*)'|link: '(?P<link>/[^']*)')", sidebar)]


def source(slug: str) -> Path:
    for candidate in (f"{slug}.mdx", f"{slug}.md", f"{slug}/index.mdx", f"{slug}/index.md"):
        if (DOCS / candidate).exists():
            return DOCS / candidate
    if slug == "":
        return DOCS / "index.mdx"
    raise SystemExit(f"no page for sidebar slug {slug!r}")


def page_url(site: str, slug: str) -> str:
    return site + (slug + "/" if slug else "")


def frontmatter(text: str) -> tuple[dict[str, str], str]:
    """Top-level `key: value` pairs; enough for titles, not a YAML parser."""
    m = FRONTMATTER.match(text)
    if not m:
        return {}, text
    fields = {}
    for line in m["yaml"].split("\n"):
        if fm := re.match(r"^(?P<key>\w+): (?P<value>.+)$", line):
            fields[fm["key"]] = fm["value"].strip().strip("\"'")
    return fields, text[m.end() :]


def snippet_body(name: str) -> list[str]:
    return (SNIPPETS / name).read_text(encoding="utf-8").rstrip("\n").split("\n")


def convert(lines: list[str], seen: set[str]) -> list[str]:
    out: list[str] = []
    in_fence = False
    in_style = False
    for line in lines:
        if FENCE.match(line):
            in_fence = not in_fence
            out.append(FENCE_META.sub(r"\g<fence>", line))  # drop Expressive Code meta such as title="..."
            continue
        if in_fence:
            out.append(line)
            continue
        if line.startswith("<style"):
            in_style = not line.rstrip().endswith("</style>")
            continue
        if in_style:
            in_style = not line.rstrip().endswith("</style>")
            continue

        if line.strip() == "<Hosts />":
            if "hosts" in seen:
                out.append('(See "API host" earlier in this file.)')
            else:
                seen.add("hosts")
                out.extend(convert(snippet_body("hosts.mdx"), seen))
        elif m := (ASIDE_OPEN.match(line) or ASIDE_TAG.match(line)):
            kind = ASIDE_LABEL.get(m["kind"], m["kind"].capitalize())
            out += [f"**{kind}: {m['title']}**" if m["title"] else f"**{kind}**", ""]
        elif m := TAB_ITEM.match(line):
            out += [f"**{m['label']}**", ""]
        elif m := ENDPOINT.match(line):
            out.append(f"`{m['method']} {html.unescape(m['path'])}`")
        elif m := CARD.match(line):
            out += [f"**{m['title']}**", ""]
        elif line.strip() == "</Card>":
            out.append("")
        elif m := LINK_CARD.match(line):
            out.append(f"- [{m['title']}]({m['href']}): {m['desc']}")
        elif re.match(r"^<div\b", line) or DROP.match(line):
            continue
        else:
            # MDX escapes back to plain Markdown, outside inline code.
            parts = re.split(r"(`+[^`]*`+)", line.strip() if line.startswith("\t") else line)
            for n in range(0, len(parts), 2):
                parts[n] = (parts[n].replace("\\{", "{").replace("\\}", "}").replace("&lt;", "<")
                            .replace("<br />", ""))
            out.append("".join(parts))
    return out


def drop_html_blocks(text: str) -> str:
    # Block-level HTML has no plain-Markdown equivalent.
    return re.sub(r"(?ms)^<div\b.*?^</div>\s*\n", "", text)


def render_page(slug: str, site: str, seen: set[str]) -> str:
    fields, body = frontmatter(source(slug).read_text(encoding="utf-8"))
    lines = [f"# {fields['title']}", ""] + convert(drop_html_blocks(body).split("\n"), seen)
    text = "\n".join(lines)

    # Absolute links, outside fenced code.
    parts = re.split(r"(```.*?```)", text, flags=re.S)
    for n in range(0, len(parts), 2):
        parts[n] = LINK.sub(lambda m: f"[{m['text']}]({absolutise(m['href'], slug, site)})", parts[n])
    text = "".join(parts)

    # Shift headings down one level so each page sits under the file's H1.
    shifted, in_fence = [], False
    for line in text.split("\n"):
        if FENCE.match(line):
            in_fence = not in_fence
        if not in_fence and re.match(r"^#{1,5} ", line):
            line = "#" + line
        shifted.append(line)
    text = "\n".join(shifted)

    text = re.sub(r"\n---\n", "\n", text)  # in-page rules; pages are separated below
    return re.sub(r"\n{3,}", "\n\n", text).strip()


def absolutise(href: str, slug: str, site: str) -> str:
    if re.match(r"^[a-z][a-z0-9+.-]*:", href):
        return href  # https:, mailto: ...
    if href.startswith("#"):
        return page_url(site, slug) + href
    return site + href.lstrip("/")


def fetch_header(url: str) -> str:
    with urllib.request.urlopen(url, timeout=30) as res:
        return res.read().decode("utf-8").strip()


def build(shared_header: str | None = None) -> str:
    site = re.search(r"site: '([^']+)'", (ROOT / "astro.config.mjs").read_text(encoding="utf-8"))[1]
    site = site.rstrip("/") + "/"
    header = HEADER.format(site=site).rstrip()
    if shared_header:
        # Keep the "generated from" note; the fetched header replaces the title and summary.
        header = shared_header + "\n\n" + header[header.index("This file is generated"):]
    chunks = [header]
    seen: set[str] = set()
    for slug in sidebar_slugs():
        if slug in EXCLUDE:
            continue
        chunks.append(f"---\n\nSource: {page_url(site, slug)}\n\n{render_page(slug, site, seen)}")
    return "\n\n".join(chunks) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--header-url")
    args = parser.parse_args()

    if args.check:
        content = build()
        current = OUTPUT.read_text(encoding="utf-8") if OUTPUT.exists() else ""
        if current != content:
            print(f"{OUTPUT.relative_to(ROOT)} is out of date; run scripts/build_llms_full.py", file=sys.stderr)
            return 1
        return 0

    shared_header = fetch_header(args.header_url) if args.header_url else None
    content = build(shared_header)
    if shared_header:
        LLMS.write_text(shared_header + "\n\n" + INDEX.read_text(encoding="utf-8"), encoding="utf-8")
        print(f"wrote {LLMS.relative_to(ROOT)}")
    OUTPUT.write_text(content, encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)} ({len(content.encode('utf-8')):,} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

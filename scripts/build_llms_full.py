#!/usr/bin/env python3
"""Build docs/llms-full.txt: the essential docs pages as one plain-Markdown file.

Run from the repository root before `mkdocs build` / `mkdocs gh-deploy`:

    python scripts/build_llms_full.py

Pages are taken in `mkdocs.yml` nav order. MkDocs-specific syntax is turned into plain
Markdown: snippets (`--8<--`) are inlined, admonitions and content tabs become bold labels
followed by their content, raw HTML is dropped and relative links become absolute URLs.
Pass `--check` to fail (exit 1) if the committed file is out of date instead of writing it.
"""

from __future__ import annotations

import posixpath
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
SNIPPETS = ROOT / "snippets"
OUTPUT = DOCS / "llms-full.txt"

# Background material that isn't specific to Permio. It stays in llms.txt under "Optional".
EXCLUDE = {"iam-basics.md"}

HEADER = """\
# Permio documentation (full text)

> Permio (perms.io) is permissions as a service: resource-level role-based access control (RBAC) behind an API.
> You define permissions and roles, grant them to principals (and groups) on hierarchical resource URIs, and ask
> from your backend whether a principal may do something on a resource. Grants are inherited by every URI beneath
> them. Permio only does authorisation; principals are the user IDs your own login system already uses.

This file is generated from the pages at {site} by `scripts/build_llms_full.py`. Do not edit it by hand.
A page index is at {site}llms.txt.
"""

ADMONITION = re.compile(r'^(?P<indent>\s*)(?:!!!|\?\?\?\+?)\s+(?P<kind>[\w-]+)(?:\s+"(?P<title>[^"]*)")?\s*$')
TAB = re.compile(r'^(?P<indent>\s*)===\+?\s+"(?P<title>[^"]*)"\s*$')
SNIPPET = re.compile(r'^(?P<indent>\s*)--8<--\s+"(?P<name>[^"]+)"\s*$')
LINK = re.compile(r"(?<!!)\[(?P<text>[^\]]+)\]\((?P<href>[^)\s]+)\)")
FENCE = re.compile(r"^\s*(```|~~~)")


def load_config() -> dict:
    # mkdocs.yml may use python tags in other projects; this one doesn't, but don't choke on them.
    class Loader(yaml.SafeLoader):
        pass

    Loader.add_multi_constructor("tag:yaml.org,2002:python/", lambda loader, suffix, node: None)
    return yaml.load((ROOT / "mkdocs.yml").read_text(encoding="utf-8"), Loader=Loader)


def nav_pages(nav: list) -> list[tuple[str, str]]:
    """Flatten the nav into (title, path) pairs, in order."""
    pages: list[tuple[str, str]] = []
    for item in nav:
        if isinstance(item, str):
            pages.append((item, item))
            continue
        for title, value in item.items():
            if isinstance(value, list):
                pages.extend(nav_pages(value))
            elif isinstance(value, str) and value.endswith(".md"):
                pages.append((title, value))
    return pages


def page_url(site: str, path: str) -> str:
    """URL of a docs page with MkDocs' default directory URLs."""
    if path == "index.md":
        return site
    if path.endswith("/index.md"):
        return site + path[: -len("index.md")]
    return site + path[: -len(".md")] + "/"


def absolutise(href: str, page: str, site: str) -> str:
    if re.match(r"^[a-z][a-z0-9+.-]*:", href):
        return href  # https:, mailto: ...
    target, _, anchor = href.partition("#")
    if not target:
        url = page_url(site, page)
    else:
        resolved = posixpath.normpath(posixpath.join(posixpath.dirname(page), target))
        url = page_url(site, resolved) if resolved.endswith(".md") else site + resolved
    return url + ("#" + anchor if anchor else "")


def indented_block(lines: list[str], start: int, indent: int) -> tuple[list[str], int]:
    """Collect the body of an admonition or tab: blank lines and lines indented past `indent`."""
    body: list[str] = []
    i = start
    while i < len(lines):
        line = lines[i]
        if line.strip() and len(line) - len(line.lstrip()) <= indent:
            break
        body.append(line)
        i += 1
    while body and not body[-1].strip():
        body.pop()
        i -= 1
    width = indent + 4
    return [line[width:] if line[:width].strip() == "" else line.lstrip() for line in body], i


def convert(lines: list[str]) -> list[str]:
    """Replace admonitions and content tabs with plain Markdown, recursively."""
    out: list[str] = []
    i = 0
    in_fence = False
    while i < len(lines):
        line = lines[i]
        if FENCE.match(line):
            in_fence = not in_fence
        if not in_fence and (m := ADMONITION.match(line) or TAB.match(line)):
            indent = len(m.group("indent"))
            body, i = indented_block(lines, i + 1, indent)
            if "kind" in m.groupdict():
                kind = m.group("kind").capitalize()
                title = m.group("title")
                label = f"{kind}: {title}" if title else kind
            else:
                label = m.group("title")
            pad = m.group("indent")
            out.append(f"{pad}**{label}**")
            out.append("")
            out.extend(pad + b if b.strip() else "" for b in convert(body))
            continue
        out.append(line)
        i += 1
    return out


def inline_snippets(lines: list[str], seen: set[str]) -> list[str]:
    """Inline `--8<--` snippets. A snippet used on several pages is written out in full only once."""
    out: list[str] = []
    for line in lines:
        m = SNIPPET.match(line)
        if m and m.group("name") in seen:
            first = (SNIPPETS / m.group("name")).read_text(encoding="utf-8").split("\n", 1)[0]
            heading = ADMONITION.match(first)
            name = heading.group("title") if heading and heading.group("title") else m.group("name")
            out.append(f'{m.group("indent")}(See "{name}" earlier in this file.)')
        elif m:
            seen.add(m.group("name"))
            snippet = (SNIPPETS / m.group("name")).read_text(encoding="utf-8").rstrip("\n").split("\n")
            out.extend(m.group("indent") + s if s.strip() else "" for s in inline_snippets(snippet, seen))
        else:
            out.append(line)
    return out


def strip_html(text: str) -> str:
    # Drop block-level HTML (the logo on the home page) and inline <br>. Only touches lines that start
    # with a tag, so placeholders such as `group:<slug>` in prose and code are left alone.
    text = re.sub(r"(?ms)^<div\b.*?^</div>\s*\n", "", text)
    return re.sub(r"<br\s*/?>", "", text)


def render_page(path: str, site: str, seen: set[str]) -> str:
    raw = (DOCS / path).read_text(encoding="utf-8")
    lines = convert(inline_snippets(strip_html(raw).split("\n"), seen))
    text = "\n".join(lines)

    # Absolute links, outside fenced code.
    parts = re.split(r"(```.*?```)", text, flags=re.S)
    for n in range(0, len(parts), 2):
        parts[n] = LINK.sub(lambda m: f"[{m.group('text')}]({absolutise(m.group('href'), path, site)})", parts[n])
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


def build() -> str:
    config = load_config()
    site = config["site_url"].rstrip("/") + "/"
    chunks = [HEADER.format(site=site).rstrip()]
    seen: set[str] = set()
    for _title, path in nav_pages(config["nav"]):
        if path in EXCLUDE:
            continue
        chunks.append(f"---\n\nSource: {page_url(site, path)}\n\n{render_page(path, site, seen)}")
    return "\n\n".join(chunks) + "\n"


def main() -> int:
    content = build()
    if "--check" in sys.argv[1:]:
        current = OUTPUT.read_text(encoding="utf-8") if OUTPUT.exists() else ""
        if current != content:
            print(f"{OUTPUT.relative_to(ROOT)} is out of date; run scripts/build_llms_full.py", file=sys.stderr)
            return 1
        return 0
    OUTPUT.write_text(content, encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)} ({len(content.encode('utf-8')):,} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

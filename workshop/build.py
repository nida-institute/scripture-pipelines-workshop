#!/usr/bin/env python3
"""Build workshop.html, a single self-contained page holding README.md and every lesson.

    python3 workshop/build.py            write workshop/workshop.html
    python3 workshop/build.py --check    write nothing; fail if the page is invalid or stale

Lessons are the files named NN-*.md beside this script, in number order. Each is converted with
pandoc. The page shows one lesson at a time, chosen from a navigator on the left; it needs no
JavaScript and makes no external requests.
"""

import html
import re
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "workshop.html"
LESSON_FILE = re.compile(r"^(\d\d)-.+\.md$")
TRACK_TAG = re.compile(r"\[(Both|sp only|Helm only)\]")
TAG_CLASS = {"Both": "both", "sp only": "sp", "Helm only": "helm"}

CSS = """
:root {
  --bg: #fbfaf7; --fg: #1d1d1b; --muted: #6b6a66; --line: #dedbd3; --nav-bg: #f2f0ea;
  --link: #1f5f99; --code-bg: #efece4;
  --both: #2e6b3f; --sp: #7a4a12; --helm: #4a3a8a;
}
@media (prefers-color-scheme: dark) {
  :root {
    --bg: #1b1b1a; --fg: #e8e6e1; --muted: #a09e98; --line: #3a3936; --nav-bg: #232321;
    --link: #8cb8e6; --code-bg: #2b2a27;
    --both: #8fd19e; --sp: #e8b77a; --helm: #b9aaf0;
  }
}
* { box-sizing: border-box; }
html { scroll-padding-top: 1rem; }
body {
  margin: 0; background: var(--bg); color: var(--fg);
  font: 16px/1.55 -apple-system, BlinkMacSystemFont, "Segoe UI", "Helvetica Neue", Arial,
    "Noto Sans", "SBL Greek", "Gentium Plus", "Times New Roman", serif;
}
a { color: var(--link); }
#toc {
  position: fixed; top: 0; left: 0; bottom: 0; width: 17rem; overflow-y: auto;
  padding: 1rem; background: var(--nav-bg); border-right: 1px solid var(--line); font-size: 0.92rem;
}
#toc h1 { font-size: 1rem; margin: 0 0 0.75rem; }
#toc ul { list-style: none; margin: 0; padding: 0; }
#toc > ul > li { margin: 0.35rem 0; }
#toc .num { display: inline-block; min-width: 1.6rem; font-weight: 600; }
#toc details { margin: 0.1rem 0 0 1.6rem; }
#toc summary { cursor: pointer; color: var(--muted); font-size: 0.85rem; }
#toc details ul { margin: 0.25rem 0 0.4rem; }
#toc details li { margin: 0.15rem 0; }
#toc details li.h3 { padding-left: 0.9rem; }
#toc .save { display: block; margin-top: 1.5rem; padding-top: 0.75rem; border-top: 1px solid var(--line); }
#toc .save small { display: block; color: var(--muted); }
main { margin-left: 17rem; padding: 1.5rem 2.5rem 4rem; max-width: 60rem; }
.lesson { display: none; }
.lesson:target, .lesson:has(:target) { display: block; }
body:not(:has(:target)) #readme { display: block; }
table { border-collapse: collapse; margin: 1rem 0; }
th, td { border: 1px solid var(--line); padding: 0.35rem 0.6rem; vertical-align: top; text-align: left; }
code { background: var(--code-bg); padding: 0 0.2rem; border-radius: 3px; }
pre { background: var(--code-bg); padding: 0.75rem; overflow-x: auto; border-radius: 4px; }
pre code { padding: 0; }
blockquote { margin-left: 0; padding-left: 1rem; border-left: 3px solid var(--line); color: var(--muted); }
.tag {
  display: inline-block; font-size: 0.72em; font-weight: 600; padding: 0 0.4em; border-radius: 3px;
  border: 1px solid currentColor; vertical-align: 0.1em; white-space: nowrap;
}
.tag.both { color: var(--both); } .tag.sp { color: var(--sp); } .tag.helm { color: var(--helm); }
@media (max-width: 820px) {
  #toc { position: static; width: auto; border-right: 0; border-bottom: 1px solid var(--line); }
  main { margin-left: 0; padding: 1rem; }
}
""".strip()


class Headings(HTMLParser):
    """Collect the id and text of every h1, h2 and h3 in a fragment."""

    def __init__(self):
        super().__init__()
        self.found = []  # (level, id, text)
        self._open = None

    def handle_starttag(self, tag, attrs):
        if tag in ("h1", "h2", "h3"):
            self._open = [int(tag[1]), dict(attrs).get("id", ""), ""]

    def handle_data(self, data):
        if self._open is not None:
            self._open[2] += data

    def handle_endtag(self, tag):
        if self._open is not None and tag == f"h{self._open[0]}":
            level, ident, text = self._open
            self.found.append((level, ident, " ".join(text.split())))
            self._open = None


def sources():
    """README.md first, then the lessons in number order, as (key, number, path)."""
    found = [(HERE / "README.md", "readme", "")]
    for path in sorted(HERE.iterdir()):
        match = LESSON_FILE.match(path.name)
        if match:
            number = str(int(match.group(1)))
            found.append((path, f"lesson-{number}", number))
    return found


def render(path, key):
    result = subprocess.run(
        ["pandoc", "-f", "gfm", "-t", "html5", "--wrap=none", f"--id-prefix={key}-", str(path)],
        capture_output=True, text=True, encoding="utf-8", check=True,
    )
    return result.stdout


def link_targets(fragment, keys_by_file):
    """Point links to other workshop files at their section of this page."""
    def replace(match):
        target = match.group(1)
        name, _, anchor = target.partition("#")
        if name in keys_by_file:
            key = keys_by_file[name]
            return f'href="#{key}-{anchor}"' if anchor else f'href="#{key}"'
        return match.group(0)
    return re.sub(r'href="([^"#:/][^":]*)"', replace, fragment)


def tag_tracks(fragment):
    return TRACK_TAG.sub(
        lambda m: f'<span class="tag {TAG_CLASS[m.group(1)]}">{html.escape(m.group(1))}</span>',
        fragment,
    )


def short_title(h1_text, number):
    """'Lesson 1 — Getting started: …' becomes 'Getting started'."""
    title = re.sub(r"^Lesson \d+\s*[—-]\s*", "", h1_text)
    return re.split(r"[:—,]", title)[0].strip() if number else "About this workshop"


def build():
    entries = sources()
    keys_by_file = {path.name: key for path, key, _ in entries}
    lessons = []
    for path, key, number in entries:
        fragment = render(path, key)
        parser = Headings()
        parser.feed(fragment)
        h1 = next((text for level, _, text in parser.found if level == 1), path.stem)
        fragment = tag_tracks(link_targets(fragment, keys_by_file))
        sections = [(level, ident, text) for level, ident, text in parser.found if level in (2, 3)]
        lessons.append({
            "key": key, "number": number, "file": path.name, "h1": h1,
            "title": short_title(h1, number), "sections": sections, "body": fragment,
        })
    return page(lessons), lessons


def nav(lessons):
    lines = ['<nav id="toc">', '<h1>Workshop</h1>', '<ul>']
    for lesson in lessons:
        label = lesson["number"] or "·"
        lines.append("<li>")
        lines.append(
            f'  <a href="#{lesson["key"]}"><span class="num">{html.escape(label)}</span>'
            f'{html.escape(lesson["title"])}</a>'
        )
        if lesson["sections"]:
            lines.append("  <details>")
            lines.append("    <summary>Sections</summary>")
            lines.append("    <ul>")
            for level, ident, text in lesson["sections"]:
                lines.append(
                    f'      <li class="h{level}"><a href="#{ident}">{tag_tracks(html.escape(text))}</a></li>'
                )
            lines.append("    </ul>")
            lines.append("  </details>")
        lines.append("</li>")
    lines.append("</ul>")
    lines.append('<a class="save" href="workshop.html" download="workshop.html">'
                 "Save this page to read offline"
                 "<small>One file, with every lesson. It works without an internet connection.</small></a>")
    lines.append("</nav>")
    return "\n".join(lines)


def page(lessons):
    description = ("A workshop on directing AI with Human at the Helm and Scripture Pipelines: "
                   + "; ".join(l["title"] for l in lessons if l["number"]) + ".")
    parts = [
        "<!DOCTYPE html>",
        '<html lang="en">',
        "<head>",
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        "<title>Workshop — directing AI with Human at the Helm and Scripture Pipelines</title>",
        f'<meta name="description" content="{html.escape(description)}">',
        "<style>",
        CSS,
        "</style>",
        "</head>",
        "<body>",
        nav(lessons),
        "<main>",
    ]
    for lesson in lessons:
        parts.append(f'<section class="lesson" id="{lesson["key"]}">')
        parts.append(lesson["body"].rstrip("\n"))
        parts.append("</section>")
    parts += ["</main>", "</body>", "</html>", ""]
    return "\n".join(parts)


def problems(text, lessons):
    """Everything wrong with a built page, as a list of sentences. Empty means valid."""
    found = []
    expected = {path.name for path, _, _ in sources()}
    built = {lesson["file"] for lesson in lessons}
    for name in sorted(expected - built):
        found.append(f"{name} is not in the page")
    ids = set(re.findall(r'\sid="([^"]+)"', text))
    for lesson in lessons:
        if lesson["number"] and not lesson["sections"]:
            found.append(f"{lesson['file']} has no sections in the navigator")
        if lesson["key"] not in ids:
            found.append(f"{lesson['file']} has no section with id {lesson['key']}")
    for target in re.findall(r'href="#([^"]+)"', text):
        if target not in ids:
            found.append(f"a link points at #{target}, which is not in the page")
    loading = re.findall(r'(?:\ssrc="|<link\b|@import|url\()[^>\n]{0,80}', text)
    for item in loading:
        found.append(f"the page loads something from outside itself: {item.strip()}")
    return found


def main():
    check = "--check" in sys.argv[1:]
    text, lessons = build()
    found = problems(text, lessons)
    if check:
        current = OUTPUT.read_text(encoding="utf-8") if OUTPUT.exists() else None
        if current != text:
            found.append(f"{OUTPUT.name} is stale: run python3 workshop/build.py")
    for problem in found:
        print(f"problem: {problem}", file=sys.stderr)
    if found:
        return 1
    if not check:
        OUTPUT.write_text(text, encoding="utf-8")
        print(f"wrote {OUTPUT} — {len(lessons)} documents")
    else:
        print(f"{OUTPUT.name} is valid and current — {len(lessons)} documents")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Build the static site published at https://opensportsprofile.org into _site/.

Layout (matches the URLs the spec references):
    /                          the specification, rendered from SPEC.md
    /v0.1/context.jsonld       the JSON-LD context
    /v0.1/profile.schema.json  the JSON Schema
    /ns                        the osp: vocabulary (https://opensportsprofile.org/ns#)
    /LICENSE.txt, /LICENSE-SPEC.txt

Requires the `markdown` package (pip install markdown).
"""
import html
import re
import shutil
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "_site"

STYLE = """
:root{color-scheme:light dark;--fg:#1d1d1f;--bg:#fff;--mut:#666;--line:#ddd;--code:#f4f4f5}
@media(prefers-color-scheme:dark){:root{--fg:#eaeaea;--bg:#161616;--mut:#9a9a9a;--line:#333;--code:#232323}}
body{margin:0 auto;max-width:56rem;padding:1.5rem 1rem 4rem;font:16px/1.6 system-ui,sans-serif;color:var(--fg);background:var(--bg)}
a{color:inherit}h1,h2,h3,h4{line-height:1.25}h2{margin-top:2.5rem;border-top:1px solid var(--line);padding-top:1.5rem}
code{background:var(--code);padding:.1em .3em;border-radius:3px;font-size:.9em}
pre{background:var(--code);padding:1rem;overflow-x:auto;border-radius:6px}pre code{background:none;padding:0}
table{border-collapse:collapse;display:block;overflow-x:auto}th,td{border:1px solid var(--line);padding:.4rem .6rem;vertical-align:top;text-align:left}
"""


def page(title, body):
    return (
        "<!doctype html>\n<html lang=\"en\"><head><meta charset=\"utf-8\">"
        "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">"
        f"<title>{html.escape(title)}</title><style>{STYLE}</style></head>"
        f"<body>{body}</body></html>\n"
    )


# (term, kind, definition, spec section)
TERMS = [
    ("version", "property", "The version of the Open Sports Profile specification the document conforms to. A string such as \"0.1\".", "4.1"),
    ("fandom", "property", "The list of fan relationships on a person's profile.", "4.2"),
    ("FandomRelationship", "class", "A person's relationship to one specific sports team: current or former fan, with optional seasons and a reason.", "4.3"),
    ("team", "property", "The IRI of the team a relationship is about, by default its Wikidata item. Omitted on a bare team.", "3.2"),
    ("teamName", "property", "A human-readable name for the team, so a profile can be read without resolving the IRI. A display hint.", "4.3"),
    ("sport", "property", "The team's sport as human-readable text. A display hint; required on a bare team.", "3.2"),
    ("sportId", "property", "The IRI of the Wikidata item for the sport, so sports can be compared without matching text.", "3.2"),
    ("relationship", "property", "The kind of relationship: current_fan or former_fan.", "4.4"),
    ("CurrentFan", "individual", "The person supports this team now.", "4.4"),
    ("FormerFan", "individual", "The person used to support this team and no longer does.", "4.4"),
    ("seasons", "property", "A list of season ranges during which the relationship held.", "4.5"),
    ("from", "property", "The first season of a range, as a label such as \"2012\" or \"2011-12\".", "4.5"),
    ("to", "property", "The last season of a range. Not allowed together with ongoing.", "4.5"),
    ("ongoing", "property", "True when the person is a fan now and the range has no end. Only valid on a current fan.", "4.5"),
    ("reason", "property", "Free-text reason for the relationship.", "4.3"),
]


def build_ns(spec_html):
    rows = []
    for term, kind, definition, sec in TERMS:
        m = re.search(r'id="(%s-[^"]*)"' % sec.replace(".", ""), spec_html)
        link = f'<a href="/#{m.group(1)}">Spec §{sec}</a>' if m else f"Spec §{sec}"
        rows.append(
            f'<h3 id="{term}"><code>osp:{term}</code> <small>({kind})</small></h3>'
            f"<p>{html.escape(definition)} {link}</p>"
        )
    body = (
        "<h1>Open Sports Profile vocabulary</h1>"
        "<p>Namespace: <code>https://opensportsprofile.org/ns#</code> (prefix <code>osp</code>)</p>"
        "<p>These are the only terms Open Sports Profile defines itself. Everything else is reused from "
        "Schema.org and IPTC Sport Schema. See the <a href=\"/\">specification</a>.</p>"
        + "".join(rows)
    )
    d = OUT / "ns"
    d.mkdir(parents=True, exist_ok=True)
    (d / "index.html").write_text(page("Open Sports Profile vocabulary", body))


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "v0.1").mkdir(parents=True)

    shutil.copy(ROOT / "context" / "v0.1" / "context.jsonld", OUT / "v0.1" / "context.jsonld")
    shutil.copy(ROOT / "schema" / "v0.1" / "profile.schema.json", OUT / "v0.1" / "profile.schema.json")
    shutil.copy(ROOT / "LICENSE", OUT / "LICENSE.txt")
    shutil.copy(ROOT / "LICENSE-SPEC", OUT / "LICENSE-SPEC.txt")

    md = markdown.Markdown(extensions=["tables", "fenced_code", "toc"])
    spec_html = md.convert((ROOT / "SPEC.md").read_text())
    (OUT / "index.html").write_text(page("Open Sports Profile specification", spec_html))
    build_ns(spec_html)
    print(f"Built {OUT}")


main()

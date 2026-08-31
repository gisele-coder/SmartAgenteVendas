"""Build a static HTML site from the project's Markdown documentation."""

from __future__ import annotations

import re
import shutil
from html import escape
from pathlib import Path
from posixpath import relpath
from urllib.parse import urlsplit

import markdown

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs-html"

CSS = """
:root { color-scheme: light dark; --bg:#0d1117; --fg:#e6edf3; --muted:#8b949e;
  --accent:#58a6ff; --border:#30363d; --code:#161b22; --surface:#161b22; }
@media (prefers-color-scheme: light) { :root { --bg:#fff; --fg:#1f2328; --muted:#59636e;
  --accent:#0969da; --border:#d0d7de; --code:#f6f8fa; --surface:#f6f8fa; } }
* { box-sizing:border-box; }
body { margin:0; background:var(--bg); color:var(--fg); font:16px/1.6 -apple-system,
  BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif; }
.container { max-width:980px; margin:auto; padding:28px 24px 72px; }
.toolbar { position:sticky; top:0; z-index:2; display:flex; flex-wrap:wrap; gap:12px;
  align-items:center; padding:10px 0; border-bottom:1px solid var(--border);
  background:var(--bg); color:var(--muted); font-size:13px; }
.dot { width:10px; height:10px; border-radius:50%; background:#3fb950; }
a { color:var(--accent); text-decoration:none; } a:hover { text-decoration:underline; }
h1,h2,h3,h4 { line-height:1.25; margin:28px 0 16px; }
h1,h2 { border-bottom:1px solid var(--border); padding-bottom:.3em; }
blockquote { margin:0; padding:0 1em; color:var(--muted); border-left:.25em solid var(--border); }
code { padding:.2em .4em; border-radius:6px; background:var(--code); font-size:85%;
  font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace; }
pre { overflow:auto; padding:16px; border-radius:8px; background:var(--code); font-size:85%; }
pre code { padding:0; background:transparent; }
table { width:100%; border-collapse:collapse; margin:16px 0; }
th,td { padding:7px 13px; border:1px solid var(--border); text-align:left; }
th,tr:nth-child(even) { background:var(--surface); }
img { max-width:100%; height:auto; } .index li { margin:6px 0; }
"""

MD_EXTENSIONS = ["fenced_code", "tables", "toc", "sane_lists"]


def output_path(source: Path) -> Path:
    relative = source.relative_to(ROOT)
    if relative == Path("README.md"):
        return OUTPUT / "readme.html"
    if relative.name.lower() == "readme.md":
        return OUTPUT / relative.parent / "index.html"
    return OUTPUT / relative.with_suffix(".html")


def source_for_link(source: Path, href: str) -> Path | None:
    parsed = urlsplit(href)
    if parsed.scheme or parsed.netloc or href.startswith("/"):
        return None
    candidate = (source.parent / parsed.path).resolve()
    try:
        candidate.relative_to(ROOT)
    except ValueError:
        return None
    if candidate.is_dir():
        candidate = candidate / "README.md"
    if candidate.suffix.lower() != ".md" or not candidate.exists():
        return None
    return candidate


def rewrite_links(body: str, source: Path) -> str:
    def replace(match: re.Match[str]) -> str:
        href = match.group(1)
        target = source_for_link(source, href)
        if target is None:
            return match.group(0)
        destination = relpath(
            output_path(target).as_posix(), start=output_path(source).parent.as_posix()
        )
        suffix = urlsplit(href).fragment
        rewritten = destination
        if suffix:
            rewritten += f"#{suffix}"
        return match.group(0).replace(href, rewritten, 1)

    return re.sub(r'href="([^"#]+)(#[^"]*)?"', replace, body)


def render(source: Path) -> str:
    title = (
        source.stem
        if source.stem.lower() != "readme"
        else source.parent.name or "SmartOrder AI"
    )
    body = markdown.markdown(source.read_text(encoding="utf-8"), extensions=MD_EXTENSIONS)
    body = rewrite_links(body, source)
    page_parent = output_path(source).parent.relative_to(OUTPUT).as_posix()
    home_href = relpath("index.html", start=page_parent)
    return (
        '<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        f'<title>{escape(title)} | SmartOrder AI</title><style>{CSS}</style></head><body>'
        '<main class="container"><nav class="toolbar"><span class="dot"></span>'
        f'<span>{escape(source.relative_to(ROOT).as_posix())}</span>'
        f'<span>· <a href="{escape(home_href)}">início</a></span>'
        '</nav>' + body + '</main></body></html>'
    )


def build_index(pages: list[Path]) -> str:
    links = []
    for page in sorted(pages):
        relative = page.relative_to(OUTPUT).as_posix()
        label = relative.removesuffix("/index.html") or "README geral"
        links.append(f'<li><a href="{escape(relative)}">{escape(label)}</a></li>')
    body = '<h1>Documentação HTML</h1><p>Versão estática da documentação do SmartOrder AI.</p>'
    body += '<ul class="index">' + "".join(links) + "</ul>"
    return (
        '<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        '<title>Documentação HTML | SmartOrder AI</title>'
        f'<style>{CSS}</style></head><body><main class="container">'
        '<nav class="toolbar"><span class="dot"></span><span>SmartOrder AI</span></nav>'
        + body + '</main></body></html>'
    )


def main() -> None:
    if OUTPUT.exists():
        shutil.rmtree(OUTPUT)
    OUTPUT.mkdir()
    sources = [ROOT / "README.md", ROOT / "Planejamento.md", ROOT / "CHANGELOG.md"]
    sources.extend(sorted((ROOT / "docs").rglob("*.md")))
    pages = []
    for source in sources:
        destination = output_path(source)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(render(source), encoding="utf-8")
        pages.append(destination)
    (OUTPUT / "index.html").write_text(build_index(pages), encoding="utf-8")
    print(f"Generated {len(pages)} documentation pages in {OUTPUT.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()

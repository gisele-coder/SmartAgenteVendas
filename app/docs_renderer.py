"""Render markdown (.md) files to styled HTML.

Provides:
- DOC_CSS: shared GitHub-like stylesheet
- render_markdown_page(): render an arbitrary markdown file to HTML
- build_docs_index(): list all .md files under a directory as links
- safe_resolve(): prevent path traversal outside an allowed base directory
"""

from html import escape
from pathlib import Path

import markdown as md

DOC_CSS = """
:root {
  color-scheme: light dark;
  --bg: #0d1117;
  --fg: #e6edf3;
  --muted: #8b949e;
  --accent: #58a6ff;
  --border: #30363d;
  --code-bg: #161b22;
  --table-stripe: #161b22;
}
@media (prefers-color-scheme: light) {
  :root {
    --bg: #ffffff;
    --fg: #1f2328;
    --muted: #59636e;
    --accent: #0969da;
    --border: #d0d7de;
    --code-bg: #f6f8fa;
    --table-stripe: #f6f8fa;
  }
}
* { box-sizing: border-box; }
body { margin: 0; padding: 0; background: var(--bg); color: var(--fg);
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
  line-height: 1.6; }
.container { max-width: 920px; margin: 0 auto; padding: 32px 24px 80px; }
h1, h2, h3, h4, h5, h6 { line-height: 1.25; margin-top: 24px; margin-bottom: 16px; }
h1 { font-size: 2em; border-bottom: 1px solid var(--border); padding-bottom: .3em; }
h2 { font-size: 1.5em; border-bottom: 1px solid var(--border); padding-bottom: .3em; }
h3 { font-size: 1.25em; }
a { color: var(--accent); text-decoration: none; }
a:hover { text-decoration: underline; }
hr { border: 0; border-top: 1px solid var(--border); margin: 24px 0; }
blockquote {
  margin: 0; padding: 0 1em; color: var(--muted);
  border-left: .25em solid var(--border);
}
code {
  background: var(--code-bg); padding: .2em .4em; border-radius: 6px; font-size: 85%;
  font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
}
pre {
  background: var(--code-bg); padding: 16px; border-radius: 6px; overflow: auto; font-size: 85%;
}
pre code { background: transparent; padding: 0; }
table { border-collapse: collapse; width: 100%; margin: 16px 0; }
th, td { border: 1px solid var(--border); padding: 6px 13px; text-align: left; }
th { background: var(--table-stripe); }
tr:nth-child(even) { background: var(--table-stripe); }
img { max-width: 100%; height: auto; }
ul, ol { padding-left: 2em; }
.toolbar {
  position: sticky; top: 0; background: var(--bg); border-bottom: 1px solid var(--border);
  padding: 8px 0; font-size: 13px; color: var(--muted); display: flex; gap: 12px;
  align-items: center; z-index: 10;
}
.toolbar .dot { width: 10px; height: 10px; border-radius: 50%; background: #3fb950; }
.docs-index li { margin: 4px 0; }
"""

_MD_EXTENSIONS = [
    "fenced_code",
    "tables",
    "toc",
    "sane_lists",
]


def safe_resolve(base: Path, relative: str) -> Path | None:
    """Resolve a relative path inside `base`. Return None if it escapes `base` or does not exist."""
    if not relative or not relative.startswith("/"):
        return None
    candidate = (base / relative.lstrip("/")).resolve()
    try:
        candidate.relative_to(base.resolve())
    except ValueError:
        return None
    return candidate if candidate.exists() else None


def render_markdown_page(
    text: str,
    *,
    title: str,
    source_label: str,
    index_url: str = "/docs-index",
    extra_nav: list[tuple[str, str]] | None = None,
) -> str:
    """Render markdown text inside the shared HTML shell.

    `source_label` is shown next to the toolbar dot.
    `extra_nav` appends toolbar links (e.g. ["health", "/health"]).
    """
    body = md.markdown(text, extensions=_MD_EXTENSIONS)
    nav = "".join(
        f'<span>· <a href="{escape(url)}">{escape(name)}</a></span>'
        for name, url in (extra_nav or [])
    )
    html = (
        '<!doctype html><html lang="pt-BR"><head>'
        '<meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        f'<title>{escape(title)}</title>'
        f'<style>{DOC_CSS}</style>'
        '</head><body><div class="container">'
        f'<div class="toolbar"><span class="dot"></span>'
        f'<span>{escape(source_label)}</span>'
        f'<span>· <a href="{escape(index_url)}">docs</a></span>'
        f"{nav}"
        "</div>"
        f"{body}"
        "</div></body></html>"
    )
    return html


def build_docs_index(base_docs: Path, *, title: str = "Documentos") -> str:
    """Build an HTML index of all .md files under `base_docs` (relative to project root)."""
    items: list[str] = []
    if base_docs.exists():
        for path in sorted(base_docs.rglob("*.md")):
            rel = path.relative_to(base_docs).as_posix()
            items.append(
                f'<li><a href="/docs{escape(rel)}">{escape(rel)}</a></li>'
            )
    body_list = "<ul>" + "\n".join(items) + "</ul>" if items else "<p>Sem documentos.</p>"
    html = (
        '<!doctype html><html lang="pt-BR"><head>'
        '<meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        f'<title>{escape(title)}</title>'
        f'<style>{DOC_CSS}</style>'
        '</head><body><div class="container">'
        f'<div class="toolbar"><span class="dot"></span>'
        f'<span>{escape(title)}</span></div>'
        f"<h1>{escape(title)}</h1>"
        f'<div class="docs-index">{body_list}</div>'
        "</div></body></html>"
    )
    return html


def markdown_body(markdown_text: str) -> str:
    """Render markdown text to an HTML body (no shell)."""
    return md.markdown(markdown_text, extensions=_MD_EXTENSIONS)

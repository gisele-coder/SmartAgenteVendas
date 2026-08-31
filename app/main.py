import re
from pathlib import Path
from typing import Annotated
from uuid import uuid4

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from langchain_openai import ChatOpenAI

from app.config import settings
from app.docs_renderer import build_docs_index, render_markdown_page, safe_resolve
from app.graph.builder import run_recommendation
from app.llm import get_llm
from app.observability.logging_config import setup_logging
from app.observability.metrics import snapshot
from app.schemas import RecommendationRequest, RecommendationResponse

setup_logging()

app = FastAPI(
    title="SmartOrder AI",
    description="Agente Inteligente de Pedidos e Recomendações",
    version="0.3.0",
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
README_PATH = PROJECT_ROOT / "README.md"
PLANNING_PATH = PROJECT_ROOT / "Planejamento.md"
CHANGELOG_PATH = PROJECT_ROOT / "CHANGELOG.md"
DOCS_DIR = PROJECT_ROOT / "docs"


def _rewrite_relative_links(html: str, source_path: Path) -> str:
    """Rewrite relative .md links in the rendered HTML so they route to /docs/<path>.

    Internal relative links such as `docs/foo.md` (from README.md) or `../plane.md`
    must be rewritten to absolute `/docs/...` paths. Stays conservative: skips
    external URLs, anchors, and non-md hrefs.
    """
    base_dir = source_path.parent

    def repl(match: re.Match) -> str:
        href = match.group(1)
        if (
            not href
            or href.startswith("#")
            or "://" in href
            or not href.endswith(".md")
            or href.startswith("/")
        ):
            return match.group(0)
        resolved = (base_dir / href).resolve()
        try:
            rel = resolved.relative_to(PROJECT_ROOT)
            rel_url = rel.as_posix()
            if rel_url.startswith("docs/"):
                url = f"/docs/{rel_url.removeprefix('docs/')}"
            elif rel == README_PATH.relative_to(PROJECT_ROOT):
                url = "/readme"
            elif rel == PLANNING_PATH.relative_to(PROJECT_ROOT):
                url = "/planejamento"
            elif rel == CHANGELOG_PATH.relative_to(PROJECT_ROOT):
                url = "/changelog"
            else:
                return match.group(0)
            return f'<a href="{url}"{match.group(2)}>'
        except ValueError:
            return match.group(0)

    return re.sub(r'<a href="([^"#]+)"([^>]*)>', repl, html)


def _render_markdown_html(source_path: Path, title: str, source_label: str) -> HTMLResponse:
    if not source_path.exists():
        return HTMLResponse(f"<h1>{source_label} não encontrado</h1>", status_code=404)
    text = source_path.read_text(encoding="utf-8")
    body = render_markdown_page(
        text,
        title=title,
        source_label=source_label,
        index_url="/docs-index",
        extra_nav=[("readme", "/readme"), ("health", "/health"), ("metrics", "/metrics")],
    )
    return HTMLResponse(_rewrite_relative_links(body, source_path))


def get_llm_service():
    return get_llm()


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "smartorder-ai", "model": settings.llm_model}


@app.get("/metrics")
def metrics() -> dict:
    return snapshot()


@app.get("/readme", response_class=HTMLResponse, include_in_schema=False)
def readme() -> HTMLResponse:
    return _render_markdown_html(
        README_PATH,
        title="SmartOrder AI — README",
        source_label="README.md",
    )


@app.get("/planejamento", response_class=HTMLResponse, include_in_schema=False)
def planning() -> HTMLResponse:
    return _render_markdown_html(
        PLANNING_PATH,
        title="Planejamento — SmartOrder AI",
        source_label="Planejamento.md",
    )


@app.get("/changelog", response_class=HTMLResponse, include_in_schema=False)
def changelog() -> HTMLResponse:
    return _render_markdown_html(
        CHANGELOG_PATH,
        title="Changelog — SmartOrder AI",
        source_label="CHANGELOG.md",
    )


@app.get("/docs-index", response_class=HTMLResponse, include_in_schema=False)
def docs_index() -> HTMLResponse:
    return HTMLResponse(build_docs_index(DOCS_DIR, title="Documentos (docs/)"))


@app.get("/docs/{path:path}", response_class=HTMLResponse, include_in_schema=False)
def docs_page(path: str) -> HTMLResponse:
    resolved = safe_resolve(DOCS_DIR, "/" + path)
    if resolved is None or resolved.suffix != ".md":
        raise HTTPException(status_code=404, detail="documento não encontrado")
    rel = resolved.relative_to(DOCS_DIR).as_posix()
    return _render_markdown_html(resolved, title=f"docs/{rel}", source_label=rel)


@app.post("/recomendacoes", response_model=RecommendationResponse)
def recommend(
    request: RecommendationRequest,
    llm: Annotated[ChatOpenAI, Depends(get_llm_service)],
) -> RecommendationResponse:
    request_id = uuid4().hex[:12]
    try:
        output = run_recommendation(
            {
                "request_id": request_id,
                "customer_id": request.customer_id,
                "query": request.query,
                "seed_products": request.seed_products,
            },
            llm=llm,
        )
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail="erro interno do agente") from exc
    return RecommendationResponse(**output)

# Pipeline — Execução local (mesmos passos do CI) — 29/08/2026

**Workflow:** `.github/workflows/ci.yml` (push dispara o CI real no GitHub Actions) · **Pipeline local executado** com os mesmos 3 estágios para captura e análise dos logs pela IA.

---

## Etapa 1 — Lint (ruff)

```text
===== ETAPA 1: LINT =====
All checks passed!
exit=0
```

**Análise da IA:** o linter não encontrou nenhuma violação em 446+ instruções (erros E/F/I/UP/B habilitados, line-length 100, prompts com E501 ignorado de propósito). Zero avisos silenciados com `noqa` no diff principal — o estágio é estável e não flaky por natureza (determinístico). Risco de falha futura: baixo, restrito a novos códigos.

## Etapa 2 — Testes (pytest, com cobertura)

```text
42 passed in ~7s
exit=0
```

**Análise da IA:** suite 100% verde, ~7 s (nenhum teste de rede — FakeLLM injetado via DI; o único teste com rede, `test_llm_smoke`, roda apenas quando `LLM_API_KEY` existe — no CI chega via **secret**, nunca hardcoded). Duração estável entre execuções anteriores (5,8–7 s) → sem flakiness. Cobertura 95% documentada em [`qa/relatorios/`](../../qa/relatorios/relatorio-cobertura-2026-08-29.md).

## Etapa 3 — Build (wheel)

```text
artefato: smartorder_ai-0.1.0-py3-none-any.whl (3.5 KB)
exit=0
```

**Análise da IA:** o wheel buildou com sucesso — valida empacotamento (`packages = ["app"]`), dependências declaradas no `pyproject.toml` e ausência de imports fora do pacote. Artefato pequeno (3,5 KB) porque dados/xlsx ficam fora do pacote (correto: trocáveis pelo ERP real).

## Conclusão

Pipeline **3/3 etapas verdes**. Pontos de atenção registrados pela IA: (1) o CI usa `python-version: 3.12` enquanto o local é 3.14 — risco de divergência de comportamento é baixo (código compatível ≥3.11), monitorado pelo próprio CI; (2) secret `LLM_API_KEY` precisa estar configurada no repositório para o smoke test rodar no CI.

---
origem: sessão de desenvolvimento assistido (opencode)
status: oficial
data: 2026-08-29
fase: 0 — Fundação
---

# Fase 0 — Fundação

> Objetivo: preparar repositório, ambiente, scaffold e a configuração do LLM, com segurança de credenciais desde o primeiro commit.

---

## Prompts utilizados

1. **Solicitação inicial de planejamento:**
   > "Leia os documentos e me ajude a planejar esta ideia de projeto por partes até sua finalização baseado na ideia de um agente de vendas com a base de dados de uma planilha que já está na pasta que é uma ideia que pretendo usar em um cliente posteriormente mas, este projeto precisa atender aos requisitos do trabalho descrito no documento de projeto avaliativo."

2. **Respostas de definição de escopo** (via questionário):
   - Modalidade: **individual** (correção aplicada ao `Planejamento.md`, que mencionava dupla)
   - LLM: inicialmente "modelo local/outro" → alterado para **API key do OpenCode** ("vou usar uma apikey do opencode que tenho, mudei de ideia")
   - Low-code: **N8N Cloud** (trial grátis)
   - Formato: **API local (FastAPI)**

3. **Estado do repositório:**
   > "O git eu já sincronizei com a main"
   (verificado: repo `gisele-coder/SmartAgenteVendas`, 1 commit na `main`; criada branch `develop`)

4. **Fornecimento da chave e solicitação de configuração:**
   > "Foi fornecida uma chave de API do OpenCode para configuração temporária (valor omitido por segurança)."

5. **Aprovação da execução da Parte 0:**
   > "sim"

6. **Solicitação de registro de evidências:**
   > "Preciso que já salvando os prompts de cada fase desenvolvida para comprovação do trabalho antes de prosseguir."
   (gerou esta subpasta `desenvolvimento/` e a regra de processo por fase)

---

## Resultado da interação

### Decisões de arquitetura
- Stack fixada: Python 3.11+, LangGraph, FastAPI, Pydantic v2, pandas+openpyxl, pytest, ruff, GitHub Actions, N8N Cloud
- Plano em 9 partes com rastreabilidade aos 15 critérios do brief (seção 6)
- Fluxo de git: `main` + `develop` + feature branches (conforme seção 5.4 do brief)

### Descoberta e configuração do LLM (evidência de depuração)
1. `GET /v1/models` na gateway OpenCode — lista de 66 modelos retornada com sucesso
2. Primeiro teste (`gpt-5.4-nano`) → **`CreditsError: Insufficient balance`** — conta sem saldo para modelos pagos
3. Teste de modelos gratuitos:
   - `deepseek-v4-flash-free` → indisponível ("Model is unavailable")
   - `mimo-v2.5-free` → **inutilizável** (`content: null`, só reasoning)
   - `nemotron-3.5-lightning-free` → funcional (plano B)
   - `hy3-free` → funcional, conciso → **escolhido como principal**
4. Config final: `LLM_BASE_URL=https://opencode.ai/zen/v1`, `LLM_MODEL=hy3-free`, troca de modelo exclusivamente por variável de ambiente (seção 4.10 do brief)

### Correções durante a execução
- `pip install -e .` falhou: *"Multiple top-level packages discovered in a flat-layout: ['app', 'data']"*
- Correção: `[tool.setuptools] packages = ["app"]` no `pyproject.toml`
- `curl` no PowerShell falhou (alias `Invoke-WebRequest`) → substituído por `curl.exe`

### Segurança aplicada
- `.gitignore` criado **antes** de qualquer commit de código, com `.env` protegido
- `LLM_API_KEY` real apenas no `.env` local (gitignored); `.env.example` com valor vazio
- Recomendação registrada: revogar/trocar a chave após a entrega (ficou exposta em conversa)

### Reorganização
- Planilha movida de `docs/` para `data/`; referências atualizadas em `docs/README.md`, `estrutura_planilha.md` e `sobre_a_planilha.md`

---

## Evidências

| Evidência | Detalhe |
|---|---|
| Commit `191733c` | `chore: organiza documentacao, move base para data/ e adiciona gitignore` (10 files) |
| Commit `ee97ca9` | `feat: configura esqueleto do projeto com fastapi, factory de llm e testes` (10 files) |
| Push | branch `develop` publicada em `origin` |
| Testes | `pytest` → **2 passed** (`test_health`, `test_llm_smoke` — conectividade LLM real) |
| Lint | `ruff check .` → **All checks passed** |
| `.env` | **não versionado** (confirmado via `git status` limpo) |

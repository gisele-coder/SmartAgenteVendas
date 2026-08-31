---
origem: sessão de desenvolvimento assistido (opencode)
status: oficial
data: 2026-08-29
fase: 2 — Núcleo LangGraph
---

# Fase 2 — Núcleo LangGraph

> Objetivo: implementar o fluxo agêntico com state tipado, nodes com responsabilidades claras, paralelização, ramificação condicional, condição de parada e separação entre decisão do LLM e regras determinísticas (brief 4.2).

---

## Prompts utilizados

1. **Aprovação de continuidade:**
   > "ok" — aprovação da execução da Parte 2 conforme plano (`docs/plano-execucao.md`), incluindo a instrução permanente de registrar os prompts de cada fase antes de prosseguir

2. **Instrução de documentação do processo (regra permanente da fase 0):**
   > "Preciso que já salvando os prompts de cada fase desenvolvida para comprovação do trabalho antes de prosseguir."

---

## Resultado da interação

### Arquitetura implementada
- `app/graph/state.py`: `RecommendationState` (TypedDict) com **reducers** `Annotated[list, operator.add]` em `errors` e `audit_events` — necessário porque os nodes paralelos atualizam estado concorrentemente
- `app/graph/builder.py`: grafo com 8 nodes; fan-out `security_check → [get_purchase_history, find_similar_products]` (retorna **lista** no router condicional = paralelização); fan-in implícito em `generate_recommendations`; `block_request` e `finalize_response` como saídas; **DAG sem ciclos** = condição de parada estrutural contra loops infinitos
- `app/graph/nodes.py`: 8 nodes + `_audit()` (base do audit log) + `parse_recommendations` (extração/validação de JSON do LLM contra o catálogo) + `_build_profile` (frequência de compra, categorias favoritas)
- `app/graph/prompts.py`: `SYSTEM_PROMPT` (identidade, objetivo, 6 regras, formato JSON) + `build_user_prompt` (histórico + coocorrência + catálogo)
- LLM injetável via `config["configurable"]["llm"]` → testes com FakeLLM sem custo nem rede
- `docs/prompts/system.md`: prompt de sistema documentado (brief 4.10)

### Bugs encontrados e corrigidos (evidência de depuração real)
1. **Testes vacuos da Parte 1**: asserts sobre listas vazias passavam sem testar nada → descoberto ao integrar o grafo; a coocorrência retornava `[]` para TODOS os clientes
   - **Causa**: a lógica olhava apenas os pedidos do próprio cliente (onde todo item já é dele) — resultado sempre vazio
   - **Correção** (`app/tools/similar.py`): market-basket real — produtos que aparecem em **qualquer pedido da base** que contenha algo do perfil do cliente, excluindo o que ele já comprou; `confidence = coocorrência / pedidos contendo produtos do perfil`
   - Testes reforçados com asserts de não-vazio
2. **Injeção de config no LangGraph**: node com parâmetro `config: dict | None` não recebia a config (warning do LangGraph) → o node chamava a **API real** nos testes (36s) em vez do FakeLLM
   - **Correção**: tipar como `RunnableConfig | None` (`langchain_core.runnables`)
3. **Reasoning consumindo tokens**: `hy3-free` gastou os 800 `max_tokens` só no raciocínio (`content: ""`) → **Refinamento 1 documentado** (`docs/prompts/refinamentos/refinamento-1-max-tokens.md`): `LLM_MAX_TOKENS=3000`

### Validação end-to-end real (modelo hy3-free, sem fallback)
```text
status: success | fallback_used: False | erros: []
- 10014 SUPORTE CONDENSADORA 450MM (conf 0.53)
- 10013 AR CONDICIONADO 9000 BTUS INVERTER (conf 0.31)
- 10012 AR CONDICIONADO 12000 BTUS INVERTER (conf 0.22)
```
O agente reproduziu o padrão semântico proposital da base (climatização: ar-condicionado → suporte), justificando cada item pela coocorrência.

---

## Evidências

| Evidência | Detalhe |
|---|---|
| Testes | `pytest` → **17 passed** (6 novos em `test_graph.py`: sucesso, catálogo, fallback, cliente inexistente, injection bloqueado, auditoria paralela) em ~6s (FakeLLM, sem rede) |
| Lint | `ruff check .` → All checks passed |
| E2E real | 1 chamada real ao `hy3-free` com recomendações coerentes (acima) |
| Branch | `feature/langgraph-core` |
| Refinamento | `docs/prompts/refinamentos/refinamento-1-max-tokens.md` |

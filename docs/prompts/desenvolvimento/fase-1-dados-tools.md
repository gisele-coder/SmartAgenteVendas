---
origem: sessão de desenvolvimento assistido (opencode)
status: oficial
data: 2026-08-29
fase: 1 — Dados + Tools
---

# Fase 1 — Dados + Tools

> Objetivo: transformar a planilha em fonte de dados validada das tools do agente, resolvendo as lacunas documentadas em `estrutura_planilha.md`.

---

## Prompts utilizados

1. **Aprovação de continuidade (contexto da conversa):**
   > "ok" — aprovação da execução da Parte 0 e do plano como um todo, incluindo a Parte 1 (tools `get_customer_orders` + `find_similar_products` com validação Pydantic e tratamento de erros)

2. **Instrução de processo incorporada ao fluxo:**
   > "Preciso que já salvando os prompts de cada fase desenvolvida para comprovação do trabalho antes de prosseguir."
   (aplicada: este arquivo é registrado antes do início da Parte 2)

---

## Resultado da interação

### Confirmação da estrutura da planilha (inspeção programática com pandas)
- Abas: `PEDIDOS` (343×12) e `LEIA_ME` (6×2) — **a aba principal chama-se `PEDIDOS`**, não `Dados`
- Estatísticas confirmadas: 120 pedidos, 12 clientes, 22 produtos, zero nulos, sem coluna de data
- Pedidos por cliente: min 5, max 15, média 10,0
- **`VALOR` = total da linha**: evidência analítica — `VALOR/QTD` resulta sempre em preços unitários terminando em `.9` (ex.: 29,8/2 = 14,9; 399,0/10 = 39,9; 1677,9/21 = 79,9)
- Esquema plano: 1 linha = 1 item; sem duplicatas `PEDIDO+COD_PROD`

### Decisões de implementação
- `loader.py`: carregamento único com `lru_cache`, validação do esquema esperado (12 colunas + aba), erros traduzidos para `RuntimeError` com mensagem clara (base ausente / aba ausente / colunas ausentes)
- `schemas.py`: contratos Pydantic (`OrderItem`, `CustomerOrders`, `SimilarProduct`) — saída estruturada já na camada de dados (seção 4.3 do brief)
- `orders.py`: `get_customer_orders` (rejeita `customer_id` não positivo), `customer_exists` (para o node `validate_input` da Parte 2)
- `similar.py`: coocorrência — produtos que aparecem nos pedidos do cliente e que ele **ainda não comprou**; `confidence = coocorrência / total de pedidos do cliente` (limitado a 1,0)
- Testes com a base real commitada (pequena, determinística) + teste de base ausente com `monkeypatch` + `cache_clear`

### Correção durante a execução
- Ruff `E501` (linha > 100) em `schemas.py` — descrição de campo encurtada; re-run: all checks passed

---

## Evidências

| Evidência | Detalhe |
|---|---|
| Testes | `pytest` → **11 passed** (9 novos em `test_tools.py`) |
| Lint | `ruff check .` → All checks passed |
| Branch | `feature/tool-dados` (fluxo develop → feature, seção 5.4 do brief) |
| Doc atualizado | `docs/estrutura_planilha.md` — lacunas marcadas como resolvidas + seção `## Correções` |

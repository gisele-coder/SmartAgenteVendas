# Execução — `e2e-real-001` (Fase 2)

**Data:** 2026-08-29 · **Fase:** 2 — Núcleo LangGraph · **Tipo:** execução real end-to-end (modelo `hy3-free`, gateway OpenCode)

---

## Contexto

Primeira execução ponta a ponta do grafo LangGraph com o modelo real, após o Refinamento 1 (max_tokens). Cliente 100011, consulta "recomende produtos para a proxima compra".

## Sinais Coletados

- **Audit events do state** (`audit_events` correlacionados pela execução):
  `input_validated → security_ok → similar_retrieved → history_retrieved → recommendation_generated → recommendations_validated → response_completed`
- **Latência total:** ~18 s (modelo gratuito com reasoning; medição via `time.perf_counter`)
- **Fallback:** não acionado (`fallback_used: False`)

## Saída Produzida

```json
{
  "request_id": "e2e-real-001",
  "customer_id": 100011,
  "status": "success",
  "customer_profile": {
    "purchase_frequency": "medium",
    "favorite_categories": ["LAMPADAS", "DISJUNTORES", "CHUVEIROS"],
    "orders_count": 10
  },
  "recommendations": [
    {"cod_prod": 10014, "product": "SUPORTE CONDENSADORA 450MM", "confidence": 0.53},
    {"cod_prod": 10013, "product": "AR CONDICIONADO 9000 BTUS INVERTER", "confidence": 0.31},
    {"cod_prod": 10012, "product": "AR CONDICIONADO 12000 BTUS INVERTER", "confidence": 0.22}
  ],
  "errors": []
}
```

Justificativas geradas pelo LLM citam a coocorrência (ex.: "Produto com maior coocorrência (19) no seu histórico recorrente"). O padrão semântico da base (ar-condicionado → suporte condensadora) foi reproduzido corretamente.

## Execução Anterior (motivou o Refinamento 1)

Antes do ajuste de `max_tokens`, a mesma consulta retornava `content: ""` do modelo (800 tokens 100% consumidos pelo reasoning) → `fallback_used: True` com recomendações determinísticas. Detalhes em [`../../prompts/refinamentos/refinamento-1-max-tokens.md`](../../prompts/refinamentos/refinamento-1-max-tokens.md).

## Conclusão da Análise

- Fluxo funcional de ponta a ponta com LLM real: entrada validada → paralelização → LLM → validação → JSON estruturado
- Latência ~18 s: aceitável para o domínio (recomendação assíncrona), mas será registrada como métrica na Parte 5 (observabilidade)
- O fallback demonstrou resiliência real em execução anterior (degradação graciosa)

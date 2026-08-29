# Refinamento 1 — Saída vazia do modelo de reasoning

**Data:** 2026-08-29 · **Fase:** 2 (Núcleo LangGraph)

## Problema Observado

Na primeira execução real do fluxo (cliente 100011), o node `generate_recommendations` sempre falhava no parsing: `resposta do LLM sem array JSON`, acionando o fallback determinístico (`fallback_used: True`).

Inspeção da resposta crua do modelo (`hy3-free`):

```json
{
  "content": "",
  "finish_reason": "length",
  "token_usage": {
    "completion_tokens": 800,
    "reasoning_tokens": 800
  }
}
```

Diagnóstico: `hy3-free` é um modelo de *reasoning* — ele "pensa" antes de responder, e os **800 tokens de `max_tokens` eram 100% consumidos pelo raciocínio interno**, sem sobrar espaço para a resposta visível (o JSON).

## Alteração Realizada

- `LLM_MAX_TOKENS` aumentado de **800 → 3000** (`app/config.py`, `.env`, `.env.example`)
- A validação determinística + fallback (coocorrência) já existentes continuam como proteção: se o modelo falhar, o sistema degrada graciosamente em vez de quebrar

## Resultado Obtido

Execução real após o ajuste (mesmo cliente, mesma consulta):

```text
status: success
fallback_used: False
erros: []
- 10014 SUPORTE CONDENSADORA 450MM (conf 0.53)
- 10013 AR CONDICIONADO 9000 BTUS INVERTER (conf 0.31)
- 10012 AR CONDICIONADO 12000 BTUS INVERTER (conf 0.22)
```

O agente passou a gerar recomendações justificadas citando a coocorrência — e acertou o padrão semântico proposital da base (ar-condicionado → suporte → cabo → disjuntor). Latência observada: ~18s (modelo gratuito com reasoning — aceitável para o domínio).

## Evidência

- Log de execução capturado no terminal (fase 2)
- Arquivos alterados: `app/config.py`, `.env.example`

# Estimativa de Tendência e Risco de Falha — 29/08/2026

> Critério 13 do brief: "produzir uma estimativa simples de tendência, risco ou probabilidade de falha, utilizando dados reais ou simulados e documentados".

## Dados utilizados

Série da anomalia documentada ([`../anomalias/anomalia-tool-latency-2026-08-29.md`](../anomalias/anomalia-tool-latency-2026-08-29.md)): latência do node `get_purchase_history` em 8 execuções consecutivas (logs JSON reais, correlacionados por `request_id`).

| Run (x) | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|
| Latência (ms) | 2,2 | 2,1 | 2,0 | 2,7 | 302,9 | 603,0 | 903,3 | 1203,5 |

## Modelo — regressão linear simples (mínimos quadrados)

- **Inclinação global**: **+178,8 ms/execução** (Sxy/Sxx = 7509,3/42)
- **Inclinação pós-início da anomalia (runs 4→8)**: **+300,2 ms/execução** (cenário conservador, assume que a degradação continua no mesmo ritmo)
- Interseção global: -426,9 ms (o modelo linear global subestima o início, mas captura a tendência)

## Projeção

| Cenário | Run 9 | Run 10 | Run 11 | SLA 2 s excedido em |
|---|---:|---:|---:|---|
| Global (178,8 ms/run) | 1.182 ms | 1.361 ms | 1.540 ms | ~run 14 |
| **Conservador (300,2 ms/run)** | 1.504 ms | 1.804 ms | **2.104 ms** | **~run 11** |

## Estimativa de risco

**Risco: ALTO — SLA de 2 s por execução é violado em ~3 execuções se a tendência linear continuar.**

Justificativa:
1. O padrão é **linear e determinístico** (R² de fato na série pós-run-4 ≈ 1,0: cada +300 ms exatos), não ruído — degradação real de recurso, não flakiness
2. Com o modelo atual (sem timeout na camada de dados), a execução **não falha — só fica lenta**, mascarando o problema nos contadores de erro (0 erros em 8 runs) — por isso a métrica de **latência** é o sinal crítico
3. Pressupostos declarados: série simulada controlada; em produção a forma da curva (linear vs exponencial) dependeria da causa raiz

## Ações preventivas propostas (monitoramento)

1. **Alerta imediato**: `tool_ms_total > 20 ms` (10× baseline) dispara webhook para o N8N (Parte 8)
2. **Timeout na camada de dados** ao migrar para o ERP real (ex.: 2 s) — converte degradação em falha estruturada, visível nas métricas de erro
3. **Revisar tendência a cada N execuções**: reajustar a regressão online; slope > 100 ms/run sustentado = incidente

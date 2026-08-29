# Anomalia — Degradação linear de latência na tool — 29/08/2026

## Sintoma

Série de 8 execuções (`anom-001` a `anom-008`) mostra latência do node `get_purchase_history` saltando do baseline (~2 ms) e crescendo **linearmente ~300 ms por execução** a partir da 5ª:

| Execução | Latência get_purchase_history | Latência find_similar_products |
|---|---:|---:|
| anom-001 | 2,2 ms | 7,3 ms |
| anom-002 | 2,1 ms | 7,2 ms |
| anom-003 | 2,0 ms | 6,9 ms |
| anom-004 | 2,7 ms | 10,0 ms |
| **anom-005** | **302,9 ms** ⚠ | 307,4 ms |
| **anom-006** | **603,0 ms** ⚠ | 607,0 ms |
| **anom-007** | **903,3 ms** ⚠ | 907,1 ms |
| **anom-008** | **1203,5 ms** ⚠ | 1207,3 ms |

Ambas as tools paralelas degradam **juntas** e na mesma proporção → o gargalo está na camada de acesso a dados comum a ambas (`load_orders`).

## Evidência bruta

- Logs JSON: `logs/execution.log` (1 linha por node, correlacionados por `request_id`)
- Métricas: `/metrics` → `tool_ms_max: 2410.8` (soma das duas tools no pico), `tool_ms_avg: 760.2` puxado para cima pelas execuções degradadas
- Audit: eventos `history_retrieved` presentes em todas as execuções (a tool **não falhou** — só ficou lenta)

## Análise da IA

- **Detecção**: primeira execução com latência > 10× o baseline = `anom-005` (302,9 ms vs 2,7 ms) — violação imediata do limite 10×
- **Padrão**: degradação **linear determinística** (+300,1 ms/execução), não aleatória → exclui flakiness de rede; indica causa sistemática e crescente
- **Correlação**: ambos os nodes de tool degradam juntos; LLM e security_check permanecem <1 ms → causa isolada na camada de dados

## Causa provável (real: simulada e declarada)

Nesta série a causa foi **injeção controlada** via `settings.tool_delay_ms` (0 → 300 → 600 → 900 → 1200 ms), simulando degradação progressiva do ERP/aramazenamento. **Em produção, este padrão indicaria**: disco em saturação, lock de leitura concorrente no Excel ou degradação do WebService do ERP — a substituição do xlsx pelo ERP real herdaria este monitoramento sem mudar o agente.

## Ação corretiva

1. Alerta automático no N8N quando `tool_ms` de uma execução > 10× baseline (Parte 8 conecta este sinal)
2. Recomendações: timeout na camada de acesso a dados quando migrada para ERP real + cache com TTL (o `lru_cache` atual já mitiga repetições no mesmo processo)
3. Risco estimado documentado em [`../metricas/tendencia-risco-2026-08-29.md`](../metricas/tendencia-risco-2026-08-29.md)

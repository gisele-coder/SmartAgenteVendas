---
origem: convenção definida pelo brief do projeto (seção 5.4)
status: placeholder
data: 2026-08-27
finalidade: concentrar artefatos comprobatórios de execução (logs, traces, métricas, screenshots)
relacionado: [../README.md](../README.md)
---

# Evidências

Esta pasta concentra **artefatos comprobatórios de execução** do projeto, conforme exigido pelo brief (seções 4.6, 4.7, 4.8) e pela convenção de organização do `docs/` (seção 5.4).

---

## Finalidade

- Armazenar **logs estruturados**, traces, métricas e registros de auditoria
- Servir como insumo para análise de **anomalias, latência e taxa de erro**
- Sustentar a **estimativa de tendência ou risco de falha** (critério #13 do brief)
- Disponibilizar **evidências objetivas** para reconstrução de execuções (critério #11)

---

## Estrutura Sugerida

| Arquivo / Pasta | Conteúdo |
|---|---|
| `README.md` | Este arquivo — visão geral da pasta |
| `execucoes/` | Logs e traces de execuções representativas da aplicação |
| `pipeline/` | Evidências do pipeline de CI (lint, testes, build) |
| `anomalias/` | Anomalias detectadas e suas análises |
| `metricas/` | Séries de métricas, tendências e estimativas de risco |
| `screenshots/` | Capturas de tela da aplicação, dashboards, fluxos low-code |
| `seguranca/` | Evidências de cenários adversariais e bloqueios |

---

## Índice de Evidências Arquivadas

| Data | Evidência | Fase | Arquivo |
|---|---|---|---|
| 29/08 | Execução real E2E do grafo (`e2e-real-001`) — cliente 100011, padrão climatização | 2 | [`execucoes/e2e-real-001-fase-2.md`](./execucoes/e2e-real-001-fase-2.md) |
| 29/08 | Smoke test HTTP da API (`668b104164e6`) — uvicorn + curl, LLM real | 3 | [`execucoes/api-668b104164e6-fase-3.md`](./execucoes/api-668b104164e6-fase-3.md) |
| 29/08 | Cenários adversariais (injection + ação destrutiva) bloqueados via HTTP com audit correlacionado | 4 | [`seguranca/adversarial-fase-4.md`](./seguranca/adversarial-fase-4.md) |
| 29/08 | 3 execuções com logs JSON + métricas + audit correlacionados (`/metrics` capturado) | 5 | [`execucoes/observabilidade-fase-5.md`](./execucoes/observabilidade-fase-5.md) |
| 29/08 | Pipeline 3/3 etapas com análise da IA de cada estágio | 7 | [`pipeline/pipeline-local-2026-08-29.md`](./pipeline/pipeline-local-2026-08-29.md) |
| 29/08 | Anomalia linear de latência da tool (detecção run 5, causa isolada) | 7 | [`anomalias/anomalia-tool-latency-2026-08-29.md`](./anomalias/anomalia-tool-latency-2026-08-29.md) |
| 29/08 | Estimativa de tendência (regressão) e risco de falha (SLA) | 7 | [`metricas/tendencia-risco-2026-08-29.md`](./metricas/tendencia-risco-2026-08-29.md) |
| 31/08 | E2E Flowise + Discord (Parte 8) — injection → `flowise_notify` → Agentflow V2 (`poolside/laguna-s-2.1`) → webhook Discord HTTP 204, todos os sinais correlacionados por `request_id` | 8 | [`execucoes/flowise-discord-e2e-fase-8.md`](./execucoes/flowise-discord-e2e-fase-8.md) |

---

## Quando Popular

Esta pasta deve começar a ser preenchida assim que:

1. Houver **logs estruturados** sendo emitidos pela aplicação
2. Pelo menos uma **execução completa** for registrada com sinais correlacionáveis
3. Uma **anomalia real ou simulada** for detectada e documentada
4. O **pipeline de CI** começar a gerar artefatos verificáveis
5. Um **cenário adversarial** for executado e bloqueado (seção 4.5)

---

## Modelo de Análise de Execução

Cada entrada em `execucoes/` pode seguir este padrão:

```markdown
# Execução — <request_id>

## Sinais Coletados
- **Logs estruturados:** <caminho ou anexo>
- **Métricas:** <caminho ou anexo>
- **Trace:** <caminho ou anexo>

## Fluxo Percorrido
1. <node 1>
2. <node 2>
...

## Decisões Relevantes
- <decisão X no node Y>

## Erros e Latência
- <erro ou gargalo observado>

## Conclusão da Análise
- <o que foi aprendido, ação corretiva, se houver>
```

---

## Modelo de Análise de Anomalia

Cada entrada em `anomalias/` pode seguir este padrão:

```markdown
# Anomalia — <data ou referência>

## Sintoma
- <descrição do comportamento anômalo>

## Evidência Bruta
- <logs, métricas, screenshots>

## Análise da IA
- <interpretação automatizada dos sinais>

## Causa Provável
- <hipótese fundamentada>

## Ação Corretiva
- <o que foi feito>
- <resultado após correção>
```

---

## Boas Práticas

- **Nunca** versionar segredos, tokens ou dados sensíveis em logs
- **Sempre** usar `request_id` para correlacionar sinais de uma mesma execução
- **Versionar** os artefatos no Git sempre que representarem uma análise fechada
- **Limitar tamanho** dos arquivos — preferir amostras representativas a logs completos

---

## Referências

- Brief: [`../Projeto_Avaliativo_modulo_2.md`](../Projeto_Avaliativo_modulo_2.md) — seções 4.6, 4.7, 4.8 e 6.5
- Correlação com QA: [`../qa/`](../qa/README.md)
- Índice geral: [`../README.md`](../README.md)

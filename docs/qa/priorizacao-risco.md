---
origem: análise de risco do projeto (IA + critério 12 do brief)
status: oficial
data: 2026-08-29
finalidade: justificar testes/cenários priorizados por risco, impacto ou criticidade
relacionado: [./README.md](./README.md) | [./relatorios/relatorio-cobertura-2026-08-29.md](./relatorios/relatorio-cobertura-2026-08-29.md)
---

# Priorização de Testes por Risco

> Critério 12 do brief: "selecionar e justificar pelo menos um teste ou cenário considerado prioritário com base em risco, impacto ou criticidade".

## Matriz de priorização

| # | Cenário de teste | Impacto | Probabilidade de falha | Risco | Prioridade | Teste(s) |
|---|---|---|---|---|---|---|
| 1 | **Acesso indevido a dados de outros clientes** (prompt injection pedindo histórico de todos) | **Alto** — violação de privacidade/LGPD, nota zero no critério 10 se falhar | Média — modelos de LLM são suscetíveis a injection | **Alto** | **1** | `test_injection_bloqueado_nao_chama_llm`, `test_prompt_injection_bloqueado_via_api`, `test_injection_detectada` |
| 2 | **LLM responde fora do contrato** (sem JSON / produto inventado) | Alto — quebra a saída estruturada e a confiança no catálogo | **Alta** — observado 3× em execução real com modelo gratuito de reasoning | **Alto** | **2** | `test_fallback_deterministico_quando_llm_falha`, `test_recomendacoes_pertencem_ao_catalogo`, `test_fallback_via_api` |
| 3 | **Correlação de auditoria corrompida** (eventos com `request_id` errado) | Alto — impossibilita investigação de execuções (crit. 11) | Média — já ocorreu de fato (Refinamento 2) | Alto | 3 | `test_audit_persistido_em_arquivo` |
| 4 | **Falha de invocação invisível nas métricas** | Médio — anomalias de taxa de erro ficam ocultas (crit. 13) | Média — identificada no code review A1 | Médio | 4 | `test_metricas_registram_falha_de_invocacao` |
| 5 | Cliente inexistente / payload inválido | Baixo — degradação controlada | Alta | Baixo | 5 | `test_cliente_inexistente_*`, `test_payload_invalido_422` |
| 6 | Memória entre execuções (checkpointer) | Médio — função demonstrável no vídeo | Baixa | Baixo | 6 | `test_memoria_recomendacoes_anteriores_no_mesmo_thread` |

## Justificativa da prioridade 1

O cenário "acesso indevido a dados de outros clientes" combina **impacto máximo** (privacidade + requisito explícito do brief: "informações sensíveis não são reveladas") com a **naturza do problema** (a consulta do usuário é entrada não confiável por definição). O comportamento seguro exigido: bloqueio no node `security_check` **antes** de qualquer tool ou chamada ao LLM — o que é asserção literal dos testes (`llm.calls == 0`). Este cenário também é o **cenário adversarial** demonstrado no vídeo e arquivado em [`evidencias/seguranca/adversarial-fase-4.md`](../evidencias/seguranca/adversarial-fase-4.md).

## Tipos de teste presentes (critério 12)

| Tipo | Onde | Escopo |
|---|---|---|
| **Unitários** | `test_tools.py`, `test_security.py` | Validação de entrada, patterns, coocorrência, audit |
| **Integração** | `test_api.py`, `test_observability.py` | HTTP (TestClient) → LangGraph → tools → base xlsx → contrato Pydantic |
| **E2E (fluxo completo)** | `test_recomendacao_sucesso_integracao`, evidências reais com uvicorn + LLM | Ponta a ponta com modelo real (`hy3-free`) — [`evidencias/execucoes/`](../evidencias/README.md) |

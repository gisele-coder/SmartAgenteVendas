# Relatório de Cobertura — 29/08/2026

**Suite:** 42 testes · **Ferramenta:** pytest-cov · **Branch:** `feature/qa-inteligente` (após correção A1 do code review)

## Sumário

| Métrica | Valor |
|---|---|
| **Cobertura total** | **95%** (451 stmts, 24 misses) |
| Módulos com 100% | 14 (config, builder, metrics, audit, guard, orders, schemas, state, llm, prompts...) |
| Menor cobertura | `observability/logging_config.py` 82% |

## Detalhamento

```
Name                                  Stmts   Miss  Cover
---------------------------------------------------------
app\__init__.py                           0      0   100%
app\config.py                            15      0   100%
app\graph\builder.py                     54      0   100%   ← +branch de exceção (A1)
app\graph\nodes.py                      137      9    93%
app\graph\prompts.py                      6      0   100%
app\graph\state.py                        3      0   100%
app\llm.py                                4      0   100%
app\main.py                              28      3    89%
app\observability\logging_config.py      40      7    82%
app\observability\metrics.py             37      0   100%
app\schemas.py                           14      0   100%
app\security\audit.py                    12      0   100%
app\security\guard.py                    16      0   100%
app\tools\loader.py                      23      3    87%
app\tools\orders.py                      21      0   100%
app\tools\schemas.py                     19      0   100%
app\tools\similar.py                     22      2    91%
---------------------------------------------------------
TOTAL                                   451     24    95%
```

## Lacunas conhecidas (aceitas, com justificativa)

| Módulo | Linhas não cobertas | Justificativa |
|---|---|---|
| `logging_config.py` (82%) | Setup de FileHandler/StreamHandler | Exige ambiente de execução real (uvicorn); validado manualmente na evidência da fase 5 |
| `nodes.py` (93%) | Ramificações de erro extremas (ex.: `history` vazio + `similar` vazio) | Caminho de fallback vazio coberto indiretamente; baixo risco |
| `main.py` (89%) | Handler de exceção 500 | Requer falha interna simulada no endpoint; comportamento do grafo já coberto |
| `loader.py` (87%) | Branches de `FileNotFoundError`/`ValueError` | Coberto por `test_base_ausente_erro_claro` (FileNotFound); aba ausente aceita |

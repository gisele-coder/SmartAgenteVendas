---
origem: convenção definida pelo brief do projeto (seção 5.4)
status: placeholder
data: 2026-08-27
finalidade: concentrar evidências de QA — code review, testes e priorização por risco
relacionado: [../README.md](../README.md)
---

# QA — Quality Assurance

Esta pasta concentra as **evidências de QA** do projeto, conforme exigido pelo brief (seção 4.7) e pela convenção de organização do `docs/` (seção 5.4).

---

## Finalidade

- Registrar **code reviews** realizados com apoio de IA
- Documentar **suites de teste** (unitário, integração, aceitação, E2E)
- Justificar a **priorização por risco, impacto ou criticidade** dos testes
- Servir como evidência objetiva para o critério de avaliação **#12** (seção 6.6 do brief)

---

## Status atual

- ✅ **Code review com IA de diff real**: [`code-reviews/review-07fbd7f-observabilidade.md`](./code-reviews/review-07fbd7f-observabilidade.md) — achado A1 corrigido (falhas de invocação agora contam nas métricas)
- ✅ **Cobertura**: [`relatorios/relatorio-cobertura-2026-08-29.md`](./relatorios/relatorio-cobertura-2026-08-29.md) — 95% total, 42 testes
- ✅ **Priorização por risco**: [`priorizacao-risco.md`](./priorizacao-risco.md) — matriz com 6 cenários; prioridade 1 = acesso indevido a dados de outros clientes
- ✅ **Tipos de teste**: unitários + integração (HTTP→grafo→tools→base) + E2E real com LLM

## Estrutura

| Arquivo / Pasta | Conteúdo |
|---|---|
| `README.md` | Este arquivo — visão geral da pasta |
| `code-reviews/` | Relatórios de revisão de código com IA (diffs analisados, problemas encontrados, sugestões) |
| `relatorios/` | Sumários de qualidade, cobertura e resultados |
| `priorizacao-risco.md` | Justificativa do(s) teste(s) priorizado(s) por risco, impacto ou criticidade |

---

## Quando Popular

✅ Populada na Parte 6 (29/08): PR real analisado com IA, testes de integração/E2E consolidados, priorização por risco documentada e relatório de cobertura arquivado.

---

## Modelo de Code Review

Cada entrada em `code-reviews/` pode seguir este padrão:

```markdown
# Code Review — <PR ou commit hash>

## Contexto
- <descrição da alteração>

## Achados da IA
- <problemas identificados>
- <oportunidades de melhoria>

## Decisões Tomadas
- <quais sugestões foram aplicadas, quais foram descartadas e por quê>

## Evidência
- <link para o PR, log da análise, etc.>
```

---

## Modelo de Justificativa de Priorização

Em `priorizacao-risco.md`, listar para cada teste prioritário:

- **Cenário:** <descrição do cenário>
- **Impacto:** <alto | médio | baixo>
- **Probabilidade de falha:** <alta | média | baixa>
- **Risco:** <alto | médio | baixo>
- **Prioridade:** <1 | 2 | 3>
- **Justificativa:** <por que esse cenário merece atenção prioritária>

---

## Referências

- Brief: [`../Projeto_Avaliativo_modulo_2.md`](../Projeto_Avaliativo_modulo_2.md) — seções 4.7 e 6.6 (critério #12)
- Evidências correlacionadas: [`../evidencias/`](../evidencias/README.md)
- Índice geral: [`../README.md`](../README.md)

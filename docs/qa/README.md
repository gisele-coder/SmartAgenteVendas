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

## Estrutura Sugerida

| Arquivo / Pasta | Conteúdo |
|---|---|
| `README.md` | Este arquivo — visão geral da pasta |
| `code-reviews/` | Relatórios de revisão de código com IA (diffs analisados, problemas encontrados, sugestões) |
| `testes/` | Suites de teste, incluindo ao menos um tipo entre integração, aceitação ou E2E |
| `relatorios/` | Sumários periódicos de qualidade, cobertura e resultados |
| `priorizacao-risco.md` | Justificativa do(s) teste(s) priorizado(s) por risco, impacto ou criticidade |

---

## Quando Popular

Esta pasta deve começar a ser preenchida assim que:

1. Houver um **Pull Request real** analisado com IA (critério #12 do brief)
2. Existir **testes relevantes** gerados ou refinados com apoio de IA
3. Ao menos um teste for **selecionado como prioritário** com justificativa documentada
4. Os testes forem executados (com **evidência de execução** armazenada em [`../evidencias/`](../evidencias/README.md))

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

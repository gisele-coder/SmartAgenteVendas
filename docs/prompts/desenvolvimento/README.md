---
origem: processo definido durante o desenvolvimento do projeto
status: oficial
data: 2026-08-29
finalidade: evidenciar os prompts usados no desenvolvimento assistido por IA, fase a fase
relacionado: [../README.md](../README.md)
---

# Prompts de Desenvolvimento

Esta pasta registra os **prompts reais utilizados durante o desenvolvimento do projeto** (interações com assistente de IA para planejamento, codificação, depuração e decisões técnicas).

---

## Finalidade

- Comprovar o **processo real de desenvolvimento assistido por IA**, fase a fase
- Servir de evidência de autoria e evolução (critérios #12 e #15 do brief — seções 6.6 e 6.7)
- Permitir que o avaliador rastreie: **prompt → decisão → artefato (commit/teste)**

## Regra de processo

> Ao final de cada fase (Parte N), **antes** de iniciar a Parte N+1:
> 1. Criar `fase-N-<nome>.md` com os prompts utilizados, resultados e evidências
> 2. Commitar na `develop` (mensagem semântica, ex.: `docs: registra prompts da fase N`)

## Convenção de arquivos

| Arquivo | Fase |
|---|---|
| `fase-0-fundacao.md` | 0 — Fundação (repo, ambiente, LLM) |
| `fase-1-dados-tools.md` | 1 — Dados + Tools |
| `fase-2-langgraph.md` | 2 — Núcleo LangGraph |
| ... | (uma por fase, em ordem) |

## Modelo de entrada

```markdown
---
origem: sessão de desenvolvimento assistido (opencode)
status: oficial
data: <AAAA-MM-DD>
fase: N — <nome>
---

# Fase N — <nome>

## Prompts utilizados
1. <prompt/instrução-chave (verbatim ou resumo fiel)>

## Resultado da interação
- <decisões, descobertas, correções>

## Evidências
- <commits, testes, comandos e resultados>
```

---
origem: convenção definida pelo brief do projeto (seção 5.4)
status: placeholder
data: 2026-08-27
finalidade: documentar prompts de sistema e histórico de refinamento do agente
relacionado: [../README.md](../README.md)
---

# Prompts

Esta pasta concentra a documentação de **prompts do agente**, conforme exigido pelo brief do projeto (seção 4.10) e pela convenção de organização do `docs/` (seção 5.4).

---

## Finalidade

- Manter **instruções de sistema** utilizadas pelo agente documentadas e versionadas
- Registrar **regras de comportamento**, objetivos da tarefa, restrições importantes e padrões de resposta esperados
- Preservar o **histórico de refinamentos**, apresentando o problema observado, a alteração realizada e o resultado obtido
- Evitar que prompts sensíveis fiquem dispersos pelo código
- **Comprovar o desenvolvimento assistido por IA**: a subpasta [`desenvolvimento/`](./desenvolvimento/README.md) registra os prompts reais usados em cada fase do projeto

---

## Estrutura Sugerida

| Arquivo / Pasta | Conteúdo |
|---|---|
| `README.md` | Este arquivo — visão geral da pasta |
| `system.md` | Prompt de sistema principal do agente (regras, objetivos, restrições) |
| `refinamentos/` | Histórico iterativo de ajustes de prompt |
| [`desenvolvimento/`](./desenvolvimento/README.md) | Prompts das fases de desenvolvimento assistido por IA (evidência por fase) |
| `outros-prompts.md` | Prompts auxiliares (ferramentas, validações, cenários específicos) |

---

## Status atual

Esta pasta já está populada:

- [`system.md`](./system.md) — prompt de sistema principal (definido na Parte 2)
- [`outros-prompts.md`](./outros-prompts.md) — prompt de usuário e prompts auxiliares
- [`desenvolvimento/`](./desenvolvimento/README.md) — prompts das fases 0-5 com evidências
- [`refinamentos/`](./refinamentos/README.md) — 2 ciclos de refinamento documentados (critério 15)

> Lembrete: o modelo (LLM) deve ser configurado por **variável de ambiente**, nunca hardcoded no repositório (seção 4.10 do brief).

---

## Modelo de Entrada para Refinamento

Cada entrada em `refinamentos/` pode seguir este padrão:

```markdown
# Refinamento — <data ou versão>

## Problema Observado
- <descrição do comportamento inadequado ou oportunidade>

## Alteração Realizada
- <mudança aplicada ao prompt>

## Resultado Obtido
- <efeito mensurável ou qualitativo observado>
- <evidência: log, métrica, screenshot, link>
```

---

## Referências

- Brief: [`../Projeto_Avaliativo_modulo_2.md`](../Projeto_Avaliativo_modulo_2.md) — seção 4.10
- Índice geral: [`../README.md`](../README.md)

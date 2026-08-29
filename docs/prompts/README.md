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

---

## Estrutura Sugerida

| Arquivo / Pasta | Conteúdo |
|---|---|
| `README.md` | Este arquivo — visão geral da pasta |
| `system.md` | Prompt de sistema principal do agente (regras, objetivos, restrições) |
| `refinamentos/` | Histórico iterativo de ajustes de prompt |
| `outros-prompts.md` | Prompts auxiliares (ferramentas, validações, cenários específicos) |

---

## Quando Popular

Esta pasta deve começar a ser preenchida assim que:

1. O **prompt de sistema principal** do agente estiver definido
2. Houver pelo menos um **ciclo de refinamento** documentado (problema → alteração → resultado)
3. Surgirem **prompts auxiliares** dignos de nota (ex.: prompt de tool de recomendação, prompt de validação)

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

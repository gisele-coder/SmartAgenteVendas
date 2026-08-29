# Documentação do Projeto

Esta pasta concentra **toda a documentação do projeto** conforme exigido pelo brief institucional (seção 5.4):

> *Organizar toda a documentação e as evidências do projeto no diretório `/docs`, utilizando subpastas quando necessário.*

---

## Índice de Arquivos

| Arquivo | Tipo | Descrição |
|---|---|---|
| [`Projeto_Avaliativo_modulo_2.md`](./Projeto_Avaliativo_modulo_2.md) | Brief | Enunciado institucional da Situação de Aprendizagem — Módulo 2 |
| [`plano-execucao.md`](./plano-execucao.md) | Doc mestre | Partes 0-9, critérios atendidos, evidências e observações de entrega (atualizado por parte) |
| [`sobre_a_planilha.md`](./sobre_a_planilha.md) | Doc interna | Descrição narrativa da base fictícia de pedidos |
| [`estrutura_planilha.md`](./estrutura_planilha.md) | Doc interna | Mapa técnico da planilha (abas e colunas) |
| [`../data/base_ficticia_pedidos_agente_ia.xlsx`](../data/base_ficticia_pedidos_agente_ia.xlsx) | Anexo | Base de dados fictícia para testes do agente (movida para `data/` em 29/08) |

## Subpastas

| Subpasta | Finalidade | Status |
|---|---|---|
| [`prompts/`](./prompts/README.md) | Prompts do sistema, prompts por fase de desenvolvimento e histórico de refinamentos | ✅ Ativa (5 fases + 2 refinamentos) |
| [`qa/`](./qa/README.md) | Evidências de QA: code review, testes, priorização por risco | Placeholder (populada na Parte 6) |
| [`evidencias/`](./evidencias/README.md) | Logs, traces, métricas, screenshots e artefatos de execução | ✅ Ativa (4 evidências arquivadas) |

## Documentos Externos

| Arquivo | Localização | Descrição |
|---|---|---|
| `Planejamento.md` | [`../Planejamento.md`](../Planejamento.md) | Planejamento geral do MVP — SmartOrder AI |

---

## Convenções

### Nomenclatura

- Preferir **kebab-case** para novos arquivos (`nome-do-doc.md`).
- Nomes descritivos do conteúdo, não do formato (`prompts.md` em vez de `doc1.md`).
- Arquivos do brief mantêm o nome original para rastreabilidade institucional.

### Estrutura recomendada para novos documentos

```markdown
---
origem: <fonte do documento>
status: <rascunho | revisão | referência | oficial>
data: <AAAA-MM-DD>
---

# Título

> Resumo de uma linha do conteúdo.

## Seções

- Listas para itens sem hierarquia forte
- Tabelas para dados tabulares
- Blocos de código para exemplos executáveis
```

### Idioma

Toda a documentação é escrita em **português**. Quando necessário, termos técnicos em inglês permanecem no original (ex.: *State*, *Tool*, *MCP*, *RAG*).

---

## Próximas Evoluções

À medida que o desenvolvimento avançar, as subpastas placeholders devem ser populadas com:

- `prompts/` — prompts de sistema e histórico de refinamentos
- `qa/` — relatórios de code review, suites de teste e justificativas de priorização
- `evidencias/` — artefatos comprobatórios de execução, logs, traces e métricas

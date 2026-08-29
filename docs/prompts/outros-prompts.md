---
origem: prompt de usuário do agente SmartOrder AI
status: oficial
data: 2026-08-29
finalidade: documentar prompts auxiliares (prompt de usuário e outros prompts não-sistema)
relacionado: [./system.md](./system.md)
---

# Prompts Auxiliares — SmartOrder AI

> Fonte de verdade em código: `app/graph/prompts.py` (função `build_user_prompt`).

---

## Prompt de usuário — `build_user_prompt`

Montado dinamicamente no node `generate_recommendations`, com quatro seções:

```text
CLIENTE {customer_id}

HISTÓRICO DE COMPRA:
- {produto} (cod {cod_prod}) | setor {setor} | categoria {categoria}   ← até 40 linhas

COOCORRÊNCIA CALCULADA (comprados junto com o histórico deste cliente):
- {produto} (cod {cod_prod}) coocorrência {n} confiança {0..1}

CATÁLOGO DISPONÍVEL:
- cod {cod_prod}: {produto} | setor {setor} | categoria {categoria}   ← 22 produtos

Gere as recomendações no formato JSON definido.
```

### Regras de montagem

| Seção | Fonte | Observações |
|---|---|---|
| `CLIENTE` | State (`customer_id`) | Identifica o thread na conversa com o modelo |
| `HISTÓRICO DE COMPRA` | Tool `get_customer_orders` | Cap de 40 linhas para controlar tokens |
| `COOCORRÊNCIA` | Tool `find_similar_products` | Top 5, já excluindo produtos já comprados |
| `CATÁLOGO DISPONÍVEL` | `get_catalog()` | Catálogo completo — o LLM só pode escolher entre estes códigos |

### Por que esse formato

- O **catálogo explícito** fecha a superfície de alucinação: o `SYSTEM_PROMPT` proíbe produtos fora dele e o node `validate_recommendations` descarta qualquer `cod_prod` inexistente (defesa em profundidade)
- A seção de **coocorrência** dá ao modelo evidência quantitativa ("comprado junto N vezes") para justificar recomendações
- O histórico limitado mantém o prompt econômico (~2,3k tokens na prática) mesmo com modelo de reasoning

## Outros prompts

| Prompt | Local | Uso |
|---|---|---|
| Prompt de sistema (identidade + regras + formato) | [`system.md`](./system.md) | Node `generate_recommendations` |
| Prompt de usuário (contexto do cliente) | Este documento (`build_user_prompt`) | Node `generate_recommendations` |
| Prompts de refinamento | [`refinamentos/`](./refinamentos/README.md) | Histórico de ciclos |
| Prompts de desenvolvimento (por fase) | [`desenvolvimento/`](./desenvolvimento/README.md) | Evidência do processo |

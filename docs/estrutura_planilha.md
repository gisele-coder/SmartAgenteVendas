---
origem: reconstrução a partir de [./sobre_a_planilha.md](./sobre_a_planilha.md)
status: referência — requer confirmação após abertura do arquivo
data: 2026-08-27
finalidade: mapear tecnicamente a estrutura da planilha fictícia
arquivo: [../data/base_ficticia_pedidos_agente_ia.xlsx](../data/base_ficticia_pedidos_agente_ia.xlsx)
---

# Estrutura da Planilha — `base_ficticia_pedidos_agente_ia.xlsx`

> **Nota importante:** este documento é uma **reconstrução parcial** feita a partir de [`sobre_a_planilha.md`](./sobre_a_planilha.md). Não foi possível ler diretamente o conteúdo do arquivo `.xlsx` (binário). **Abra o arquivo no Excel/LibreOffice e confirme as informações abaixo antes de usar como referência técnica.**

---

## 1. Visão Geral

Base fictícia estruturada para servir como **laboratório de testes** do agente inteligente de pedidos (SmartOrder AI). Substitui temporariamente a integração com o ERP real.

| Atributo | Valor |
|---|---|
| Tipo | Planilha Excel (`.xlsx`) |
| Tamanho | ~27 KB |
| Origem | Gerada para o projeto |
| Substituível por | WebService do ERP real (sem mudança na lógica do agente) |

---

## 2. Abas Prováveis

A planilha deve conter **pelo menos duas abas**. **Confirmar após abrir o arquivo:**

| Aba | Conteúdo esperado | Confirmado? |
|---|---|---|
| `Dados` (ou nome equivalente) | Tabela principal com 120 pedidos × 12 colunas + 343 linhas de itens detalhados | ☐ Pendente |
| `LEIA_ME` | Instruções sobre como a base foi estruturada | ☐ Pendente |

> Pode haver outras abas não mencionadas. Inspecionar o arquivo ao abrir.

---

## 3. Esquema de Colunas — Inferido

O esquema é o mesmo identificado para os pedidos reais do projeto. Tipos e descrições abaixo são **inferências** baseadas no domínio.

| Coluna | Tipo Inferido | Descrição | Observações |
|---|---|---|---|
| `PEDIDO` | Inteiro / String | Identificador único do pedido | Chave do pedido |
| `CLIENTE` | Inteiro / String | Identificador único do cliente | Chave do cliente |
| `QTD` | Inteiro | Quantidade do item no pedido | Sempre ≥ 1 |
| `COD_PROD` | String | Código interno do produto | Chave do produto |
| `VALOR` | Decimal | Valor unitário (ou total — **a confirmar**) | Moeda: BRL |
| `BARCODE` | String | Código de barras (EAN-13 ou similar) | Pode ter nulos |
| `PRODUTO` | String | Descrição comercial do produto | Texto livre |
| `MARCA` | String | Marca do produto | Pode ter nulos |
| `REF` | String | Referência do fabricante / SKU | Código auxiliar |
| `SETOR` | String | Setor/área do produto | Ex.: Climatização, Construção |
| `CATEGORIA` | String | Categoria comercial | Ex.: Eletroportáteis, Cozinha |
| `TIPO` | String | Tipo/subcategoria | Granularidade mais fina |

---

## 4. Cardinalidade e Estatísticas

Estatísticas esperadas com base em `sobre_a_planilha.md`:

| Métrica | Valor Esperado | Confirmado? |
|---|---:|---|
| Total de pedidos distintos | 120 | ☐ |
| Total de linhas de itens | 343 | ☐ |
| Clientes fictícios distintos | 12 | ☐ |
| Produtos distintos | 22 | ☐ |
| Média de itens por pedido | ~2,86 (343 / 120) | ☐ derivado |
| Média de pedidos por cliente | ~10 (120 / 12) | ☐ derivado |

> A média calculada acima é apenas referência. Pedidos com múltiplos produtos são propositais (vide `sobre_a_planilha.md`, seção 4).

---

## 5. Lacunas de Informação

Antes de usar a planilha como referência técnica, **confirmar manualmente**:

- [ ] Nome exato das abas
- [ ] Existência de abas adicionais além de `Dados` e `LEIA_ME`
- [ ] Se `VALOR` representa valor unitário ou total da linha
- [ ] Se há valores nulos em alguma coluna (`BARCODE`, `MARCA`, `REF` são candidatas)
- [ ] Se o esquema é **plano** (uma linha por item) ou **normalizado** (uma linha por pedido com agregação)
- [ ] Se há coluna de **data do pedido** (não mencionada, mas plausível)
- [ ] Distribuição efetiva de pedidos por cliente

---

## 6. Próximos Passos Recomendados

1. **Abrir o `.xlsx`** e validar este documento contra a estrutura real
2. **Atualizar este arquivo** com os dados confirmados, removendo o marcador "Pendente"
3. Se houver divergências, criar uma seção `## Correções` no final deste documento com o que mudou
4. Quando integrado ao agente, versionar este arquivo junto com qualquer mudança no esquema da base

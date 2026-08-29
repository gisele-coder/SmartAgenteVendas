---
origem: reconstrução a partir de [./sobre_a_planilha.md](./sobre_a_planilha.md)
status: referência — requer confirmação após abertura do arquivo
data: 2026-08-27
finalidade: mapear tecnicamente a estrutura da planilha fictícia
arquivo: [../data/base_ficticia_pedidos_agente_ia.xlsx](../data/base_ficticia_pedidos_agente_ia.xlsx)
---

# Estrutura da Planilha — `base_ficticia_pedidos_agente_ia.xlsx`

> **Status:** ✅ **CONFIRMADO EM 29/08** via inspeção programática (`pandas`). Ver seção `## Correções` ao final deste documento.

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

## 2. Abas Confirmadas

| Aba | Conteúdo | Confirmado? |
|---|---|---|
| `PEDIDOS` | Tabela principal: 343 linhas de itens × 12 colunas | ✅ Confirmado |
| `LEIA_ME` | 6 linhas × 2 colunas (`CAMPO`, `DESCRICAO`) explicando a base | ✅ Confirmado |

> Não há outras abas.

---

## 3. Esquema de Colunas — Inferido

O esquema é o mesmo identificado para os pedidos reais do projeto. Tipos e descrições abaixo são **inferências** baseadas no domínio.

| Coluna | Tipo Inferido | Descrição | Observações |
|---|---|---|---|
| `PEDIDO` | Inteiro / String | Identificador único do pedido | Chave do pedido |
| `CLIENTE` | Inteiro / String | Identificador único do cliente | Chave do cliente |
| `QTD` | Inteiro | Quantidade do item no pedido | Sempre ≥ 1 |
| `COD_PROD` | String | Código interno do produto | Chave do produto |
| `VALOR` | Decimal | **Valor TOTAL da linha (BRL)** | Confirmado: `QTD × preço unitário` (unitários terminam em `.9`) |
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
| Total de pedidos distintos | 120 | ✅ |
| Total de linhas de itens | 343 | ✅ |
| Clientes fictícios distintos | 12 | ✅ |
| Produtos distintos | 22 | ✅ |
| Média de itens por pedido | ~2,86 (343 / 120) | ✅ derivado |
| Pedidos por cliente (min / max / média) | 5 / 15 / 10,0 | ✅ medido |

> A média calculada acima é apenas referência. Pedidos com múltiplos produtos são propositais (vide `sobre_a_planilha.md`, seção 4).

---

## 5. Lacunas — Resolvidas em 29/08

- [x] Nome exato das abas → `PEDIDOS` e `LEIA_ME`
- [x] Abas adicionais → nenhuma
- [x] `VALOR` → **total da linha** (QTD × unitário; unitários terminam em `.9`)
- [x] Nulos → **zero nulos em todas as 12 colunas**
- [x] Esquema → **plano**: 1 linha por item; mesmo `PEDIDO` = itens comprados juntos; sem duplicatas `PEDIDO+COD_PROD`
- [x] Coluna de data → **não existe**
- [x] Distribuição por cliente → min 5, max 15, média 10,0 pedidos/cliente

---

## 6. Próximos Passos

1. ~~Abrir o `.xlsx` e validar~~ ✅ Concluído em 29/08
2. ~~Atualizar este arquivo~~ ✅ Concluído
3. ~~Seção `## Correções`~~ ✅ Abaixo

---

## Correções

| # | Item documentado antes | Real confirmado |
|---|---|---|
| 1 | Aba principal chamada `Dados` (inferido) | Aba chama-se **`PEDIDOS`** |
| 2 | `VALOR` possivelmente unitário | **Total da linha** (BRL) |
| 3 | Nulos possíveis em `BARCODE`, `MARCA`, `REF` | **Nenhum nulo** em nenhuma coluna |
| 4 | "Média de pedidos por cliente ~10 (120/12)" | Média exata 10,0 (min 5, max 15) |
| 5 | `LEIA_ME` com instruções genéricas | 6 linhas × 2 colunas (`CAMPO`/`DESCRICAO`), incluindo a linha "Uso para IA" |

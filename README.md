# judex

**Extração inteligente de dados do Poder Judiciário brasileiro**

> Acesse e filtre processos judiciais de qualquer tribunal do Brasil diretamente da API pública do CNJ (DataJud), exporte em CSV e conecte ao Tableau ou Power BI em segundos.

---

## O que é

**judex** é uma aplicação web construída com [Streamlit](https://streamlit.io) que permite consultar e extrair metadados processuais da [API Pública do DataJud](https://datajud-wiki.cnj.jus.br/api-publica/), mantida pelo Conselho Nacional de Justiça (CNJ).

Sem código. Sem terminal. Direto no navegador.

---

## Funcionalidades

- Seleção de tribunal (18 tribunais disponíveis: TJRS, TJSP, TRFs, STJ, STF, TST e mais)
- Filtros por grau, classe processual, assunto, município e período de ajuizamento
- Rate limit automático respeitando o limite de 120 requisições/min da API
- Cálculo do tempo médio de trânsito em julgado
- Exportação em CSV com separador `;` e encoding UTF-8 BOM (compatível com Excel, Tableau e Power BI)

---

## Campos exportados

| Campo | Descrição |
|---|---|
| `numeroProcesso` | Número CNJ unificado |
| `tribunal` | Sigla do tribunal |
| `grau` | G1, G2, JE, TR, SUP |
| `dataAjuizamento` | Data de ajuizamento (YYYY-MM-DD) |
| `dataUltimaAtualizacao` | Última atualização no DataJud |
| `classeProcessual_nome` | Nome da classe processual (TPU) |
| `assunto_nome` | Assunto principal (TPU) |
| `orgaoJulgador_nome` | Vara, câmara ou turma |
| `orgaoJulgador_municipio` | Município do órgão julgador |
| `situacao_nome` | Situação atual do processo |
| `quantidadeMovimentos` | Total de movimentações |
| `ultimoMovimento_nome` | Último movimento registrado |
| `ultimoMovimento_dataHora` | Data do último movimento |
| `dias_tramitacao` | Dias entre ajuizamento e último movimento |
| `sistema_nome` | Sistema processual (PJe, Projudi, eProc...) |
| `nivelSigilo` | Nível de sigilo (0 = público) |
| `prioridade` | Se o processo tem prioridade |

---

## Como rodar localmente

**Pré-requisitos:** Python 3.9+

```bash
git clone https://github.com/seu-usuario/judex.git
cd judex
pip install -r requirements.txt
streamlit run datajud_app.py
```

O app abre automaticamente em `http://localhost:8501`.

---

## Como usar

1. Selecione o **tribunal** na barra lateral
2. Informe a **chave de API** do DataJud (a chave pública está disponível em [datajud-wiki.cnj.jus.br](https://datajud-wiki.cnj.jus.br/api-publica/acesso))
3. Defina o **número de processos** desejado (até 10.000)
4. Aplique os **filtros** opcionais (grau, assunto, município, período)
5. Clique em **Iniciar Extração**
6. Aguarde e baixe o **CSV** gerado

---

## Base legal

Os dados são disponibilizados pelo CNJ conforme:

- Resolução CNJ nº 331/2020 — institui o DataJud
- Portaria CNJ nº 160/2020 — regulamenta o envio de dados pelos tribunais

O acesso é público, gratuito e não requer cadastro além da chave pública disponibilizada pelo próprio CNJ.

---

## Limitações

- A API retorna apenas **metadados** — documentos, petições e textos de decisões não estão disponíveis
- Processos em segredo de justiça não são retornados
- O limite da API é de **10.000 processos por consulta** (paginação via `from/offset`)
- Alguns tribunais (especialmente Projudi/JE) enviam metadados incompletos ao CNJ

---

## Stack

- [Streamlit](https://streamlit.io) — interface web
- [Requests](https://docs.python-requests.org) — chamadas à API
- [Pandas](https://pandas.pydata.org) — manipulação e exportação dos dados

---

## Licença

MIT — livre para uso, modificação e distribuição.

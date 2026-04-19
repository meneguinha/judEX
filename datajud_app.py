import streamlit as st
import requests
import pandas as pd
import math
import time
import io
from datetime import datetime, date

# =============================================================================
# CONFIGURACAO DA PAGINA
# =============================================================================

st.set_page_config(
    page_title="DataJud Extrator",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =============================================================================
# ESTILOS
# =============================================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* Fundo geral */
.stApp {
    background-color: #f5f4f0;
    color: #1a1a2e;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #ffffff;
    border-right: 1px solid #e2e0db;
}

[data-testid="stSidebar"] * {
    color: #1a1a2e !important;
}

/* Título principal */
.titulo-principal {
    font-size: 2.8rem;
    font-weight: 700;
    letter-spacing: -0.03em;
    line-height: 1.1;
    color: #1a1a2e;
    margin-bottom: 0.2rem;
}

.titulo-sub {
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
    color: #1a5276;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-bottom: 2rem;
}

/* Cards de métricas */
.metric-card {
    background: #ffffff;
    border: 1px solid #e2e0db;
    border-radius: 8px;
    padding: 1.2rem 1.5rem;
    margin-bottom: 0.8rem;
}

.metric-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.63rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #888;
    margin-bottom: 0.3rem;
}

.metric-value {
    font-size: 2rem;
    font-weight: 700;
    color: #1a5276;
    line-height: 1;
}

.metric-unit {
    font-size: 0.85rem;
    color: #aaa;
    margin-left: 0.3rem;
}

/* Barra de progresso customizada */
.progress-container {
    background: #e2e0db;
    border-radius: 4px;
    height: 6px;
    width: 100%;
    margin: 0.5rem 0;
    overflow: hidden;
}

.progress-bar {
    background: linear-gradient(90deg, #1a5276, #2980b9);
    height: 100%;
    border-radius: 4px;
    transition: width 0.3s ease;
}

/* Seção de resultado */
.resultado-header {
    font-family: 'DM Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #1a5276;
    border-bottom: 1px solid #e2e0db;
    padding-bottom: 0.5rem;
    margin: 1.5rem 0 1rem 0;
}

/* Alerta de trânsito em julgado */
.transito-card {
    background: #ffffff;
    border: 1px solid #aed6f144;
    border-left: 3px solid #1a5276;
    border-radius: 8px;
    padding: 1.2rem 1.5rem;
    margin: 1rem 0;
}

/* Inputs */
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stSelectbox > div > div,
.stDateInput > div > div > input {
    background-color: #ffffff !important;
    border: 1px solid #e2e0db !important;
    color: #1a1a2e !important;
    border-radius: 6px !important;
    font-family: 'DM Mono', monospace !important;
}

/* Botão principal */
.stButton > button {
    background: #1a5276 !important;
    color: #ffffff !important;
    border: none !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.03em !important;
    padding: 0.6rem 2rem !important;
    border-radius: 6px !important;
    width: 100% !important;
    transition: all 0.2s !important;
}

.stButton > button:hover {
    background: #2980b9 !important;
    transform: translateY(-1px) !important;
}

/* Botão de download */
.stDownloadButton > button {
    background: transparent !important;
    color: #1a5276 !important;
    border: 1px solid #1a5276 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    width: 100% !important;
    border-radius: 6px !important;
}

/* Divisor */
hr {
    border-color: #e2e0db !important;
    margin: 1.5rem 0 !important;
}

/* Tabela */
.stDataFrame {
    border: 1px solid #e2e0db !important;
    border-radius: 8px !important;
}

/* Expander */
.streamlit-expanderHeader {
    background-color: #ffffff !important;
    border: 1px solid #e2e0db !important;
    border-radius: 6px !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.8rem !important;
    color: #888 !important;
}

/* Label dos campos */
label {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.70rem !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    color: #888 !important;
}

/* Info/warning boxes */
.stInfo, .stWarning, .stError, .stSuccess {
    border-radius: 6px !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.8rem !important;
}

div[data-testid="stStatusWidget"] { display: none; }
</style>
""", unsafe_allow_html=True)

# =============================================================================
# FUNCOES DE EXTRACAO
# =============================================================================

TRIBUNAIS = {
    "TJRS - Tribunal de Justiça do RS": "tjrs",
    "TJSP - Tribunal de Justiça de SP": "tjsp",
    "TJRJ - Tribunal de Justiça do RJ": "tjrj",
    "TJMG - Tribunal de Justiça de MG": "tjmg",
    "TJPR - Tribunal de Justiça do PR": "tjpr",
    "TJSC - Tribunal de Justiça de SC": "tjsc",
    "TJBA - Tribunal de Justiça da BA": "tjba",
    "TJPE - Tribunal de Justiça de PE": "tjpe",
    "TJCE - Tribunal de Justiça do CE": "tjce",
    "TRF1 - Tribunal Regional Federal 1ª Região": "trf1",
    "TRF2 - Tribunal Regional Federal 2ª Região": "trf2",
    "TRF3 - Tribunal Regional Federal 3ª Região": "trf3",
    "TRF4 - Tribunal Regional Federal 4ª Região": "trf4",
    "TRF5 - Tribunal Regional Federal 5ª Região": "trf5",
    "STJ - Superior Tribunal de Justiça": "stj",
    "STF - Supremo Tribunal Federal": "stf",
    "TST - Tribunal Superior do Trabalho": "tst",
    "TRT4 - Tribunal Regional do Trabalho 4ª Região": "trt4",
}

GRAUS = {
    "Todos": None,
    "G1 - Primeiro Grau": "G1",
    "G2 - Segundo Grau": "G2",
    "JE - Juizado Especial": "JE",
    "TR - Turma Recursal": "TR",
    "SUP - Superior": "SUP",
}


def calcular_intervalo(quantidade):
    n_req = math.ceil(quantidade / 10)
    if n_req <= 10:
        return 0.0, n_req
    elif n_req <= 50:
        return 0.5, n_req
    else:
        return 0.52, n_req


def extrair_dict(valor):
    if isinstance(valor, dict):
        return valor
    if isinstance(valor, list):
        return valor[0] if valor else {}
    return {}


def normalizar_data(valor):
    if not valor:
        return ""
    s = str(valor).strip()
    if len(s) >= 10 and s[4] == "-" and s[7] == "-":
        return s[:10]
    if s.isdigit() and len(s) >= 8:
        return f"{s[0:4]}-{s[4:6]}-{s[6:8]}"
    return s


def normalizar_processo(hit, tribunal):
    src = hit.get("_source", {})
    classe            = extrair_dict(src.get("classeProcessual", {}))
    assuntos          = src.get("assuntos", [])
    assuntos          = assuntos if isinstance(assuntos, list) else []
    assunto_principal = extrair_dict(assuntos[0] if assuntos else {})
    orgao             = extrair_dict(src.get("orgaoJulgador", {}))
    movimentos        = src.get("movimentos", [])
    movimentos        = movimentos if isinstance(movimentos, list) else []
    ultimo_mov        = extrair_dict(movimentos[0] if movimentos else {})
    situacao          = extrair_dict(src.get("situacao", {}))
    formato           = extrair_dict(src.get("formato", {}))
    sistema           = extrair_dict(src.get("sistema", {}))

    return {
        "numeroProcesso":                    src.get("numeroProcesso", ""),
        "tribunal":                          src.get("siglaTribunal", tribunal.upper()),
        "grau":                              src.get("grau", ""),
        "dataAjuizamento":                   normalizar_data(src.get("dataAjuizamento", "")),
        "dataUltimaAtualizacao":             normalizar_data(src.get("dataHoraUltimaAtualizacao", "")),
        "classeProcessual_codigo":           classe.get("codigo", ""),
        "classeProcessual_nome":             classe.get("nome", ""),
        "assunto_codigo":                    assunto_principal.get("codigo", ""),
        "assunto_nome":                      assunto_principal.get("nome", ""),
        "assunto_codigoPai":                 assunto_principal.get("codigoPai", ""),
        "assunto_principal":                 assunto_principal.get("principal", ""),
        "orgaoJulgador_codigo":              orgao.get("codigo", ""),
        "orgaoJulgador_nome":                orgao.get("nome", ""),
        "orgaoJulgador_municipio":           orgao.get("municipio", ""),
        "orgaoJulgador_codigoMunicipioIBGE": orgao.get("codigoMunicipioIBGE", ""),
        "orgaoJulgador_instancia":           orgao.get("instancia", ""),
        "situacao_codigo":                   situacao.get("codigo", ""),
        "situacao_nome":                     situacao.get("nome", ""),
        "quantidadeMovimentos":              len(movimentos),
        "ultimoMovimento_codigo":            ultimo_mov.get("codigo", ""),
        "ultimoMovimento_nome":              ultimo_mov.get("nome", ""),
        "ultimoMovimento_dataHora":          normalizar_data(ultimo_mov.get("dataHora", "")),
        "ultimoMovimento_complemento":       ultimo_mov.get("complemento", ""),
        "nivelSigilo":                       src.get("nivelSigilo", 0),
        "prioridade":                        "Sim" if src.get("prioridade") else "Nao",
        "formato_codigo":                    formato.get("codigo", ""),
        "formato_nome":                      formato.get("nome", ""),
        "sistema_codigo":                    sistema.get("codigo", ""),
        "sistema_nome":                      sistema.get("nome", ""),
        "codigoLocalidade":                  src.get("codigoLocalidade", ""),
        "dias_tramitacao":                   "",
    }


def montar_query(from_offset, classe_processual, assunto_codigo, grau, municipio_ibge, data_inicio, data_fim):
    filtros = []
    if classe_processual:
        filtros.append({"term": {"classeProcessual.codigo": int(classe_processual)}})
    if assunto_codigo:
        filtros.append({"term": {"assuntos.codigo": int(assunto_codigo)}})
    if grau:
        filtros.append({"term": {"grau.keyword": grau}})
    if municipio_ibge:
        filtros.append({"term": {"orgaoJulgador.codigoMunicipioIBGE": municipio_ibge}})
    if data_inicio:
        filtros.append({"range": {"dataAjuizamento": {"gte": str(data_inicio)}}})
    if data_fim:
        filtros.append({"range": {"dataAjuizamento": {"lte": str(data_fim)}}})

    return {
        "size": 10,
        "from": from_offset,
        "query": {"bool": {"must": filtros if filtros else [{"match_all": {}}]}},
    }


def calcular_transito(df):
    df = df.copy()
    df["_ajuiz_dt"]   = pd.to_datetime(df["dataAjuizamento"], errors="coerce")
    df["_ultimo_dt"]  = pd.to_datetime(df["ultimoMovimento_dataHora"], errors="coerce")
    df["dias_tramitacao"] = (df["_ultimo_dt"] - df["_ajuiz_dt"]).dt.days.astype("Int64")
    df = df.drop(columns=["_ajuiz_dt", "_ultimo_dt"])

    mask    = df["ultimoMovimento_nome"].str.strip().str.lower() == "trânsito em julgado"
    df_enc  = df[mask]

    stats = None
    if not df_enc.empty:
        stats = {
            "total":   len(df_enc),
            "media":   df_enc["dias_tramitacao"].mean(),
            "mediana": df_enc["dias_tramitacao"].median(),
            "minimo":  df_enc["dias_tramitacao"].min(),
            "maximo":  df_enc["dias_tramitacao"].max(),
        }
    return df, stats


def executar_extracao(tribunal, api_key, quantidade, classe_processual, assunto_codigo,
                      grau, municipio_ibge, data_inicio, data_fim,
                      progress_bar, status_text, metrics_placeholder):

    intervalo, n_req = calcular_intervalo(quantidade)
    base_url = f"https://api-publica.datajud.cnj.jus.br/api_publica_{tribunal}/_search"
    headers  = {"Authorization": f"APIKey {api_key}", "Content-Type": "application/json"}

    processos   = []
    offset      = 0
    pagina      = 1
    erros       = 0
    MAX_ERROS   = 5
    total_req   = 0
    ultimo_req  = 0.0
    inicio      = time.monotonic()

    while len(processos) < quantidade:
        # Rate limiting
        if intervalo > 0:
            agora     = time.monotonic()
            decorrido = agora - ultimo_req
            if decorrido < intervalo:
                time.sleep(intervalo - decorrido)
        ultimo_req = time.monotonic()

        query = montar_query(offset, classe_processual, assunto_codigo,
                             grau, municipio_ibge, data_inicio, data_fim)

        try:
            resp = requests.post(base_url, headers=headers, json=query, timeout=30)
            total_req += 1

            if resp.status_code == 429:
                status_text.warning("Rate limit atingido. Aguardando 10s...")
                time.sleep(10)
                continue

            if resp.status_code == 401:
                status_text.error("Chave de API inválida ou expirada. Atualize a chave na barra lateral.")
                return None

            if resp.status_code != 200:
                erros += 1
                status_text.warning(f"Erro HTTP {resp.status_code} (tentativa {erros}/{MAX_ERROS})")
                if erros >= MAX_ERROS:
                    status_text.error("Muitos erros consecutivos. Encerrando extração.")
                    break
                continue

            hits = resp.json().get("hits", {}).get("hits", [])

            if not hits:
                status_text.info(f"Sem mais resultados. Total extraído: {len(processos)}")
                break

            for hit in hits:
                if len(processos) >= quantidade:
                    break
                processos.append(normalizar_processo(hit, tribunal))

            offset   += len(hits)
            erros     = 0
            decorrido = time.monotonic() - inicio
            rpm       = (total_req / decorrido * 60) if decorrido > 0 else 0
            pct       = min(len(processos) / quantidade, 1.0)

            progress_bar.progress(pct)
            status_text.markdown(
                f"Página **{pagina}** · Extraídos **{len(processos)}/{quantidade}** "
                f"· {rpm:.0f} req/min"
            )
            metrics_placeholder.markdown(
                f"<div class='metric-card'>"
                f"<div class='metric-label'>Processos extraídos</div>"
                f"<div class='metric-value'>{len(processos)}<span class='metric-unit'>/ {quantidade}</span></div>"
                f"</div>"
                f"<div class='metric-card'>"
                f"<div class='metric-label'>Requisições</div>"
                f"<div class='metric-value'>{total_req}<span class='metric-unit'>req</span></div>"
                f"</div>"
                f"<div class='metric-card'>"
                f"<div class='metric-label'>Taxa</div>"
                f"<div class='metric-value'>{rpm:.0f}<span class='metric-unit'>req/min</span></div>"
                f"</div>",
                unsafe_allow_html=True,
            )
            pagina += 1

        except requests.exceptions.Timeout:
            erros += 1
            status_text.warning(f"Timeout (tentativa {erros}/{MAX_ERROS})")
            if erros >= MAX_ERROS:
                break
        except Exception as e:
            erros += 1
            status_text.warning(f"Erro: {e} (tentativa {erros}/{MAX_ERROS})")
            if erros >= MAX_ERROS:
                break

    return pd.DataFrame(processos) if processos else None


# =============================================================================
# INTERFACE
# =============================================================================

# --- Cabeçalho ---
st.markdown("<div class='titulo-principal'>DataJud<br>Extrator</div>", unsafe_allow_html=True)
st.markdown("<div class='titulo-sub'>⚖ CNJ · Base Nacional de Dados do Poder Judiciário</div>", unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.markdown("### Configuração")
    st.markdown("---")

    tribunal_label = st.selectbox("Tribunal", list(TRIBUNAIS.keys()), index=0)
    tribunal       = TRIBUNAIS[tribunal_label]

    api_key = st.text_input(
        "Chave API DataJud",
        value="cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw==",
        type="password",
        help="Consulte a chave vigente em datajud-wiki.cnj.jus.br/api-publica/acesso",
    )

    quantidade = st.number_input(
        "Número de processos",
        min_value=10,
        max_value=10000,
        value=100,
        step=10,
        help="Máximo de 10.000 por extração",
    )

    st.markdown("---")
    st.markdown("### Filtros opcionais")

    grau_label     = st.selectbox("Grau", list(GRAUS.keys()), index=0)
    grau           = GRAUS[grau_label]

    classe_processual = st.text_input(
        "Código da Classe Processual",
        value="",
        placeholder="Ex: 7, 40, 219",
        help="Consulte os códigos na TPU do CNJ",
    ) or None

    assunto_codigo = st.text_input(
        "Código do Assunto",
        value="",
        placeholder="Ex: 9980, 10456",
        help="Ex: 10456 = Difamação",
    ) or None

    municipio_ibge = st.text_input(
        "Código IBGE do Município",
        value="",
        placeholder="Ex: 4314902 (Porto Alegre)",
    ) or None

    st.markdown("---")
    st.markdown("### Período de ajuizamento")

    col_d1, col_d2 = st.columns(2)
    with col_d1:
        data_inicio = st.date_input("De", value=None, min_value=date(1990, 1, 1))
    with col_d2:
        data_fim = st.date_input("Até", value=None, min_value=date(1990, 1, 1))

    st.markdown("---")

    intervalo_calc, n_req_calc = calcular_intervalo(quantidade)
    tempo_est = n_req_calc * intervalo_calc
    st.markdown(
        f"<div style='font-family:DM Mono,monospace;font-size:0.7rem;color:#999;line-height:1.8'>"
        f"~{n_req_calc} requisições<br>"
        f"intervalo: {intervalo_calc}s<br>"
        f"tempo est.: ~{tempo_est:.0f}s"
        f"</div>",
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)
    iniciar = st.button("⚖ Iniciar Extração")

# --- Área principal ---
col_main, col_side = st.columns([3, 1])

with col_main:
    if not iniciar:
        st.markdown(
            "<div style='color:#aaa;font-family:DM Mono,monospace;font-size:0.8rem;"
            "margin-top:3rem;line-height:2'>Configure os parâmetros na barra lateral<br>"
            "e clique em Iniciar Extração.</div>",
            unsafe_allow_html=True,
        )

    if iniciar:
        progress_bar       = st.progress(0)
        status_text        = st.empty()
        metrics_placeholder = col_side.empty()

        with st.spinner(""):
            df = executar_extracao(
                tribunal       = tribunal,
                api_key        = api_key,
                quantidade     = quantidade,
                classe_processual = classe_processual,
                assunto_codigo = assunto_codigo,
                grau           = grau,
                municipio_ibge = municipio_ibge,
                data_inicio    = data_inicio if data_inicio else None,
                data_fim       = data_fim if data_fim else None,
                progress_bar   = progress_bar,
                status_text    = status_text,
                metrics_placeholder = metrics_placeholder,
            )

        if df is not None and not df.empty:
            progress_bar.progress(1.0)
            status_text.success(f"Extração concluída — {len(df)} processos")

            # Calcular trânsito em julgado
            df, stats_transito = calcular_transito(df)

            # --- Resultado trânsito ---
            st.markdown("<div class='resultado-header'>Trânsito em Julgado</div>", unsafe_allow_html=True)

            if stats_transito:
                t = stats_transito
                c1, c2, c3, c4, c5 = st.columns(5)
                c1.metric("Processos encerrados", t["total"])
                c2.metric("Tempo médio", f"{t['media']:.0f} dias")
                c3.metric("Mediana", f"{t['mediana']:.0f} dias")
                c4.metric("Mínimo", f"{t['minimo']:.0f} dias")
                c5.metric("Máximo", f"{t['maximo']:.0f} dias")
            else:
                st.info("Nenhum processo com Trânsito em Julgado nesta amostra.")

            # --- Preview da tabela ---
            st.markdown("<div class='resultado-header'>Prévia dos dados</div>", unsafe_allow_html=True)
            st.dataframe(df.head(20), use_container_width=True, height=300)

            # --- Download ---
            st.markdown("<div class='resultado-header'>Exportar</div>", unsafe_allow_html=True)

            csv_bytes = df.to_csv(index=False, sep=";", encoding="utf-8-sig").encode("utf-8-sig")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nome_csv  = f"processos_{tribunal}_{timestamp}.csv"

            st.download_button(
                label="⬇ Baixar CSV (separador ;  ·  UTF-8 BOM  ·  Tableau-ready)",
                data=csv_bytes,
                file_name=nome_csv,
                mime="text/csv",
            )

            with st.expander("Ver informações do arquivo"):
                st.markdown(
                    f"<div style='font-family:DM Mono,monospace;font-size:0.75rem;line-height:2;color:#666'>"
                    f"Arquivo : {nome_csv}<br>"
                    f"Processos : {len(df)}<br>"
                    f"Colunas : {len(df.columns)}<br>"
                    f"Separador : ; (ponto-e-vírgula)<br>"
                    f"Encoding : UTF-8 com BOM<br>"
                    f"Compatível com : Excel · Tableau · Power BI"
                    f"</div>",
                    unsafe_allow_html=True,
                )
        elif iniciar:
            st.error("Nenhum dado retornado. Verifique as configurações e tente novamente.")

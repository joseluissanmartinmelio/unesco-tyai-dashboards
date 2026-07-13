import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="La integridad de Chile en datos",
    page_icon="",
    layout="wide",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&family=Space+Grotesk:wght@500;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #f0f4f8;
    color: #1a2332;
}

/* Header */
.dash-header {
    background: linear-gradient(135deg, #0a2540 0%, #1a4a7a 60%, #2563a8 100%);
    border-radius: 12px;
    padding: 2rem 2.5rem;
    margin-bottom: 1.5rem;
    color: white;
}
.dash-header h1 {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.75rem;
    font-weight: 700;
    margin: 0 0 0.25rem 0;
    letter-spacing: -0.5px;
    color: white;
}
.dash-header p {
    font-size: 0.9rem;
    color: #a8c5e8;
    margin: 0;
    font-weight: 300;
}

/* Metric cards */
.metric-row {
    display: flex;
    gap: 1rem;
    margin-bottom: 1.5rem;
    flex-wrap: wrap;
}
.metric-card {
    background: white;
    border-radius: 10px;
    padding: 1.1rem 1.4rem;
    flex: 1;
    min-width: 160px;
    border-left: 4px solid #2563a8;
    box-shadow: 0 1px 4px rgba(0,0,0,0.07);
}
.metric-card .label {
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #6b7280;
    font-weight: 600;
    margin-bottom: 0.3rem;
}
.metric-card .value {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.5rem;
    font-weight: 700;
    color: #0a2540;
}
.metric-card .sub {
    font-size: 0.75rem;
    color: #9ca3af;
    margin-top: 0.1rem;
}

/* Section titles */
.section-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 0.8rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #6b7280;
    margin: 1.5rem 0 0.75rem 0;
    padding-bottom: 0.4rem;
    border-bottom: 1px solid #e5e7eb;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #0a2540;
}
section[data-testid="stSidebar"] > div {
    color: white !important;
}
section[data-testid="stSidebar"] .stSelectbox label,
section[data-testid="stSidebar"] .stMultiSelect label {
    color: #a8c5e8 !important;
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}

/* Chart container */
.chart-container {
    background: white;
    border-radius: 10px;
    padding: 1rem;
    box-shadow: 0 1px 4px rgba(0,0,0,0.07);
    margin-bottom: 1rem;
}

/* Footer */
.footer {
    text-align: center;
    font-size: 0.72rem;
    color: #9ca3af;
    margin-top: 2rem;
    padding-top: 1rem;
    border-top: 1px solid #e5e7eb;
}
</style>
""", unsafe_allow_html=True)

# ── Dataset registry ──────────────────────────────────────────────────────────
DATASETS = {
    "CPI - Percepción de Corrupción": {
        "file": "cpi.csv",
        "score_var": "CPI_score",
        "time_var": "Year",
        "country_var": "country",
        "ocde_var": "ocde",
        "latam_var": "latam",
        "higher_is_better": True,
        "scale": "0-100 (mayor = menos corrupto)",
    },
    "OBS - Open Budget Survey": {
        "file": "obs.csv",
        "score_var": "OBI_unrounded",
        "time_var": "Year",
        "country_var": "country",
        "ocde_var": "ocde",
        "latam_var": "latam",
        "higher_is_better": True,
        "scale": "0-100 (mayor = más transparente)",
    },
    "WGI-CC - Control of Corruption": {
        "file": "wgicc.csv",
        "score_var": "value",
        "time_var": "year",
        "country_var": "country",
        "ocde_var": "ocde",
        "latam_var": "latam",
        "higher_is_better": True,
        "scale": "-2.5 a 2.5 (mayor = mejor)",
    },
    "WJP - Rule of Law Index": {
        "file": "wjprol.csv",
        "score_var": "WJP_Rule_of_Law_Index_Overall_Score",
        "time_var": "Year",
        "country_var": "country",
        "ocde_var": "ocde",
        "latam_var": "latam",
        "higher_is_better": True,
        "scale": "0-1 (mayor = mejor)",
    },
}

DATA_PATH = "./data"

# ── Load data ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_dataset(meta):
    path = os.path.join(DATA_PATH, meta["file"])
    df = pd.read_csv(path)
    # Normalize column names
    df.columns = df.columns.str.strip()
    # Cast year to int where possible
    df[meta["time_var"]] = pd.to_numeric(df[meta["time_var"]], errors="coerce")
    df[meta["score_var"]] = pd.to_numeric(df[meta["score_var"]], errors="coerce")
    df[meta["ocde_var"]] = pd.to_numeric(df[meta["ocde_var"]], errors="coerce")
    df[meta["latam_var"]] = pd.to_numeric(df[meta["latam_var"]], errors="coerce")
    df = df.dropna(subset=[meta["time_var"], meta["score_var"]])
    df[meta["time_var"]] = df[meta["time_var"]].astype(int)
    return df

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### Filtros")
    st.markdown("---")

    region = st.selectbox(
        "Región de comparación",
        options=["OCDE", "LATAM"],
        index=0,
    )

    year_range = st.slider(
        "Rango de años",
        min_value=2000,
        max_value=2025,
        value=(2000, 2025),
        step=1,
    )

    st.markdown("---")
    st.markdown(
        "<small style='color:#a8c5e8'>Cátedra UNESCO - Datos abiertos<br>Cada índice cubre años distintos.</small>",
        unsafe_allow_html=True,
    )

region_var = "ocde" if region == "OCDE" else "latam"
region_label = "OCDE" if region == "OCDE" else "América Latina"

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="dash-header">
    <h1>La integridad de Chile en perspectiva comparada</h1>
    <p>Índices de gobernanza y corrupción - Chile vs {region_label} - {year_range[0]}-{year_range[1]}</p>
</div>
""", unsafe_allow_html=True)

# ── Charts ────────────────────────────────────────────────────────────────────
CHILE_COLOR = "#2563a8"
REGION_COLOR = "#93c5e8"
GRID_COLOR = "#f0f4f8"

for idx_name, meta in DATASETS.items():
    try:
        df = load_dataset(meta)
    except FileNotFoundError:
        st.warning(f"⚠️ Archivo no encontrado: `{meta['file']}`")
        continue

    tv = meta["time_var"]
    sv = meta["score_var"]
    cv = meta["country_var"]
    ov = meta[f"{region_var}_var"] if f"{region_var}_var" in meta else (
        meta["ocde_var"] if region_var == "ocde" else meta["latam_var"]
    )

    # Filter years
    df_f = df[(df[tv] >= year_range[0]) & (df[tv] <= year_range[1])]

    # Chile series
    chile = (
        df_f[df_f[cv] == "Chile"]
        .groupby(tv)[sv]
        .mean()
        .reset_index()
        .sort_values(tv)
    )

    # Region series (mean of group, excluding Chile)
    region_df = (
        df_f[(df_f[ov] == 1) & (df_f[cv] != "Chile")]
        .groupby(tv)[sv]
        .mean()
        .reset_index()
        .sort_values(tv)
    )

    if chile.empty and region_df.empty:
        st.info(f"{idx_name}: sin datos para el período seleccionado.")
        continue

    # Summary stats for current period
    chile_last = chile[sv].iloc[-1] if not chile.empty else None
    region_last = region_df[sv].iloc[-1] if not region_df.empty else None

    direction = "Mientras más ↑ mejor" if meta["higher_is_better"] else "Mientras menos ↓ mejor"

    st.markdown(f'<div class="section-title">{idx_name}</div>', unsafe_allow_html=True)

    col_meta, col_chart = st.columns([1, 3])

    with col_meta:
        if chile_last is not None:
            st.markdown(f"""
            <div class="metric-card">
                <div class="label">Chile (último año)</div>
                <div class="value">{chile_last:.2f}</div>
                <div class="sub">{meta['scale']}</div>
            </div>
            """, unsafe_allow_html=True)
        if region_last is not None:
            diff = chile_last - region_last if chile_last is not None else None
            diff_str = ""
            if diff is not None:
                sign = "+" if diff > 0 else ""
                better = (diff > 0) == meta["higher_is_better"]
                color = "#16a34a" if better else "#dc2626"
                diff_str = f'<span style="color:{color};font-size:0.8rem">({sign}{diff:.2f} vs {region_label})</span>'
            st.markdown(f"""
            <div class="metric-card" style="border-left-color:#93c5e8; margin-top:0.75rem">
                <div class="label">Promedio {region_label}</div>
                <div class="value">{region_last:.2f}</div>
                <div class="sub">{diff_str}</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown(f'<p style="font-size:0.72rem;color:#9ca3af;margin-top:0.5rem">{direction}</p>', unsafe_allow_html=True)

    with col_chart:
        fig = go.Figure()

        # Region band (min/max) for context
        region_band = (
            df_f[(df_f[ov] == 1) & (df_f[cv] != "Chile")]
            .groupby(tv)[sv]
            .agg(["min", "max"])
            .reset_index()
            .sort_values(tv)
        )

        if not region_band.empty:
            fig.add_trace(go.Scatter(
                x=pd.concat([region_band[tv], region_band[tv][::-1]]),
                y=pd.concat([region_band["max"], region_band["min"][::-1]]),
                fill="toself",
                fillcolor="rgba(147,197,232,0.15)",
                line=dict(color="rgba(0,0,0,0)"),
                name=f"Rango {region_label}",
                hoverinfo="skip",
            ))

        # Region mean line
        if not region_df.empty:
            fig.add_trace(go.Scatter(
                x=region_df[tv],
                y=region_df[sv],
                mode="lines",
                name=f"Promedio {region_label}",
                line=dict(color=REGION_COLOR, width=2, dash="dot"),
                hovertemplate=f"%{{x}}: %{{y:.2f}} ({region_label})<extra></extra>",
            ))

        # Chile line
        if not chile.empty:
            fig.add_trace(go.Scatter(
                x=chile[tv],
                y=chile[sv],
                mode="lines+markers",
                name="Chile",
                line=dict(color=CHILE_COLOR, width=2.5),
                marker=dict(size=5, color=CHILE_COLOR),
                hovertemplate="%{x}: %{y:.2f} (Chile)<extra></extra>",
            ))

        fig.update_layout(
            height=220,
            margin=dict(l=0, r=10, t=10, b=30),
            paper_bgcolor="white",
            plot_bgcolor="white",
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                font=dict(size=11),
            ),
            xaxis=dict(
                showgrid=True,
                gridcolor=GRID_COLOR,
                tickfont=dict(size=10),
                dtick=2,
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor=GRID_COLOR,
                tickfont=dict(size=10),
                zeroline=False,
            ),
            hovermode="x unified",
            font=dict(family="Inter, sans-serif"),
        )

        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    st.markdown("<hr style='border:none;border-top:1px solid #e5e7eb;margin:0.5rem 0 1rem'>", unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    Cátedra UNESCO - Fuentes: Transparency International, IBP, TRACE International, World Bank, World Justice Project - Datos abiertos
</div>
""", unsafe_allow_html=True)

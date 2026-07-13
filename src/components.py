# components.py
# ── Componentes de UI ─────────────────────────────────────────────────────────
# Funciones que renderizan bloques HTML/Streamlit.
# Cada función hace una sola cosa; el HTML vive aquí, no en app.py.

import streamlit as st

from src.config import COLORS
from src.charts import build_index_figure

# ── Header ────────────────────────────────────────────────────────────────────

def render_header(region_label: str, year_range: tuple[int, int]) -> None:
    st.markdown(f"""
    <div class="dash-header">
        <h1>Chile en perspectiva comparada</h1>
        <p>Índices de gobernanza y corrupción · Chile vs {region_label} · {year_range[0]}–{year_range[1]}</p>
    </div>
    """, unsafe_allow_html=True)


# ── Sidebar ───────────────────────────────────────────────────────────────────

def render_sidebar(available_regions: list[str]) -> tuple[str, tuple[int, int]]:
    """Renderiza los controles del sidebar y devuelve los valores seleccionados.

    Returns:
        (region_key, year_range)
    """
    from src.config import YEAR_MIN, YEAR_MAX, YEAR_DEFAULT

    with st.sidebar:
        st.markdown("### 🔎 Filtros")
        st.markdown("---")

        region_key = st.selectbox(
            "Región de comparación",
            options=available_regions,
            index=0,
        )

        year_range = st.slider(
            "Rango de años",
            min_value=YEAR_MIN,
            max_value=YEAR_MAX,
            value=YEAR_DEFAULT,
            step=1,
        )

        st.markdown("---")
        st.markdown(
            "<small style='color:#a8c5e8'>Cátedra UNESCO · Datos abiertos"
            "<br>Cada índice cubre años distintos.</small>",
            unsafe_allow_html=True,
        )

    return region_key, year_range


# ── Metric cards ──────────────────────────────────────────────────────────────

def _metric_card(label: str, value: float, sub: str = "",
                 border_color: str = COLORS["chile"]) -> str:
    return f"""
    <div class="metric-card" style="border-left-color:{border_color}">
        <div class="label">{label}</div>
        <div class="value">{value:.2f}</div>
        <div class="sub">{sub}</div>
    </div>
    """


def render_metric_col(
    score_var:    str,
    series:       dict,
    meta:         dict,
    region_label: str,
) -> None:
    """Renderiza la columna izquierda con las metric cards de un índice."""
    chile       = series["chile"]
    region_mean = series["region_mean"]

    chile_last  = chile[score_var].iloc[-1]  if not chile.empty       else None
    region_last = region_mean[score_var].iloc[-1] if not region_mean.empty else None

    direction = "↑ mejor" if meta["higher_is_better"] else "↓ mejor"

    if chile_last is not None:
        st.markdown(
            _metric_card("Chile (último año)", chile_last, meta["scale"]),
            unsafe_allow_html=True,
        )

    if region_last is not None:
        diff_str = ""
        if chile_last is not None:
            diff  = chile_last - region_last
            sign  = "+" if diff > 0 else ""
            better = (diff > 0) == meta["higher_is_better"]
            color  = COLORS["positive"] if better else COLORS["negative"]
            diff_str = (
                f'<span style="color:{color};font-size:0.8rem">'
                f'({sign}{diff:.2f} vs {region_label})</span>'
            )
        st.markdown(
            _metric_card(
                f"Promedio {region_label}", region_last,
                sub=diff_str, border_color=COLORS["region"]
            ),
            unsafe_allow_html=True,
        )

    st.markdown(
        f'<p style="font-size:0.72rem;color:#9ca3af;margin-top:0.5rem">{direction}</p>',
        unsafe_allow_html=True,
    )


# ── Sección completa de un índice ─────────────────────────────────────────────

def render_index_section(
    idx_name:     str,
    meta:         dict,
    series:       dict,
    region_label: str,
) -> None:
    """Renderiza título + metric cards + chart de un índice."""
    st.markdown(
        f'<div class="section-title">{idx_name}</div>',
        unsafe_allow_html=True,
    )

    col_meta, col_chart = st.columns([1, 3])

    with col_meta:
        render_metric_col(meta["score_var"], series, meta, region_label)

    with col_chart:
        fig = build_index_figure(
            series       = series,
            time_var     = meta["time_var"],
            score_var    = meta["score_var"],
            region_label = region_label,
        )
        st.plotly_chart(fig, use_container_width=True,
                        config={"displayModeBar": False})

    st.markdown(
        "<hr style='border:none;border-top:1px solid #e5e7eb;margin:0.5rem 0 1rem'>",
        unsafe_allow_html=True,
    )


# ── Footer ────────────────────────────────────────────────────────────────────

def render_footer() -> None:
    st.markdown("""
    <div class="footer">
        Cátedra UNESCO · Fuentes: Transparency International, IBP, TRACE International,
        World Bank, World Justice Project · Datos abiertos
    </div>
    """, unsafe_allow_html=True)

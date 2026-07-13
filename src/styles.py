# styles.py
# ── Estilos CSS del dashboard ─────────────────────────────────────────────────
# Todo el CSS vive aquí. inject_styles() lo inyecta una sola vez desde app.py.
# Para cambiar colores base usar config.py; para cambiar layout/tipografía
# editar los bloques de este archivo.

import streamlit as st

_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&family=Space+Grotesk:wght@500;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #f0f4f8;
    color: #1a2332;
}

/* ── Header ──────────────────────────────────────────────────────────────── */
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

/* ── Metric cards ────────────────────────────────────────────────────────── */
.metric-card {
    background: white;
    border-radius: 10px;
    padding: 1.1rem 1.4rem;
    border-left: 4px solid #2563a8;
    box-shadow: 0 1px 4px rgba(0,0,0,0.07);
    margin-bottom: 0.75rem;
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

/* ── Section titles ──────────────────────────────────────────────────────── */
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

/* ── Sidebar ─────────────────────────────────────────────────────────────── */
section[data-testid="stSidebar"] {
    background-color: #0a2540;
}
section[data-testid="stSidebar"] < div {
    color: white !important;
}
section[data-testid="stSidebar"] .stSelectbox label,
section[data-testid="stSidebar"] .stMultiSelect label {
    color: #a8c5e8 !important;
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}

/* ── Footer ──────────────────────────────────────────────────────────────── */
.footer {
    text-align: center;
    font-size: 0.72rem;
    color: #9ca3af;
    margin-top: 2rem;
    padding-top: 1rem;
    border-top: 1px solid #e5e7eb;
}
</style>
"""


def inject_styles() -> None:
    """Inyecta el CSS global. Llamar una sola vez al inicio de app.py."""
    st.markdown(_CSS, unsafe_allow_html=True)

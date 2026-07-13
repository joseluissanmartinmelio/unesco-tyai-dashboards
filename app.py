# app.py
# ── Punto de entrada ──────────────────────────────────────────────────────────
# Solo orquesta: inicializa, lee controles, itera datasets.
# La lógica vive en los módulos específicos.

import streamlit as st

from src.config     import DATASETS, REGIONS
from src.styles     import inject_styles
from src.data       import load_from_meta, compute_series, get_region_col
from src.components import render_header, render_sidebar, render_index_section, render_footer

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="La integridad pública de Chile en perspectiva comparada",
    page_icon="",
    layout="wide",
)

# ── Estilos ───────────────────────────────────────────────────────────────────
inject_styles()

# ── Sidebar → controles ───────────────────────────────────────────────────────
# Las regiones disponibles se derivan de lo que todos los datasets declaran,
# preservando el orden de REGIONS (que es la fuente de verdad).
available_regions = [
    key for key in REGIONS
    if all(key in meta["regions"] for meta in DATASETS.values())
]

region_key, year_range = render_sidebar(available_regions)

region_col   = REGIONS[region_key]          # nombre de columna dummy, ej. "ocde"
region_label = region_key                   # label legible, ej. "OCDE"

# ── Header ────────────────────────────────────────────────────────────────────
render_header(region_label, year_range)

# ── Loop principal ────────────────────────────────────────────────────────────
for idx_name, meta in DATASETS.items():
    try:
        df = load_from_meta(meta)
    except FileNotFoundError:
        st.warning(f"⚠️ Archivo no encontrado: `{meta['file']}`")
        continue
    except Exception as e:
        st.error(f"Error cargando `{meta['file']}`: {e}")
        continue

    try:
        region_col_idx = get_region_col(meta, region_key)
    except KeyError as e:
        st.warning(str(e))
        continue

    series = compute_series(
        _df         = df,
        score_var   = meta["score_var"],
        time_var    = meta["time_var"],
        country_var = meta["country_var"],
        region_col  = region_col_idx,
        year_min    = year_range[0],
        year_max    = year_range[1],
    )

    if series["chile"].empty and series["region_mean"].empty:
        st.info(f"{idx_name}: sin datos para el período seleccionado.")
        continue

    render_index_section(idx_name, meta, series, region_label)

# ── Footer ────────────────────────────────────────────────────────────────────
render_footer()

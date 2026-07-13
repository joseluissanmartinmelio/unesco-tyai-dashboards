# data.py
# ── Carga y transformación de datos ──────────────────────────────────────────
# Dos responsabilidades únicas:
#   1. load_dataset  → lee el CSV y normaliza tipos
#   2. compute_series → filtra y agrega las tres series que necesita el chart
# Ambas funciones son cacheadas por Streamlit.

import os
import pandas as pd
import streamlit as st

from src.config import DATA_PATH


# ── Helpers ───────────────────────────────────────────────────────────────────

def get_region_col(meta: dict, region_key: str) -> str:
    """Devuelve el nombre de columna dummy para la región solicitada.

    Si el dataset no declara esa región, lanza KeyError con mensaje claro,
    lo que hace fácil detectar CSVs incompletos al agregar regiones nuevas.
    """
    try:
        return meta["regions"][region_key]
    except KeyError:
        raise KeyError(
            f"Región '{region_key}' no declarada para el índice "
            f"'{meta.get('file', '?')}'. Revisar config.py."
        )


# ── Carga ─────────────────────────────────────────────────────────────────────

@st.cache_data(show_spinner=False)
def load_dataset(file: str, score_var: str, time_var: str,
                 ocde_col: str, latam_col: str) -> pd.DataFrame:
    """Lee el CSV y normaliza columnas numéricas.

    Recibe parámetros escalares (no el dict completo) para que
    Streamlit pueda hashearlos correctamente y la caché sea efectiva.
    """
    path = os.path.join(DATA_PATH, file)
    df = pd.read_csv(path)
    df.columns = df.columns.str.strip()

    for col in [time_var, score_var, ocde_col, latam_col]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=[time_var, score_var])
    df[time_var] = df[time_var].astype(int)
    return df


def load_from_meta(meta: dict) -> pd.DataFrame:
    """Wrapper conveniente: extrae los parámetros del dict y llama load_dataset."""
    # Recoge todas las columnas de región declaradas para este dataset
    region_cols = list(meta["regions"].values())
    ocde_col  = region_cols[0] if len(region_cols) > 0 else ""
    latam_col = region_cols[1] if len(region_cols) > 1 else ""

    return load_dataset(
        file       = meta["file"],
        score_var  = meta["score_var"],
        time_var   = meta["time_var"],
        ocde_col   = ocde_col,
        latam_col  = latam_col,
    )


# ── Transformación ────────────────────────────────────────────────────────────

@st.cache_data(show_spinner=False)
def compute_series(
    _df: pd.DataFrame,          # prefijo _ para que Streamlit no lo hashee
    score_var:   str,
    time_var:    str,
    country_var: str,
    region_col:  str,
    year_min:    int,
    year_max:    int,
) -> dict[str, pd.DataFrame]:
    """Filtra el DataFrame y devuelve las tres series del chart.

    Returns:
        {
            "chile":       DataFrame con columnas [time_var, score_var]
            "region_mean": DataFrame con columnas [time_var, score_var]
            "region_band": DataFrame con columnas [time_var, "min", "max"]
        }
    """
    df_f = _df[(_df[time_var] >= year_min) & (_df[time_var] <= year_max)]

    chile = (
        df_f[df_f[country_var] == "Chile"]
        .groupby(time_var)[score_var]
        .mean()
        .reset_index()
        .sort_values(time_var)
    )

    region_mask = (df_f[region_col] == 1) & (df_f[country_var] != "Chile")

    region_mean = (
        df_f[region_mask]
        .groupby(time_var)[score_var]
        .mean()
        .reset_index()
        .sort_values(time_var)
    )

    region_band = (
        df_f[region_mask]
        .groupby(time_var)[score_var]
        .agg(["min", "max"])
        .reset_index()
        .sort_values(time_var)
    )

    return {
        "chile":       chile,
        "region_mean": region_mean,
        "region_band": region_band,
    }

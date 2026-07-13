#TODO: datos de VDEM y TRACE
# config.py
# ── Configuración central del dashboard ──────────────────────────────────────
# Agregar índices, regiones o cambiar paths aquí. No tocar lógica.

import os

# ── Paths ─────────────────────────────────────────────────────────────────────
DATA_PATH = "data"

# ── Colores ───────────────────────────────────────────────────────────────────
COLORS = {
    "chile":    "#2563a8",
    "region":   "#93c5e8",
    "grid":     "#f0f4f8",
    "positive": "#16a34a",
    "negative": "#dc2626",
}

# ── Regiones disponibles ──────────────────────────────────────────────────────
# Clave: label que ve el usuario → valor: nombre de la columna dummy en los CSVs
# Para agregar "Top 1%": añadir "Top 1%": "top1" acá y asegurar
# que la columna exista en cada CSV.
REGIONS: dict[str, str] = {
    "OCDE":  "ocde",
    "LATAM": "latam",
}

# ── Registro de datasets ──────────────────────────────────────────────────────
# Cada entrada declara qué columnas usar y cómo interpretar el score.
# Para agregar un índice nuevo: copiar un bloque y ajustar los valores.
# La clave "regions" mapea los labels de REGIONS a la columna dummy del CSV;
# si un CSV usa nombres distintos de columna, se declara aquí por índice.
DATASETS: dict[str, dict] = {
    "CPI – Percepción de Corrupción": {
        "file":             "cpi.csv",
        "score_var":        "CPI_score",
        "time_var":         "Year",
        "country_var":      "country",
        "regions":          {"OCDE": "ocde", "LATAM": "latam"},
        "higher_is_better": True,
        "scale":            "0–100 (mayor = menos corrupto)",
    },
    "OBS – Open Budget Survey": {
        "file":             "obs.csv",
        "score_var":        "OBI_unrounded",
        "time_var":         "Year",
        "country_var":      "country",
        "regions":          {"OCDE": "ocde", "LATAM": "latam"},
        "higher_is_better": True,
        "scale":            "0–100 (mayor = más transparente)",
    },
    
    #"TBRM – TRACE Bribery Risk Matrix": {
    #    "file":             "tbrm.csv",
    #    "score_var":        "Total Score",
    #    "time_var":         "year",
    #    "country_var":      "country",
    #    "regions":          {"OCDE": "ocde", "LATAM": "latam"},
    #    "higher_is_better": False,
    #    "scale":            "0–100 (menor = menos riesgo)",
    #},
    
    #"V-DEM – Political Corruption Index": {
    #    "file":             "vdem-pci.csv",
    #    "score_var":        "v2x_corr",          # ajustar si la columna difiere
    #    "time_var":         "year",
    #    "country_var":      "country",
    #    "regions":          {"OCDE": "ocde", "LATAM": "latam"},
    #    "higher_is_better": False,
    #    "scale":            "0–1 (menor = menos corrupto)",
    #},
    "WGI-CC – Control of Corruption": {
        "file":             "wgicc.csv",
        "score_var":        "value",
        "time_var":         "year",
        "country_var":      "country",
        "regions":          {"OCDE": "ocde", "LATAM": "latam"},
        "higher_is_better": True,
        "scale":            "-2.5 a 2.5 (mayor = mejor)",
    },
    "WJP – Rule of Law Index": {
        "file":             "wjprol.csv",
        "score_var":        "WJP_Rule_of_Law_Index_Overall_Score",
        "time_var":         "Year",
        "country_var":      "country",
        "regions":          {"OCDE": "ocde", "LATAM": "latam"},
        "higher_is_better": True,
        "scale":            "0–1 (mayor = mejor)",
    },
}

# ── Parámetros de UI ──────────────────────────────────────────────────────────
YEAR_MIN     = 2000
YEAR_MAX     = 2025
YEAR_DEFAULT = (2005, 2023)

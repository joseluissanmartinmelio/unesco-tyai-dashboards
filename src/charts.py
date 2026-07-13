# charts.py
# ── Construcción de figuras Plotly ────────────────────────────────────────────
# Una sola función pública: build_index_figure()
# No importa streamlit; devuelve go.Figure puro → testeable y reutilizable.

import pandas as pd
import plotly.graph_objects as go

from src.config import COLORS


def build_index_figure(
    series:       dict[str, pd.DataFrame],
    time_var:     str,
    score_var:    str,
    region_label: str,
) -> go.Figure:
    """Construye el line chart de un índice.

    Args:
        series:       dict con claves "chile", "region_mean", "region_band"
        time_var:     nombre de la columna temporal
        score_var:    nombre de la columna de score
        region_label: label legible de la región (ej. "OCDE")

    Returns:
        go.Figure lista para st.plotly_chart()
    """
    chile       = series["chile"]
    region_mean = series["region_mean"]
    region_band = series["region_band"]

    fig = go.Figure()

    # Banda min/max de la región
    if not region_band.empty:
        fig.add_trace(go.Scatter(
            x=pd.concat([region_band[time_var], region_band[time_var][::-1]]),
            y=pd.concat([region_band["max"], region_band["min"][::-1]]),
            fill="toself",
            fillcolor="rgba(147,197,232,0.15)",
            line=dict(color="rgba(0,0,0,0)"),
            name=f"Rango {region_label}",
            hoverinfo="skip",
        ))

    # Media regional
    if not region_mean.empty:
        fig.add_trace(go.Scatter(
            x=region_mean[time_var],
            y=region_mean[score_var],
            mode="lines",
            name=f"Promedio {region_label}",
            line=dict(color=COLORS["region"], width=2, dash="dot"),
            hovertemplate=f"%{{x}}: %{{y:.2f}} ({region_label})<extra></extra>",
        ))

    # Chile
    if not chile.empty:
        fig.add_trace(go.Scatter(
            x=chile[time_var],
            y=chile[score_var],
            mode="lines+markers",
            name="Chile",
            line=dict(color=COLORS["chile"], width=2.5),
            marker=dict(size=5, color=COLORS["chile"]),
            hovertemplate="%{x}: %{y:.2f} (Chile)<extra></extra>",
        ))

    fig.update_layout(
        height=220,
        margin=dict(l=0, r=10, t=10, b=30),
        paper_bgcolor="white",
        plot_bgcolor="white",
        legend=dict(
            orientation="h",
            yanchor="bottom", y=1.02,
            xanchor="right",  x=1,
            font=dict(size=11),
        ),
        xaxis=dict(
            showgrid=True,
            gridcolor=COLORS["grid"],
            tickfont=dict(size=10),
            dtick=2,
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor=COLORS["grid"],
            tickfont=dict(size=10),
            zeroline=False,
        ),
        hovermode="x unified",
        font=dict(family="Inter, sans-serif"),
    )

    return fig

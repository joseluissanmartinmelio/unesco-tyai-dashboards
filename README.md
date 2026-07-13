# Dashboard · Chile en perspectiva comparada

Comparación de índices de gobernanza y corrupción entre Chile y una región de referencia (OCDE, LATAM, u otras que se agreguen). Desplegado en Streamlit Community Cloud.

---

## Estructura de módulos

```
src/
├── app.py          # Punto de entrada
├── config.py       # Registro de datasets y constantes
├── data.py         # Carga y transformación de datos
├── charts.py       # Construcción de figuras Plotly
├── components.py   # Componentes de UI (HTML + Streamlit)
└── styles.py       # CSS global
```

---

## Qué hace cada módulo y cuándo editarlo

### `config.py`
Configuración central: el registro de datasets, los colores, las regiones disponibles y los parámetros del slider de años.

**Editar cuando quieras:**
- Agregar un índice nuevo → agregar una entrada a `DATASETS`
- Agregar una región nueva (ej. "Top 1%") → agregar una clave a `REGIONS` y la columna dummy correspondiente en cada entrada de `DATASETS`
- Cambiar los colores de Chile o de la región → editar `COLORS`
- Ajustar el rango de años por defecto → editar `YEAR_MIN`, `YEAR_MAX`, `YEAR_DEFAULT`

### `data.py`
Carga los CSVs y calcula las tres series que usa cada chart (Chile, media regional, banda min/max). Ambas funciones están cacheadas con `@st.cache_data`.

**Editar cuando quieras:**
- Cambiar cómo se normalizan las columnas al leer un CSV (ej. parseo de fechas, renombres)
- Cambiar la lógica de agregación (ej. mediana en vez de media)
- Agregar una lógica de filtrado especial para una región nueva que no sea una dummy `0/1`

### `charts.py`
Construye y devuelve un `go.Figure` de Plotly. No importa Streamlit: la figura es un objeto puro.

**Editar cuando quieras:**
- Cambiar el tipo de chart (ej. barras, área)
- Agregar anotaciones, líneas de referencia o eventos históricos al gráfico
- Cambiar el estilo visual de las líneas (grosor, dash, markers)
- Ajustar el layout del chart (altura, márgenes, leyenda)

### `components.py`
Funciones que renderizan bloques de UI en Streamlit: header, sidebar, metric cards, sección por índice, footer.

**Editar cuando quieras:**
- Cambiar el copy o estructura del header o footer
- Agregar un tercer tipo de metric card
- Cambiar cómo se calcula o muestra la diferencia Chile vs región
- Agregar un nuevo control al sidebar

### `styles.py`
Todo el CSS en un solo lugar. `inject_styles()` lo inyecta una vez al inicio de `app.py`.

**Editar cuando quieras:**
- Cambiar tipografía o importar otra fuente de Google Fonts
- Ajustar el gradiente del header
- Cambiar el radio de bordes, sombras o espaciado de las cards
- Agregar estilos para un nuevo componente HTML

---

## Agregar un índice nuevo (flujo típico)

1. Poner el CSV en `data/`
2. Agregar una entrada a `DATASETS` en `config.py`:

```python
"Nombre – Descripción": {
    "file":             "nombre.csv",
    "score_var":        "columna_score",
    "time_var":         "columna_año",
    "country_var":      "country",
    "regions":          {"OCDE": "ocde", "LATAM": "latam"},
    "higher_is_better": True,
    "scale":            "descripción de escala",
},
```

3. Listo. El loop en `app.py` lo recoge automáticamente.

---

## Agregar una región nueva (ej. "Top 1%")

1. Agregar la columna dummy `top1` (0/1) a cada CSV
2. En `config.py`:
   - Agregar `"Top 1%": "top1"` a `REGIONS`
   - Agregar `"Top 1%": "top1"` al dict `regions` de cada dataset en `DATASETS`
3. El selectbox del sidebar la mostrará automáticamente.

---

## Stack

- [Streamlit](https://streamlit.io/) — UI y deploy
- [Plotly](https://plotly.com/python/) — charts interactivos
- [Pandas](https://pandas.pydata.org/) — transformación de datos
- [UptimeRobot](https://uptimerobot.com/) — ping cada 10 min para evitar sleep en Streamlit Community Cloud

GitHub (código + CSV)
    ↓
Streamlit Community Cloud (deploy)
    ↓
UptimeRobot (ping cada 10 min para que no duerma)

---

comparaciones:

1. nivel general (con el top 1%) de momento no implementado
2. nivel latam
3. nivel europa occidental

---

Year = 2013 es 2012-2013
Year = 2018 es 2017-2018

---

## estructura

1. Un dashboard
2. con selectores:
    1. [region]: puede ser ocde, latam o 1% de mayores del ranking
    2. [año]: selecciona los años posibles
3. el dashborad muestra la comparación de "Chile" frente a la [region] y al [año] para todos los indicadores, 6 indicadores:
    1. cpi.csv = Percepction Corruption Index
    2. obs.csv = Open Budget Survey
    3. tbrm.csv = TRACE Bribery Risk Matrix
    4. vdem-pci.csv = V-DEM Political Corruption Index
    5. wgicc.csv = Control of Corruption
    6. wjprol.csv = Rule of Law Index
4. Las variables de interés son:

| name | dataset | time_var | score_var | country_var | ocde_var | latam_var |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| cpi | Percepction Corruption Index | CPI_score | Year | country | ocde | latam |
| obs | Open Budget Survey | OBI_unrounded | Year | country | ocde | latam |
| tbrm | TRACE Bribery Risk Matrix | Total Score | year | country | ocde | latam |
| vdem-pci | V-DEM Political Corruption Index | | | country | ocde | latam |
| wgicc | Control of Corruption | value | year | country | ocde | latam |
| wjprol | Rule of Law Index | WJP_Rule_of_Law_Index_Overall_Score | Year | country | ocde | latam |

5. Cada variable ocde y latam lo que mide es una indicadora de 1 si es ocde 0 sino, y asi.
6. Colores azules con blanco
7. Datos en: ./data
8. Estructura de carpetas:

UNESCO-TYAI-DASHBOARDS/
├── .venv/
├── data/
│   ├── .Rhistory
│   ├── cpi.csv
│   ├── obs.csv
│   ├── tbrm.csv
│   ├── vdem-pci.csv
│   ├── vdemcodebook.pdf
│   ├── wgicc.csv
│   └── wjprol.csv
├── docs/
│   ├── data_name_vars.xlsx
│   └── paises_regiones.xlsx
├── scripts/
│   └── indicator_region_function.R
├── src/
├── .gitignore
├── app.py
├── internal_docs.md
└── requirements.txt
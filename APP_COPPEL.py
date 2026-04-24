import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

st.set_page_config(
    page_title="AFORE COPPEL",
    page_icon="LOGO.jpg",
    layout="wide"
)

# ── Grid uniforme ─────────────────────────────────────────────────────────────
GRID_COLOR = "rgba(0,0,0,.25)"
GRID_WIDTH  = 1.10

# ── Tamaños de fuente uniformes ───────────────────────────────────────────────
FS_TITLE  = 32   # títulos de gráfica
FS_AXIS   = 22   # etiquetas de ejes (xlabel / ylabel)
FS_TICK   = 20   # valores de los ejes
FS_LEGEND = 20   # leyenda
FS_HOVER  = 14   # hover
FS_ANNOT  = 18   # anotaciones

# ── Título e imagen ───────────────────────────────────────────────────────────
st.title("¿PUEDE COPPEL SER EL AFORE #1 CON APORTACIONES VOLUNTARIAS?")

col1, col2, col3 = st.columns([10, 10, 10])
with col2:
    st.image("COPPEL PANEL.jpg", width=1500)

st.markdown("""
<div style="font-size:25px; line-height:1.5; color:#1a1a1a; text-align:justify;">
  <p>
    Grupo Coppel es una empresa mexicana con más de ocho décadas de trayectoria, fundada en
    <b>1941</b> en <b>Culiacán, Sinaloa</b>, por Luis Coppel Rivas y su hijo Enrique Coppel Tamayo.
    A lo largo del tiempo, el grupo evolucionó de un modelo centrado en el comercio minorista
    hacia una estructura empresarial integrada por tres segmentos estratégicos complementarios:
    tiendas, banco y afore. <b>Afore Coppel</b>, creada en <b>2005</b>,
    y <b>BanCoppel</b> en <b>2007</b>, consolidando así un grupo con presencia transversal
    en el sector retail y en el sistema financiero mexicano.
  </p>
  <p>
    El presente proyecto se enfoca en el segmento de <b>Afore Coppel</b>. Con más de
    <b>11.9 millones de cuentas</b> bajo administración, Afore Coppel se posiciona como
    uno de los actores de mayor relevancia dentro del <b>Sistema de Ahorro para el Retiro (SAR) en México.</b>
  </p>
</div>
""", unsafe_allow_html=True)

st.divider()

# ── Carga de datos ────────────────────────────────────────────────────────────
@st.cache_data
def cargar_datos():
    hoja = pd.read_excel("consar.xlsx", sheet_name=None)

    hoja["05_cuentas"].drop(columns=["total_cuentas_administradas_sar"], inplace=True)
    hoja["05_cuentas"] = hoja["05_cuentas"][[
        "fecha", "afore",
        "trabajadores_registrados",
        "trabajadores_asignados_recursos_depositados_siefores",
        "trabajadores_asignados_recursos_depositados_banco_mexico"
    ]]

    df_cuentas = hoja["05_cuentas"].copy().fillna(0)
    df_cuentas["total_cuentas_administradas_afores"] = (
        df_cuentas["trabajadores_registrados"] +
        df_cuentas["trabajadores_asignados_recursos_depositados_siefores"] +
        df_cuentas["trabajadores_asignados_recursos_depositados_banco_mexico"]
    )

    df_tabla = (
        df_cuentas.groupby("afore")[[
            "trabajadores_registrados",
            "trabajadores_asignados_recursos_depositados_siefores",
            "trabajadores_asignados_recursos_depositados_banco_mexico",
            "total_cuentas_administradas_afores"
        ]].last().reset_index()
        .sort_values("trabajadores_registrados", ascending=False)
    )

    afores_validas = df_tabla[df_tabla["trabajadores_registrados"] > 0]["afore"].tolist()

    df_tabla.columns = [
        "Afore", "Trabajadores Registrados",
        "trabajadores_asignados_recursos_depositados_siefores",
        "Con recursos Depositados en Banco de México",
        "Total de Cuentas Administradas por las Afores"
    ]
    df_tabla = df_tabla[df_tabla["Trabajadores Registrados"] > 0]

    df_evolucion = df_cuentas[df_cuentas["afore"].isin(afores_validas)].copy()
    df_evolucion = df_evolucion[df_evolucion["total_cuentas_administradas_afores"] > 0]

    return df_tabla, df_evolucion, hoja

df_tabla, df_evolucion, hoja = cargar_datos()


# ── MAPA ──────────────────────────────────────────────────────────────────────

st.markdown("""
<div style="font-size:25px; line-height:1.5; color:#1a1a1a; text-align:justify;">
  <p>
    <b>Afore Coppel</b> se posiciona en el <b>segundo lugar a nivel nacional</b> en número de sucursales dentro del sector AFORE en México, siendo superada únicamente por <b>Afore Azteca</b>. La ventaja competitiva de ambas instituciones frente al resto radica en su <b>modelo de negocio integral</b>, al combinar tienda departamental, banco y AFORE en un mismo ecosistema. Esto les permite tener mayor alcance y cercanía con los clientes al ubicar sus módulos dentro de sus propias tiendas.
    <br><br>
    Los números reflejan una diferencia significativa entre las dos principales AFORE y el resto del mercado:
    <br><br>
    • <b>Afore Azteca:</b> 1,695 sucursales<br>
    • <b>Afore Coppel:</b> 1,176 sucursales<br>
    • <b>XXI Banorte:</b> 174 sucursales<br>
    • <b>Inbursa:</b> 134 sucursales<br>
    • <b>Invercap:</b> 81 sucursales<br>
    • <b>Banamex:</b> 68 sucursales<br>
    • <b>PensionISSSTE:</b> 50 sucursales<br>
    • <b>Profuturo:</b> 48 sucursales<br>
    • <b>Principal:</b> 38 sucursales<br>
    • <b>SURA:</b> 25 sucursales
  </p>
</div>
""", unsafe_allow_html=True)


@st.cache_data
def cargar_sucursales():
    return pd.read_csv("SUCURSALES.csv", encoding="latin-1")

sucursales = cargar_sucursales()
colores_afore = {
    "CITIBANAMEX":   "#1F4E96",
    "INBURSA":       "#00BFFF",
    "PRINCIPAL":     "#FF0000",
    "PROFUTURO":     "#FFB6C1",
    "SURA":          "#00CED1",
    "XXI BANORTE":   "#00CC00",
    "AZTECA":        "#FFA500",
    "INVERCAP":      "#FFD700",
    "COPPEL":        "#6A0DAD",
    "PENSIONISSSTE": "#C0C0C0",
}

fig1 = px.scatter_mapbox(
    sucursales,
    lat="Latitud", lon="Longitud",
    color="razon social",
    color_discrete_map=colores_afore,
    hover_name="razon social",
    hover_data={"Entidad federativa": True, "Latitud": False, "Longitud": False},
    zoom=3,
    center={"lat": 23.6345, "lon": -102.5528},
)
fig1.update_traces(marker=dict(size=7.5))
fig1.update_layout(
    mapbox=dict(
        style="carto-positron",
        center={"lat": 23.6345, "lon": -102.5528},
        zoom=4.4,
    ),
    hoverlabel=dict(font_size=FS_HOVER, font_family="Arial", namelength=-1),
    title=dict(
        text="<b>SUCURSALES DE AFORES EN MEXICO</b><br><sup>CONSAR</sup>",
        font=dict(size=FS_TITLE, color="#1a1a1a"),
        x=0.5, xanchor="center",
    ),
    legend=dict(
        title=dict(text="AFORE", font=dict(size=FS_LEGEND)),
        font=dict(size=FS_LEGEND),
        bordercolor="lightgray", borderwidth=1,
        itemsizing="constant", itemwidth=30,
    ),
    font=dict(size=FS_TICK, color="#1a1a1a"),
    height=750,
    margin={"r": 0, "t": 80, "l": 0, "b": 0},
)
st.plotly_chart(fig1)
st.divider()

# ── CUENTAS ADMINISTRADAS — barra horizontal ──────────────────────────────────
st.markdown("""
<div style="font-size:25px; line-height:1.5; color:#1a1a1a; text-align:justify;">
  <p>
    El <b>Sistema de Ahorro para el Retiro (SAR)</b> administra actualmente más de <b>69 millones de cuentas</b> en México. Dentro de este mercado, <b>Afore Azteca</b>, <b>Afore Coppel</b> y <b>Banamex</b> se posicionan en los <b>tres primeros lugares</b> en número de cuentas administradas.
    <br><br>
    Sin embargo, el liderazgo de <b>Afore Azteca</b> se explica en gran parte porque concentra aproximadamente <b>9.29 millones de cuentas no registradas o asignadas</b>, derivadas de procesos de licitación y administración de cuentas no plenamente identificadas. Si se excluyeran estas cuentas, <b>Afore Coppel</b> pasaría al <b>primer lugar</b> en cuentas registradas, con cerca de <b>12 millones</b>
    <br><br>
    Esto refleja que el liderazgo de Azteca en cuentas totales responde más a una <b>ventaja administrativa y de licitación</b>, mientras que Coppel mantiene una mayor captación de clientes con cuentas activamente registradas.
  </p>
</div>
""", unsafe_allow_html=True)

promedio = df_tabla["Total de Cuentas Administradas por las Afores"].mean()

fig2 = px.bar(
    df_tabla,
    x="Total de Cuentas Administradas por las Afores",
    y="Afore",
    orientation="h",
    labels={"Afore": "AFORE", "Total de Cuentas Administradas por las Afores": "Total de Cuentas"},
)
fig2.add_vline(
    x=promedio, line_dash="dash", line_color="black", line_width=1,
    annotation_text=f"Promedio: {promedio:,.0f}",
    annotation_position="top left",
    annotation_font_size=15, annotation_yshift=20,
)
fig2.update_traces(
    hovertemplate="<b>%{y}</b><br>Total: %{x:,.0f}<extra></extra>",
    marker_color="#1E3FBE",
)
fig2.update_layout(
    template="plotly_white",
    title=dict(
        text="<b>CUENTAS ADMINISTRADAS POR AFORE</b>",
        font=dict(size=FS_TITLE, color="#1a1a1a"),
        x=0.5, xanchor="center",
    ),
    xaxis=dict(
        title=dict(text="Total de Cuentas", font=dict(size=FS_AXIS)),
        tickfont=dict(size=FS_TICK),
        tickformat=",.0f",
        showgrid=True,
        gridcolor=GRID_COLOR,
        gridwidth=GRID_WIDTH,
    ),
    yaxis=dict(
        title=dict(text="AFORE", font=dict(size=FS_AXIS)),
        tickfont=dict(size=FS_TICK),
        showgrid=False,
        categoryorder="total ascending",
        type="category",
        automargin=True,
    ),
    hoverlabel=dict(font_size=FS_HOVER),
    bargap=0.3,
    showlegend=False,
    margin=dict(t=120, b=80, l=120, r=40),
    height=750,
)
st.plotly_chart(fig2)
st.divider()

# ── EVOLUCIÓN CUENTAS — línea ─────────────────────────────────────────────────
st.markdown("""
<div style="font-size:25px; line-height:1.5; color:#1a1a1a; text-align:justify;">
  <p>
    Se observa que <b>Afore Coppel</b> ha mantenido una <b>evolución gradual y constante</b> en el número de cuentas administradas, posicionándose actualmente en el <b>segundo lugar</b> dentro del sector.
    <br><br>
    También se identifica el primer crecimiento importante de <b>Afore XXI Banorte</b> en <b>noviembre de 2011</b>, impulsado por la primera licitación de cuentas realizada por la <b>CONSAR</b>, mientras que <b>Afore Azteca</b> fortaleció su posición al ganar la segunda licitación en años posteriores.
    <br><br>
    Asimismo, se aprecia una caída generalizada en <b>agosto de 2024</b> en todas las AFORE, atribuida a la salida de la <b>SIEFORE 55-59</b>, correspondiente a personas que alcanzaron la edad de jubilación de <b>65 años</b>.
    <br><br>
    La caída más pronunciada en <b>Afore Coppel</b> revela un insight clave: esta administradora concentraba una mayor proporción de cuentas pertenecientes al segmento de clientes nacidos entre <b>1955 y 1959</b>.
    <br><br>
    Esto plantea una pregunta estratégica: <b>¿Cómo está distribuida la edad de las cuentas administradas en Afore Coppel?</b> Analizar esta información puede ayudar a diseñar <b>campañas de marketing más asertivas</b> y estrategias de retención o captación por segmento generacional.
  </p>
</div>
""", unsafe_allow_html=True)



fig3 = px.line(
    df_evolucion,
    x="fecha",
    y="total_cuentas_administradas_afores",
    color="afore",
    markers=False,
    labels={
        "fecha": "Fecha",
        "total_cuentas_administradas_afores": "Total Cuentas Administradas",
        "afore": "AFORE",
    },
)
fig3.update_traces(
    line=dict(width=2),
    hovertemplate="<b>%{fullData.name}</b><br>Fecha: %{x}<br>Total: %{y:,.0f}<extra></extra>",
)
fig3.update_layout(
    template="plotly_white",
    title=dict(
        text="<b>EVOLUCIÓN DE CUENTAS ADMINISTRADAS POR AFORE</b>",
        font=dict(size=32, color="#1a1a1a"),
        x=0.5, xanchor="center",
    ),
    xaxis=dict(
        title=dict(text="Fecha", font=dict(size=22)),
        tickfont=dict(size=20),
        showgrid=False,
    ),
    yaxis=dict(
        title=dict(text="Total Cuentas Administradas", font=dict(size=22)),
        tickfont=dict(size=20),
        tickformat=",.0f",
        rangemode="nonnegative",
        showgrid=True,
        gridcolor=GRID_COLOR,
        gridwidth=GRID_WIDTH,
    ),
    legend=dict(
        title=dict(text="AFORE", font=dict(size=25)),
        font=dict(size=14),
        bordercolor="lightgray", borderwidth=1,
    ),
    hoverlabel=dict(font_size=14),
    hovermode="closest",
    height=750,
)
st.plotly_chart(fig3)
st.divider()

# ── ESTADO DE SITUACIÓN FINANCIERA ───────────────────────────────────────────
@st.cache_data
def cargar_estados_financieros():
    esf = pd.read_csv("ESF.csv", encoding="utf-8-sig")
    bg  = pd.read_csv("BG.csv",  encoding="utf-8-sig")
    return esf, bg

esf, bg = cargar_estados_financieros()

if "slide_idx" not in st.session_state:
    st.session_state.slide_idx = 0

# ── FIG4 — ESTADO DE RESULTADOS ───────────────────────────────────────────────
estado = esf.copy()
estado['enero'] = pd.to_numeric(estado['enero'], errors='coerce')
estado = estado[['concepto', 'enero']].rename(columns={'enero': 'CANTIDAD'})
estado['concepto'] = estado['concepto'].str.strip()

orden_correcto = [
    'Ingresos por comisión',
    'Costos de operación',
    'Utilidad de operación',
    'Gastos generales de administración',
    'Utilidad bruta',
    'Otros ingresos y gastos (neto)',
    'Utilidad (perdida) antes de impuestos a la utilidad',
    'Impuesto a la utilidad',
    'Utilidad (Perdida) neta',
]
estado = estado.set_index('concepto').loc[orden_correcto].reset_index()

costos = ['Costos de operación', 'Gastos generales de administración', 'Impuesto a la utilidad']
estado.loc[estado['concepto'].isin(costos), 'CANTIDAD'] *= -1

measure = ['absolute','relative','total','relative','total','relative','total','relative','total']

fig4 = go.Figure(go.Waterfall(
    name='Coppel',
    orientation='v',
    measure=measure,
    x=estado['concepto'],
    y=estado['CANTIDAD'],
    text=estado['CANTIDAD'].apply(lambda x: f'${abs(x):,.0f}'),
    textposition='outside',
    textfont=dict(size=FS_TICK),
    connector=dict(line=dict(color='#AAAAAA', width=1)),
    increasing=dict(marker=dict(color='#F5C800')),
    decreasing=dict(marker=dict(color='#e91e8c')),
    totals=dict(marker=dict(color='#1E3FBE'))
))
fig4.update_layout(
    template='plotly_white',
    title=dict(
        text="<b>ESTADO DE RESULTADOS — COPPEL — ENERO</b>",
        font=dict(size=FS_TITLE, color="#1a1a1a"),
        x=0.5, xanchor="center",
    ),
    xaxis=dict(
        title=dict(text="Concepto", font=dict(size=FS_AXIS)),
        tickfont=dict(size=FS_TICK),
        tickangle=-25,
    ),
    yaxis=dict(
        title=dict(text="Monto", font=dict(size=FS_AXIS)),
        tickfont=dict(size=FS_TICK),
        tickformat='$,.0f',
        gridcolor='#DDDDDD',
        showgrid=True,
    ),
    hoverlabel=dict(font_size=FS_HOVER),
    font=dict(size=FS_TICK),
    margin=dict(t=100, b=180),
    height=800,
)


# ── FIG5 — BALANCE GENERAL ────────────────────────────────────────────────────
AZUL_COPPEL     = '#003DA5'
AZUL_CLARO      = '#1a5dc8'
AMARILLO_COPPEL = '#FFD100'
AMARILLO_CLARO  = '#ffe566'
GRIS_OSCURO     = '#4a4a4a'
GRIS_CLARO      = '#7a7a7a'

df_bg = bg[bg['afore_nombre'] == 'Coppel'][['concepto', 'enero']].copy()
df_bg['enero'] = pd.to_numeric(df_bg['enero'], errors='coerce').fillna(0)
df_bg = df_bg.rename(columns={'enero': 'valor'}).reset_index(drop=True)

tipo_map = {
    'Activos':                             'total_activo',
    'Activo a Corto Plazo':                'subtotal_activo',
    'Activo a largo plazo e intangibles':  'subtotal_activo',
    'Pasivo':                              'total_pasivo',
    'Pasivo a corto plazo':                'subtotal_pasivo',
    'Pasivo a largo plazo':                'subtotal_pasivo',
    'Capital Contable':                    'total_capital',
    'Capital Contribuido':                 'subtotal_capital',
    'Capital Ganado':                      'subtotal_capital',
}

def asignar_tipo(concepto):
    if concepto in tipo_map:
        return tipo_map[concepto]
    c = concepto.lower()
    if 'activo' in c:   return 'activo'
    elif 'pasivo' in c: return 'pasivo'
    else:               return 'capital'

df_bg['tipo'] = df_bg['concepto'].apply(asignar_tipo)

conceptos_mostrar = [
    'Activos','Activo a Corto Plazo','Efectivo y equivalentes de efectivo',
    'Inversiones en valores','Cuentas por Cobrar',
    'Activo a largo plazo e intangibles','Inversiones permanentes en acciones',
    'Propiedades, Mobiliario y Equipo (Neto)',
    'Pasivo','Pasivo a corto plazo','Cuenta por Pagar y Otros Gastos Acumulados',
    'Impuestos a la utilidad por pagar',
    'Pasivo a largo plazo',
    'Impuestos diferidos',
    'Beneficio a los empleados',
    'Reserva para pensiones del personal',
    'Reserva para primas de antigüedad y beneficios por terminación',  # ← nombre exacto
    'Capital Contable','Capital Contribuido','Capital social pagado',
    'Capital Ganado',
    'Reserva legal',
    'Resultados de ejercicios anteriores',
    'Resultados del ejercicio',
]


df_bg = df_bg[df_bg['concepto'].isin(conceptos_mostrar)].copy()
df_bg = df_bg.set_index('concepto').loc[conceptos_mostrar].reset_index()

sin_barra = {'total_activo','subtotal_activo','total_pasivo','subtotal_pasivo','total_capital','subtotal_capital'}

color_map_bg = {
    'total_activo':    'rgba(0,0,0,0)',
    'subtotal_activo': 'rgba(0,0,0,0)',
    'activo':          AZUL_CLARO,
    'total_pasivo':    'rgba(0,0,0,0)',
    'subtotal_pasivo': 'rgba(0,0,0,0)',
    'pasivo':          AMARILLO_CLARO,
    'total_capital':   'rgba(0,0,0,0)',
    'subtotal_capital':'rgba(0,0,0,0)',
    'capital':         GRIS_CLARO,
}

bases, anchos, running = [], [], 0.0
for _, row in df_bg.iterrows():
    if row['tipo'] in {'total_activo', 'total_pasivo', 'total_capital'}:
        bases.append(0); anchos.append(0); running = 0.0  # ← reinicia en cada sección
    elif row['tipo'] in {'subtotal_activo', 'subtotal_pasivo', 'subtotal_capital'}:
        bases.append(0); anchos.append(0)  # ← no modifica running
    else:
        bases.append(running); anchos.append(row['valor']); running += row['valor']

df_bg['base']  = bases
df_bg['ancho'] = anchos
df_bg['color'] = df_bg['tipo'].map(color_map_bg)

def fmt(v, t):
    if t in sin_barra or v == 0: return ''
    return f"${v/1e6:.2f}M" if v >= 1e6 else f"${v:,.0f}"
df_bg['texto'] = [fmt(r['valor'], r['tipo']) for _, r in df_bg.iterrows()]

def get_valor(concepto):
    row = df_bg[df_bg['concepto'] == concepto]
    return row['valor'].values[0] if not row.empty else 0

fig5_bg = go.Figure()
fig5_bg.add_trace(go.Bar(
    x=df_bg['base'], y=df_bg['concepto'], orientation='h',
    marker=dict(color='rgba(0,0,0,0)'), hoverinfo='skip', showlegend=False
))
fig5_bg.add_trace(go.Bar(
    x=df_bg['ancho'], y=df_bg['concepto'], orientation='h',
    marker=dict(color=df_bg['color'].tolist(), line=dict(color='white', width=0.8)),
    text=df_bg['texto'], textposition='outside',
    textfont=dict(size=FS_TICK, color='#222222'),
    hovertemplate='<b>%{y}</b><br>$%{x:,.0f}<extra></extra>',
    showlegend=False
))
fig5_bg.update_layout(
    barmode='stack',
    template='plotly_white',
    title=dict(
        text='<b>BALANCE GENERAL — COPPEL — ENERO 2024</b><br>'
             f'<span style="font-size:14px;color:#666">en miles de pesos</span>',
        font=dict(size=FS_TITLE, color="#1a1a1a"),
        x=0.5, xanchor='center',
    ),
    plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
    height=800,
    margin=dict(l=300, r=150, t=110, b=70),
    xaxis=dict(
        title=dict(text='Miles de pesos', font=dict(size=FS_AXIS)),
        tickfont=dict(size=FS_TICK),
        tickformat='$,.0f',
        zeroline=True, zerolinecolor='#aaaaaa', zerolinewidth=1.5,
    ),
    yaxis=dict(
        tickfont=dict(size=FS_TICK),
        autorange='reversed',
        categoryorder='array',
        categoryarray=df_bg['concepto'].tolist(),
    ),
    hoverlabel=dict(font_size=FS_HOVER, bgcolor='white', bordercolor='#cccccc'),
    showlegend=False,
)

for label, concepto, color in [
    ('🔵  Activos', 'Activos',          AZUL_COPPEL),
    ('🟡  Pasivos', 'Pasivo',           AMARILLO_COPPEL),
    ('⚫  Capital', 'Capital Contable', GRIS_OSCURO),
]:
    valor = get_valor(concepto)
    total_txt = f"${valor/1e6:.2f}M" if valor >= 1e6 else f"${valor:,.0f}"
    fig5_bg.add_annotation(
        x=0, y=concepto,
        text=f'<b>{label}</b>  <span style="font-size:{FS_TICK}px;color:{color}">({total_txt})</span>',
        showarrow=False, xanchor='right', xshift=-12,
        font=dict(size=FS_LEGEND, color=color, family='Arial'), xref='x', yref='y'
    )

for label, concepto, color in [
    ('Activo CP', 'Activo a Corto Plazo',               AZUL_CLARO),
    ('Activo LP', 'Activo a largo plazo e intangibles',  AZUL_CLARO),
    ('Pasivo CP', 'Pasivo a corto plazo',                AMARILLO_COPPEL),
    ('Pasivo LP', 'Pasivo a largo plazo',                AMARILLO_COPPEL),
]:
    valor = get_valor(concepto)
    total_txt = f"${valor/1e6:.2f}M" if valor >= 1e6 else f"${valor:,.0f}"
    fig5_bg.add_annotation(
        x=0, y=concepto,
        text=f'<i>{label}</i>  <span style="font-size:{FS_TICK-2}px;color:{color}">({total_txt})</span>',
        showarrow=False, xanchor='right', xshift=-12,
        font=dict(size=FS_TICK, color=color, family='Arial'), xref='x', yref='y'
    )

for concepto_sep in ['Pasivo', 'Capital Contable']:
    idx = df_bg[df_bg['concepto'] == concepto_sep].index[0]
    fig5_bg.add_hline(y=idx - 0.5, line=dict(color='#cccccc', width=1.5, dash='dash'))

# ── SLIDES — NAVEGACIÓN ───────────────────────────────────────────────────────
graficas = [
    ("Estado de Resultados", fig4),
    ("Balance General",      fig5_bg),
]

col_prev, col_titulo, col_next = st.columns([1, 4, 1])

with col_prev:
    if st.button("◀ Anterior", disabled=(st.session_state.slide_idx == 0)):
        st.session_state.slide_idx -= 1
        st.rerun()

with col_titulo:
    titulo, _ = graficas[st.session_state.slide_idx]
    st.markdown(
        f"<h4 style='text-align:center'>{titulo} "
        f"({st.session_state.slide_idx + 1}/{len(graficas)})</h4>",
        unsafe_allow_html=True
    )

with col_next:
    if st.button("Siguiente ▶", disabled=(st.session_state.slide_idx == len(graficas) - 1)):
        st.session_state.slide_idx += 1
        st.rerun()

_, fig_activa = graficas[st.session_state.slide_idx]
st.plotly_chart(fig_activa)
st.divider()

# ── RECURSOS POR AFORE — barra horizontal ─────────────────────────────────────
st.markdown("""
<div style="font-size:25px; line-height:1.5; color:#1a1a1a; text-align:justify;">
  <p>
    Los recursos administrados en el <b>Sistema de Ahorro para el Retiro (SAR)</b> superan actualmente los <b>10 billones de pesos</b>. Dentro de este mercado, <b>Afore Coppel</b> se posiciona en el <b>cuarto lugar</b> en recursos administrados; sin embargo, ocupa apenas el <b>décimo lugar</b> en aportaciones voluntarias.
    <br><br>
    Esta diferencia genera una interrogante importante: <b>¿por qué los clientes de Afore Coppel realizan menos aportaciones voluntarias en comparación con otras AFORE?</b>
    <br><br>
    Más adelante se analizarán posibles factores relacionados con el perfil del cliente, la educación financiera y los canales de promoción, para entender este comportamiento.
  </p>
</div>
""", unsafe_allow_html=True)


df_recursos_copia = hoja["09_recursos"][[
    "fecha", "afore",
    "monto_ahorro_voluntario_y_solidario",
    "monto_recursos_registrados_sar",
]]
df_ultimo = df_recursos_copia.sort_values("fecha").groupby("afore").last().reset_index()
df_ultimo["afore"] = df_ultimo["afore"].replace({
    "fondo de pensiones para el bienestar 9": "pensiones bienestar"
})
df_ultimo["monto_ahorro_voluntario_y_solidario"] *= 1000
df_ultimo["monto_recursos_registrados_sar"] *= 1000

orden_afores = (
    df_ultimo.sort_values("monto_recursos_registrados_sar", ascending=False)["afore"].tolist()
)
df_melted = df_ultimo.sort_values("monto_recursos_registrados_sar", ascending=False).melt(
    id_vars="afore",
    value_vars=["monto_ahorro_voluntario_y_solidario", "monto_recursos_registrados_sar"],
    var_name="tipo", value_name="monto",
)
df_melted["tipo"] = df_melted["tipo"].map({
    "monto_ahorro_voluntario_y_solidario": "Ahorro Voluntario y Solidario",
    "monto_recursos_registrados_sar": "Recursos Registrados SAR",
})

fig6_rec = px.bar(
    df_melted,
    x="monto", y="afore", color="tipo",
    barmode="group", orientation="h",
    category_orders={"afore": orden_afores},
    color_discrete_map={
        "Ahorro Voluntario y Solidario": "#F5C800",
        "Recursos Registrados SAR": "#1E3FBE",
    },
    labels={"monto": "Monto (pesos)", "afore": "AFORE", "tipo": ""},
)
fig6_rec.update_traces(
    hovertemplate="<b>%{fullData.name}</b><br>AFORE: %{y}<br>Monto: %{x:,.2f}<extra></extra>"
)
fig6_rec.update_layout(
    template="plotly_white",
    title=dict(
        text="<b>RECURSOS ADMINISTRADOS POR AFORE</b>",
        font=dict(size=FS_TITLE, color="#1a1a1a"),
        x=0.5, xanchor="center",
    ),
    xaxis=dict(
        title=dict(text="Recursos Administrados (pesos)", font=dict(size=FS_AXIS)),
        tickfont=dict(size=FS_TICK),
        tickformat=",.0f",
        showgrid=True,
        gridcolor=GRID_COLOR,
        gridwidth=GRID_WIDTH,
    ),
    yaxis=dict(
        title=dict(text="AFORE", font=dict(size=FS_AXIS)),
        tickfont=dict(size=FS_TICK),
        showgrid=False,
    ),
    legend=dict(
        font=dict(size=FS_LEGEND),
        bordercolor="lightgray", borderwidth=1,
    ),
    hoverlabel=dict(font_size=FS_HOVER),
    height=750,
)
st.plotly_chart(fig6_rec)
st.divider()

# ── RENDIMIENTO SIEFORES — línea ──────────────────────────────────────────────
st.markdown("""
<div style="font-size:25px; line-height:1.5; color:#1a1a1a; text-align:justify;">
  <p>
    En esta gráfica se observan los <b>rendimientos por SIEFORE generacional</b>, donde cada fondo presenta variaciones debido a sus <b>restricciones de inversión</b>, perfil de riesgo y los instrumentos financieros permitidos para cada generación.
    <br><br>
    Se aprecia cómo cada SIEFORE mantiene un comportamiento distinto según la etapa de vida del trabajador: las generaciones más jóvenes suelen tener mayor exposición a instrumentos de renta variable, mientras que las generaciones próximas al retiro priorizan activos más conservadores.
    <br><br>
    Entre <b>julio y agosto</b>, se observa un cambio importante en la composición del SAR: la <b>SIEFORE 55-59</b> deja de formar parte del sistema debido a la jubilación de ese grupo generacional, mientras que se incorpora la <b>SIEFORE 95-99</b>, correspondiente a personas que comienzan su <b>vida económicamente activa</b>.
  </p>
</div>
""", unsafe_allow_html=True)


hoja["10_rendimientos_precio_bolsa"] = hoja["10_rendimientos_precio_bolsa"][
    hoja["10_rendimientos_precio_bolsa"]["tipo_recurso"] != "sb pensiones promedio ponderado"
]
hoja["10_rendimientos_precio_bolsa"]["plazo"] = (
    hoja["10_rendimientos_precio_bolsa"]["plazo"].replace({"5 aÃ±os": "5 años"})
)

promedios_excluir = [
    "sb 55-59 promedio ponderado", "sb 60-64 promedio ponderado",
    "sb 65-69 promedio ponderado", "sb 70-74 promedio ponderado",
    "sb 75-79 promedio ponderado", "sb 80-84 promedio ponderado",
    "sb 85-89 promedio ponderado", "sb 90-94 promedio ponderado",
    "sb 95-99 promedio ponderado", "sb 1000 promedio ponderado",
]

df_rendimientos = hoja["10_rendimientos_precio_bolsa"].copy()
df_rendimientos = df_rendimientos[
    (df_rendimientos["plazo"] == "5 años") &
    (~df_rendimientos["tipo_recurso"].isin([
        "sb pensiones promedio ponderado", "adicionales promedio ponderado"
    ])) &
    (~df_rendimientos["afore"].isin(promedios_excluir))
]
df_rendimientos["tipo_recurso"] = (
    df_rendimientos["tipo_recurso"]
    .str.replace(" promedio ponderado", "", regex=False)
    .str.strip()
)

datos_rend = df_rendimientos[df_rendimientos["afore"] == "coppel"]

fig6 = px.line(
    datos_rend, x="fecha", y="monto", color="tipo_recurso",
    markers=False,
    labels={"fecha": "Fecha", "monto": "Rendimiento (%)", "tipo_recurso": "SB"},
)
fig6.update_traces(
    line=dict(width=3),
    hovertemplate="<b>%{fullData.name}</b><br>Fecha: %{x}<br>Rendimiento: %{y:.4f}%<extra></extra>",
)
fig6.update_layout(
    template="plotly_white",
    title=dict(
        text="<b>RENDIMIENTO SIEFORES — COPPEL (5 AÑOS)</b>",
        font=dict(size=FS_TITLE, color="#1a1a1a"),
        x=0.5, xanchor="center",
    ),
    xaxis=dict(
        title=dict(text="Fecha", font=dict(size=FS_AXIS)),
        tickfont=dict(size=FS_TICK),
        showgrid=False,
    ),
    yaxis=dict(
        title=dict(text="Rendimiento (%)", font=dict(size=FS_AXIS)),
        tickfont=dict(size=FS_TICK),
        ticksuffix="%",
        showgrid=True,
        gridcolor=GRID_COLOR,
        gridwidth=GRID_WIDTH,
    ),
    legend=dict(
        title=dict(text="SB", font=dict(size=FS_LEGEND)),
        font=dict(size=FS_LEGEND),
        bordercolor="lightgray", borderwidth=1,
    ),
    hoverlabel=dict(font_size=FS_HOVER),
    hovermode="closest",
    height=750,
)
st.plotly_chart(fig6)
st.divider()

# ── TRASPASOS COPPEL — línea ──────────────────────────────────────────────────
st.markdown("""
<div style="font-size:25px; line-height:1.5; color:#1a1a1a; text-align:justify;">
  <p>
    Se puede observar que la entrada de <b>Afore Coppel</b> al mercado fue de manera <b>asertiva y gradual</b>, pasando por una etapa de <b>introducción y desarrollo</b> entre <b>2006</b> y la mayoría temprana, hasta alcanzar su etapa de <b>madurez a finales de 2014</b>.
    <br><br>
    A partir de <b>julio de 2024</b>, se observa una disminución importante en el número de cuentas administradas. Este comportamiento coincide con el impacto indirecto del <b>ciberataque sufrido por Grupo Coppel en abril de 2024</b>, el cual afectó operaciones, servicios y canales digitales durante varios meses.
    <br><br>
    Entre <b>julio y diciembre de 2024</b>, <b>Afore Coppel</b> perdió aproximadamente <b>230 mil cuentas administradas</b>, lo que podría estar relacionado con afectaciones en la atención al cliente, confianza del usuario o retrasos operativos derivados del incidente.
  </p>
</div>
""", unsafe_allow_html=True)



df_traspasos = hoja["08_traspasos"].copy()
df_traspasos["fecha"] = pd.to_datetime(df_traspasos["fecha"], errors="coerce")

datos_trasp = df_traspasos[df_traspasos["afore"] == "coppel"]
datos_melted = datos_trasp.melt(
    id_vars="fecha",
    value_vars=["num_tras_cedido", "num_tras_recibido"],
    var_name="tipo", value_name="cantidad",
)
datos_melted["tipo"] = datos_melted["tipo"].map({
    "num_tras_cedido": "Cedidos",
    "num_tras_recibido": "Recibidos",
})
datos_melted["cantidad"] = datos_melted["cantidad"].replace(0, pd.NA)

fig7 = px.line(
    datos_melted, x="fecha", y="cantidad", color="tipo",
    color_discrete_map={"Cedidos": "red", "Recibidos": "green"},
    labels={"fecha": "Fecha", "cantidad": "Número de Traspasos", "tipo": ""},
)
fig7.update_traces(
    line=dict(width=3),
    marker=dict(size=3),
    connectgaps=True,
    hovertemplate="<b>%{fullData.name}</b><br>Fecha: %{x}<br>Total: %{y:,.0f}<extra></extra>",
)
fig7.update_layout(
    template="plotly_white",
    title=dict(
        text="<b>TRASPASOS CEDIDOS Y RECIBIDOS — COPPEL</b>",
        font=dict(size=FS_TITLE, color="#1a1a1a"),
        x=0.5, xanchor="center",
    ),
    xaxis=dict(
        title=dict(text="Fecha", font=dict(size=FS_AXIS)),
        tickfont=dict(size=FS_TICK),
        range=["2006-01-01", datos_melted["fecha"].max()],
        showgrid=False,
    ),
    yaxis=dict(
        title=dict(text="Número de Traspasos", font=dict(size=FS_AXIS)),
        tickfont=dict(size=FS_TICK),
        tickformat=",.0f",
        showgrid=True,
        gridcolor=GRID_COLOR,
        gridwidth=GRID_WIDTH,
    ),
    legend=dict(
        font=dict(size=FS_LEGEND),
        bordercolor="lightgray", borderwidth=1,
    ),
    hoverlabel=dict(font_size=FS_HOVER),
    hovermode="closest",
    height=750,
)
st.plotly_chart(fig7)
st.divider()

# ── TRASPASOS TODOS LOS AFORES — barra vertical ───────────────────────────────
st.markdown("""
<div style="font-size:25px; line-height:1.5; color:#1a1a1a; text-align:justify;">
  <p>
    El análisis del total de traspasos por AFORE (excluyendo licitaciones) revela que la mayoría de las administradoras presentan un mayor volumen de <b>traspasos cedidos que recibidos</b>, siendo <b>Banamex, Coppel, XXI Banorte, Sura, Profuturo y Principal</b> los casos más representativos de esta tendencia.
    <br><br>
    Sin embargo, destacan como excepciones <b>Azteca</b> e <b>Invercap</b>, quienes registran más <b>traspasos recibidos que cedidos</b>, lo que sugiere una mayor capacidad de atracción de afiliados en el periodo analizado.
    <br><br>
    Por su parte, <b>Inbursa</b> y <b>Pensionissste</b> muestran cifras más equilibradas y de menor volumen en comparación con el resto del sistema.
  </p>
</div>
""", unsafe_allow_html=True)


df_traspasos2 = hoja["08_traspasos"].copy().fillna(0)
df_total = (
    df_traspasos2.groupby("afore")[["num_tras_cedido", "num_tras_recibido"]]
    .sum().reset_index()
    .sort_values("num_tras_cedido", ascending=False)
)
orden_afores2 = df_total["afore"].tolist()

df_melted2 = df_total.melt(
    id_vars="afore",
    value_vars=["num_tras_cedido", "num_tras_recibido"],
    var_name="tipo", value_name="cantidad",
)
df_melted2["tipo"] = df_melted2["tipo"].map({
    "num_tras_cedido": "Cedidos",
    "num_tras_recibido": "Recibidos",
})

fig8 = px.bar(
    df_melted2, x="afore", y="cantidad", color="tipo",
    barmode="group",
    color_discrete_map={"Cedidos": "red", "Recibidos": "green"},
    category_orders={"afore": orden_afores2},
    labels={"afore": "AFORE", "cantidad": "Total Traspasos", "tipo": ""},
)
fig8.update_traces(
    hovertemplate="<b>%{fullData.name}</b><br>AFORE: %{x}<br>Total: %{y:,.0f}<extra></extra>"
)
fig8.update_layout(
    template="plotly_white",
    title=dict(
        text="<b>TOTAL DE TRASPASOS POR AFORE</b>",
        font=dict(size=FS_TITLE, color="#1a1a1a"),
        x=0.5, xanchor="center",
    ),
    xaxis=dict(
        title=dict(text="AFORE", font=dict(size=FS_AXIS)),
        tickfont=dict(size=FS_TICK),
        showgrid=False,
    ),
    yaxis=dict(
        title=dict(text="Total Traspasos", font=dict(size=FS_AXIS)),
        tickfont=dict(size=FS_TICK),
        tickformat=",.0f",
        showgrid=True,
        gridcolor=GRID_COLOR,
        gridwidth=GRID_WIDTH,
    ),
    legend=dict(
        font=dict(size=FS_LEGEND),
        bordercolor="lightgray", borderwidth=1,
    ),
    hoverlabel=dict(font_size=FS_HOVER),
    height=750,
)
st.plotly_chart(fig8)
st.divider()

# ── COMISIONES — línea ────────────────────────────────────────────────────────
st.markdown("""
<div style="font-size:25px; line-height:1.5; color:#1a1a1a; text-align:justify;">
  <p>
    Se observa cómo las <b>comisiones de las AFORE</b> comenzaron un proceso de <b>convergencia gradual</b> entre <b>2012 y 2020</b>, reduciendo sus diferencias año con año.
    <br><br>
    A partir de <b>2022</b>, tras la reforma a la <b>Ley del Sistema de Ahorro para el Retiro</b>, la mayoría de las AFORE adoptaron una comisión prácticamente uniforme de <b>0.57%</b>, como resultado de la regulación impuesta por la <b>CONSAR</b>.
    <br><br>
    La única excepción fue <b>PensionISSSTE</b>, que mantuvo una comisión menor, consolidándose como la administradora con el costo más bajo del mercado.
    <br><br>
    Este cambio transformó la competencia del sector, desplazando el enfoque de las comisiones hacia factores como <b>rendimientos netos</b>, <b>servicio</b> y <b>captación de clientes</b>.
  </p>
</div>
""", unsafe_allow_html=True)


df_comisiones = hoja["06_comisiones"].copy().replace(0, float("nan"))

fig9 = px.line(
    df_comisiones, x="fecha", y="comision", color="afore",
    markers=False,
    labels={"fecha": "Fecha", "comision": "Comisión (%)", "afore": "AFORE"},
)
fig9.update_traces(
    connectgaps=True,
    line=dict(width=3),
    hovertemplate="<b>%{fullData.name}</b><br>Fecha: %{x}<br>Comisión: %{y:.2f}%<extra></extra>",
)
fig9.update_layout(
    template="plotly_white",
    title=dict(
        text="<b>COMISIONES POR AFORE</b>",
        font=dict(size=FS_TITLE, color="#1a1a1a"),
        x=0.5, xanchor="center",
    ),
    xaxis=dict(
        title=dict(text="Fecha", font=dict(size=FS_AXIS)),
        tickfont=dict(size=FS_TICK),
        showgrid=False,
    ),
    yaxis=dict(
        title=dict(text="Comisión (%)", font=dict(size=FS_AXIS)),
        tickfont=dict(size=FS_TICK),
        ticksuffix="%",
        showgrid=True,
        gridcolor=GRID_COLOR,
        gridwidth=GRID_WIDTH,
    ),
    legend=dict(
        title=dict(text="AFORE", font=dict(size=FS_LEGEND)),
        font=dict(size=FS_LEGEND),
        bordercolor="lightgray", borderwidth=1,
    ),
    hoverlabel=dict(font_size=FS_HOVER),
    hovermode="closest",
    height=750,
)
st.plotly_chart(fig9)
st.divider()

# ── GOOGLE TRENDS ─────────────────────────────────────────────────────────────
st.markdown("""
<div style="font-size:25px; line-height:1.5; color:#1a1a1a; text-align:justify;">
  <p>
    En términos de <b>tendencia de búsqueda en Google Trends</b>, <b>Afore Coppel</b> se posiciona en el <b>tercer lugar</b>, únicamente por debajo de <b>XXI Banorte</b> y <b>SURA</b>, reflejando un alto nivel de interés digital por parte de los usuarios.
    <br><br>
    Entre <b>2022 y 2023</b>, <b>Afore Coppel</b> registró su <b>mayor volumen de búsquedas</b>, impulsado principalmente por el uso de su aplicación móvil, la cual alcanzó cerca de <b>2 millones de descargas</b>, convirtiéndose en uno de sus principales canales digitales para consultas, movimientos y aportaciones voluntarias.
    <br><br>
    Sin embargo, despues de <b>2023</b>, la aplicación comenzó a perder relevancia debido a <b>fallas técnicas recurrentes</b>, problemas de acceso y sincronización, además de que la empresa comenzó a redirigir gradualmente a sus usuarios hacia <b>AforeMóvil</b> y <b>AforeWeb</b>.
    <br><br>
     <b>Afore Coppel</b> fue de las últimas administradoras en integrarse completamente a <b>AforeMóvil</b>, lo que pudo haber generado fricción en la experiencia del usuario y afectar temporalmente la adopción digital de sus servicios.
    <br><br>
    Esto genera una nueva incógnita: <b>¿Los usuarios lograron adaptarse y migrar de la app de Afore Coppel hacia AforeMóvil?</b>
    <br><br>
  </p>
</div>
""", unsafe_allow_html=True)


google = pd.read_excel(
    "COPPEL_GOOGLE_TRENDS.xlsx",
    sheet_name=None,
)
GT_COLORS = [
    "#00C8FF", "#FF6B35", "#FFD700", "#B44FFF",
    "#00E676", "#FF4081", "#FF9100", "#64FFDA",
]

def make_trends_fig(df, title, replace_zeros=False, min_year=None):
    df = df.copy()
    if min_year:
        df = df[df["Time"].dt.year >= min_year]
    afores = [c for c in df.columns if c != "Time"]
    if replace_zeros:
        df[afores] = df[afores].replace(0, np.nan)

    fig10 = go.Figure()
    for i, afore in enumerate(afores):
        fig10.add_trace(go.Scatter(
            x=df["Time"], y=df[afore],
            mode="lines",
            name=afore.title(),
            line=dict(color=GT_COLORS[i % len(GT_COLORS)], width=3),
            connectgaps=True,
            hovertemplate=(
                f"<b>{afore.title()}</b><br>"
                "Fecha: %{x|%b %Y}<br>"
                "Índice GT: %{y}<extra></extra>"
            ),
        ))

    fig10.update_layout(
        template="plotly_white",
        title=dict(
            text=f"<b>{title.upper()}</b>",
            font=dict(size=FS_TITLE, color="#1a1a1a"),
            x=0.5, xanchor="center",
        ),
        xaxis=dict(
            title=dict(text="Año", font=dict(size=FS_AXIS)),
            tickfont=dict(size=FS_TICK),
            showgrid=False,
            tickformat="%Y",
            dtick="M12",
            tickangle=-45,
        ),
        yaxis=dict(
            title=dict(text="Índice relativo (0 – 100)", font=dict(size=FS_AXIS)),
            tickfont=dict(size=FS_TICK),
            showgrid=True,
            gridcolor=GRID_COLOR,
            gridwidth=GRID_WIDTH,
            range=[0, 100],
        ),
        legend=dict(
            title=dict(text="AFORE", font=dict(size=FS_LEGEND)),
            font=dict(size=FS_LEGEND),
            bordercolor="lightgray", borderwidth=1,
        ),
        hoverlabel=dict(font_size=FS_HOVER, namelength=-1),
        hovermode="closest",
        margin=dict(t=120, b=100, l=70, r=40),
        height=750,
    )
    return fig10


# ── 2. Luego el selector y las llamadas ───────────────────────
opciones = {
    "Interés de búsqueda en Google Trends — AFOREs": "consultas",
    "Interés de búsqueda en Google Trends — AFOREs Aplicaciones": "afore_app_SAF",
    "Interés de búsqueda en Google Trends — BanCoppel / AforeMovil / Afore Coppel App": "B,AM,ACA",
}

seleccion = st.selectbox("Selecciona la gráfica a mostrar:", list(opciones.keys()))
sheet = opciones[seleccion]

if sheet == "consultas":
    fig10 = make_trends_fig(
        google["consultas"],
        title="Interés de búsqueda en Google Trends — AFOREs",
    )
elif sheet == "afore_app_SAF":
    fig10 = make_trends_fig(
        google["afore_app_SAF"],
        title="Interés de búsqueda en Google Trends — AFOREs Aplicaciones",
        replace_zeros=True,
        min_year=2019,
    )
elif sheet == "B,AM,ACA":
    fig10 = make_trends_fig(
        google["B,AM,ACA"],
        title="Interés de búsqueda en Google Trends — BanCoppel / AforeMovil / Afore Coppel App",
        min_year=2019,
    )

st.plotly_chart(fig10)

# ── Funnel ─────────────────────────────────────────────────────

st.markdown("""
<div style="font-size:25px; line-height:1.5; color:#1a1a1a; text-align:justify;">
  <p>
    De las casi <b>70 millones de cuentas administradas</b> en el <b>Sistema de Ahorro para el Retiro (SAR)</b>, aproximadamente <b>12 millones</b> pertenecen a <b>Afore Coppel</b>, posicionándola como uno de los principales jugadores del mercado.
    <br><br>
    Sin embargo, en el canal digital existe una importante brecha: <b>AforeMóvil</b> cuenta con cerca de <b>10 millones de usuarios</b>, mientras que la aplicación de <b>BanCoppel</b>, tomada como benchmark, registra casi <b>11 millones de usuarios</b>.
    <br><br>
    En un best case scenario donde los <b>12 millones de clientes de Afore Coppel</b> migraran a <b>AforeMóvil</b>, considerando que alrededor de <b>2 millones</b> ya formaban parte de Afore Coppel, existiría un <b>cuello de botella de 2 millones de usuarios</b> si la infraestructura actual no escala adecuadamente.
    <br><br>
    Esto revela una gran oportunidad estratégica: <b>integrar y conciliar los servicios de Afore Coppel con BanCoppel</b>, creando una interfaz más alineada con el ecosistema digital de Coppel, más moderna y en constante evolución.
    <br><br>
    Esta integración permitiría desarrollar funcionalidades clave como <b>aportaciones voluntarias</b>, <b>educación financiera mediante blogs</b>, <b>simuladores de retiro</b>, <b>productos financieros de Afore Coppel</b> y herramientas de fidelización, fortaleciendo la experiencia del cliente y aumentando la captación digital.
    <br><br>
    En la gráfica de <b>boxplot</b> se observa un <b>spread del 2%</b> en la media de <b>aportaciones voluntarias mensuales</b> entre AFORE que cuentan con aplicación móvil y aquellas que no, lo que sugiere una relación positiva entre digitalización y ahorro voluntario.
    <br><br>
    Finalmente, la última gráfica muestra que las <b>aportaciones voluntarias han ido aumentando gradualmente</b> en todas las AFORE; por ello, el siguiente paso estratégico es <b>fortalecer y consolidar</b> los canales digitales para capitalizar este crecimiento.
  </p>
</div>
""", unsafe_allow_html=True)


df2 = pd.read_csv("analitica.csv")

etapas = [
    "Cuentas administradas en el SAR",
    "Cuentas administradas por Coppel",
    "Usuarios App Aforemóvil",
    "Usuarios App BanCoppel"
]

valores = [69, 12, 10, 11]
colores = ['#0033A0', '#0044CC', '#0055FF', '#0033A0']

fig11 = go.Figure(go.Funnel(
    y=etapas,
    x=valores,
    textposition="inside",
    textinfo="value",
    texttemplate="%{value}M",
    textfont=dict(size=13, color="white", family="Arial Bold"),
    marker=dict(color=colores),
    connector=dict(line=dict(color="lightgray", width=2, dash="dot")),
    hovertemplate="<b>%{y}</b><br>Valor: %{x}M<extra></extra>"
))
fig11.update_layout(
    title=dict(
        text="<b>Funnel de Conversión AFORE Coppel</b><br><sub>Millones de cuentas y descargas</sub>",
        x=0.5,
        font=dict(size=20, family="Arial Black", color="#0033A0")
    ),
    funnelmode="stack",
    height=750,
    plot_bgcolor="white",
    paper_bgcolor="white",
    font=dict(family="Arial")
)
# ❌ Elimina: st.plotly_chart(fig11)

# ── Boxplot + Jitter ───────────────────────────────────────────
colores_box = {0: "#1E3FBE", 1: "#F5C800"}
etiquetas   = {0: "Sin App",  1: "Con App"}

fig12 = go.Figure()

for i, valor in enumerate([0, 1]):
    color = colores_box[valor]
    datos = df2[df2["app_dummy"] == valor]["incremento_mensual"].dropna()

    q1, q3 = datos.quantile(0.25), datos.quantile(0.75)
    iqr = q3 - q1
    datos_filtrados = datos[(datos >= q1 - 1.5*iqr) & (datos <= q3 + 1.5*iqr)]

    np.random.seed(42 + i)
    jitter_x = np.random.uniform(-0.15, 0.15, size=len(datos_filtrados))

    fig12.add_trace(go.Scatter(
        x=[i + j for j in jitter_x],
        y=datos_filtrados,
        mode="markers",
        marker=dict(color=color, size=6, opacity=0.35),
        showlegend=False,
        hovertemplate=f"<b>{etiquetas[valor]}</b><br>Incremento: %{{y:.2f}}%<extra></extra>"
    ))
    fig12.add_trace(go.Box(
        y=datos_filtrados,
        x=[i] * len(datos_filtrados),
        name=etiquetas[valor],
        boxmean=True,
        marker_color=color,
        line=dict(color="black", width=2),
        fillcolor=color,
        opacity=0.7,
        boxpoints=False
    ))

fig12.update_xaxes(
    tickvals=[0, 1],
    ticktext=[etiquetas[0], etiquetas[1]],
    title="App Dummy",
    tickfont=dict(size=13),
    showgrid=False
)
fig12.update_layout(
    template="plotly_white",
    title=dict(
        text="<b>Distribución del Incremento Mensual</b><br><sup>Por disponibilidad de App</sup>",
        x=0.5,
        xanchor="center",
        font=dict(size=20, color="#1a1a2e"),
    ),
    yaxis=dict(
        title="Incremento Mensual (%)",
        tickfont=dict(size=12),
        ticksuffix="%",
        showgrid=True
    ),
    height=750
)

# ── Barras por AFORE ───────────────────────────────────────────
df_anual_afore = df2.groupby(["año", "afore"])["incremento_mensual"].sum().reset_index()

fig13 = px.bar(
    df_anual_afore,
    x="año",
    y="incremento_mensual",
    color="afore",
    barmode="group",
    title="Incremento Acumulado Anual por AFORE",
    labels={"incremento_mensual": "Incremento Total", "año": "Año"}
)
fig13.update_layout(
    template="plotly_white",
    title_x=0.5,
    yaxis=dict(title="Incremento Total (%)", ticksuffix="%"),
)
fig13.update_traces(
    hovertemplate="<b>Año:</b> %{x}<br><b>Incremento:</b> %{y:.1f}%<br><b>AFORE:</b> %{fullData.name}<extra></extra>"
)
# ❌ Elimina: st.plotly_chart(fig13)

# ── Navegador ──────────────────────────────────────────────────
# ── Navegador 2 (fig11, fig12, fig13) ─────────────────────────
graficas_2 = [
    ("Funnel de Conversión AFORE Coppel", fig11),
    ("Distribución del Incremento Mensual", fig12),
    ("Incremento Acumulado Anual por AFORE", fig13),
]

if "slide_idx_2" not in st.session_state:
    st.session_state.slide_idx_2 = 0
elif st.session_state.slide_idx_2 >= len(graficas_2):
    st.session_state.slide_idx_2 = 0

col_prev2, col_titulo2, col_next2 = st.columns([1, 4, 1])

with col_prev2:
    if st.button("◀ Anterior", disabled=(st.session_state.slide_idx_2 == 0), key="btn_anterior_2"):
        st.session_state.slide_idx_2 -= 1
        st.rerun()

with col_titulo2:
    titulo, _ = graficas_2[st.session_state.slide_idx_2]
    st.markdown(
        f"<h4 style='text-align:center'>{titulo} "
        f"({st.session_state.slide_idx_2 + 1}/{len(graficas_2)})</h4>",
        unsafe_allow_html=True
    )

with col_next2:
    if st.button("Siguiente ▶", disabled=(st.session_state.slide_idx_2 == len(graficas_2) - 1), key="btn_siguiente_2"):
        st.session_state.slide_idx_2 += 1
        st.rerun()

_, fig_actual = graficas_2[st.session_state.slide_idx_2]
st.plotly_chart(fig_actual, use_container_width=True)




# cd C:/Users/monzo/Desktop/PAD/COPPEL
# python -m streamlit run APP_COPPEL.py
#Librerias
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import geopandas as gpd
import unicodedata
import os

st.set_page_config(layout="wide")

#Título y descripción de la página
st.title("📈 Análisis Histórico del Mercado")
st.write("A continuación se exponen las principales visualizaciones y conclusiones de la evolución del precio del mercado inmobiliario en la Comunidad de Madrid")

#Dfs necesarios
df_municipios = pd.read_csv("data/municipios.csv")
df_medias = pd.read_csv("data/medias.csv")
df_distritos = pd.read_csv("data/distritos.csv")

st.divider()

#Grafico de lineas España y Madrid

st.subheader("Evolución del precio medio en España y Comunidad de Madrid")
st.text("El siguiente gráfico muestra la evolución del valor tasado medio por metro cuadrado en España y en la Comunidad de Madrid desde 1995 hasta 2025.")

# Filtrar dataframes
mad = df_medias[df_medias["Region"] == "Madrid"].sort_values("Fecha")
esp = df_medias[df_medias["Region"] == "España"].sort_values("Fecha")
# Crear figura
fig = go.Figure()
# Línea Madrid
fig.add_trace(go.Scatter(
    x=mad["Fecha"], 
    y=mad["Valor_Tasado"],
    mode="lines",
    name="Media Madrid",
    line=dict(width=3, color="#1f77b4")))
# Línea España
fig.add_trace(go.Scatter(
    x=esp["Fecha"], 
    y=esp["Valor_Tasado"],
    mode="lines",
    name="Media España",
    line=dict(width=3, color="#ff7f0e")))
# Layout
fig.update_layout(
    title="Evolución del valor tasado medio: España vs Comunidad de Madrid",
    xaxis_title="Fecha",
    yaxis_title="Valor Tasado (€)",
    hovermode="x unified",
    template="plotly_white",
    height=500,)
# Mostrar en Streamlit
st.plotly_chart(fig, use_container_width=True)

st.text("Se observa una evolución similar en ambas series, siendo la media de Madrid consistentemente más alta que la media nacional. \n\
Ambas series muestran un crecimiento sostenido hasta 2008, seguido de una caída pronunciada hasta 2013. A partir de 2014, ambas series inician una recuperación gradual que se acelera a partir de 2020.")

st.divider()

#Grafico de lineas con filtros

st.subheader("Evolución del precio medio en la Comunidad de Madrid por municipio")
st.text("Este gráfico interactivo permite seleccionar los municipios deseados para ver su evolución de los años 2005-2025")

# Selector de municipios
municipios = df_municipios["Municipio"].unique()
seleccion = st.multiselect(
    "Selecciona uno o varios municipios:",
    options=municipios,
    default=["Madrid"])
# Filtramos solo para este gráfico
df_lineas = df_municipios[df_municipios["Municipio"].isin(seleccion)]
# Gráfico de líneas
fig_lineas = px.line(
    df_lineas,
    x="Fecha",
    y="Valor_Tasado",
    color="Municipio",
    markers=True,
    title="Evolución del valor tasado por municipio",)
st.plotly_chart(fig_lineas, use_container_width=True)

st.divider()

#Mapa interactivo

st.subheader("Mapa histórico del valor tasado e incremento anual en la Comunidad de Madrid")
st.markdown("""Este mapa interactivo permite seleccionar entre valor tasado (€ / m²) o incremento anual (%) para observar de forma visual la evolución de los municipios. Seleccione el año de su interés o haga click en el botón de *play* para ver la evolución desde el 2005.  
           *Nota: Para el incremento anual (%), el mapa está vacío para el año 2005, ya que no hay datos del año anterior con los que comparar*""")

@st.cache_data
def load_limites_geo():
    path = "data/limites_madrid.geojson"
    with open(path, "r", encoding="utf-8") as f:
        geojson = json.load(f)
    gdf = gpd.GeoDataFrame.from_features(geojson["features"])
    gdf = gdf.set_crs(epsg=4326)
    return gdf, geojson
gdf, geojson = load_limites_geo()

#Calcular incremento anual
gdf_all = gdf.sort_values(["NAMEUNIT", "Año"])
gdf_all["Incremento_%"] = (
    gdf_all
    .groupby("NAMEUNIT")["Valor_Tasado"]
    .pct_change() * 100)

#Crear selector
modo = st.radio(
    "Selecciona el tipo de visualización:",
    ["Valor tasado (€ / m²)", "Incremento anual (%)"],
    horizontal=True)

#Lógica del modo
if modo == "Valor tasado (€ / m²)":
    color_var = "Valor_Tasado"
    color_scale = "YlOrRd"
    range_color = None
    titulo = "Valor tasado por municipio – Comunidad de Madrid (2005–2025)"
    label_color = "€/m²"

else:
    color_var = "Incremento_%"
    color_scale = "RdYlGn"
    range_color = (-20, 15)
    titulo = "Incremento anual del valor tasado por municipio (%) – Comunidad de Madrid"
    label_color = "Incremento anual (%)"

#Crear mapa
fig = px.choropleth_mapbox(
    gdf_all,
    geojson=geojson,
    locations="id",
    featureidkey="properties.id",
    color=color_var,
    animation_frame="Año",
    mapbox_style="carto-positron",
    zoom=8.5,
    height=700,
    center={"lat": 40.3468, "lon": -3.7038},
    opacity=0.7,
    color_continuous_scale=color_scale,
    range_color=range_color,
    labels={color_var: label_color},
    hover_name="NAMEUNIT",
    hover_data={
        "NAMEUNIT": False,
        color_var: ":.2f" if modo == "Incremento anual (%)" else ":.0f",
        "Valor_Tasado": ":.0f",
        "id": False
    }
)

fig.update_layout(
    title=titulo,
    margin=dict(r=0, l=0, t=40, b=0)
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

#Nivel Municipio de Madrid
st.header("Análisis específico del Municipio de Madrid")
st.text("Podemos ver cómo el Municipio de Madrid se mantiene durante los años como el municipio con el valor tasado más alto.\n\
Además de ser la capital de la Comunidad, representa casi al 50% de la población total de la Región.")

#Evolucion temporal distritos

st.subheader("Evolución del precio medio por distrito en el Municipio de Madrid")

distritos_sel = st.multiselect(
    "Selecciona uno o varios distritos:",
    sorted(df_distritos["Distrito"].unique()),
    default=["Salamanca", "Centro"])

df_ciudad = df_distritos[df_distritos["Distrito"] == "Ciudad de Madrid"][["Año", "€/m²"]]
df_solo_distritos = df_distritos[df_distritos["Distrito"] != "Ciudad de Madrid"]

fig = px.line(
    df_solo_distritos[df_solo_distritos["Distrito"].isin(distritos_sel)],
    x="Año",
    y="€/m²",
    color="Distrito",)

fig.add_scatter(
    x=df_ciudad["Año"],
    y=df_ciudad["€/m²"],
    mode="lines",
    name="Ciudad de Madrid",
    line=dict(color="green", dash="dash"))

st.plotly_chart(fig, use_container_width=True)

st.divider()

#Precio medio

st.subheader("Precio medio por distrito en el Municipio de Madrid")

year_sel = st.slider(
    "Selecciona el año",
    int(df_distritos["Año"].min()),
    int(df_distritos["Año"].max()),
    2024)

df_rank = (
    df_distritos[
        (df_distritos["Año"] == year_sel) &
        (df_distritos["Distrito"] != "Ciudad de Madrid")
        ]
    .sort_values("€/m²", ascending=False))

df_rank["Distrito"] = pd.Categorical(
    df_rank["Distrito"],
    categories=df_rank["Distrito"],
    ordered=True)

n_distritos = df_rank.shape[0]
altura = max(400, n_distritos * 35)

fig = px.bar(
    df_rank,
    x="€/m²",
    y="Distrito",
    orientation="h",
    height=altura)

fig.update_layout(
    yaxis=dict(autorange="reversed"),
    xaxis_title="€/m²",
    yaxis_title="Distrito",
    margin=dict(l=120)
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# Incremento acumulado desde 2015

year_base = 2015
year_last = df_distritos["Año"].max()

df_growth = (
    df_distritos[
        (df_distritos["Año"].isin([2015, year_last])) &
        (df_distritos["Distrito"] != "Ciudad de Madrid")
    ]
    .pivot(index="Distrito", columns="Año", values="€/m²")
    .dropna()
)

df_growth["Incremento_%"] = (df_growth[year_last] / df_growth[2015] - 1) * 100

df_growth = df_growth.sort_values("Incremento_%", ascending=False)

# Convertir índice en categórico
df_growth.index = pd.Categorical(
    df_growth.index,
    categories=df_growth.index,
    ordered=True)

# Gráfico

st.subheader("Incremento acumulado del precio medio por distrito (2015-2024)")

df_growth = df_growth.reset_index()
df_growth = df_growth.rename(columns={"index": "Distrito"})

n_distritos = df_growth.shape[0]
altura = max(400, n_distritos * 35)

fig = px.bar(
    df_growth,
    x="Incremento_%",
    y="Distrito",
    orientation="h",
    height=altura,
    color_discrete_sequence=["#2ca02c"]
)

fig.update_layout(
    yaxis=dict(autorange="reversed"),
    margin=dict(l=140)
)

st.plotly_chart(fig, use_container_width=True)















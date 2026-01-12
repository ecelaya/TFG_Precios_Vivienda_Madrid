#Librerías
import streamlit as st
import pandas as pd
import geopandas as gpd
import os
import json

st.set_page_config(layout="wide")

#Título y descripción de la página
st.title("📁 Datos")
st.write("A continuación se muestran todas las bases de datos tratadas que han sido utilizadas para la creación de visualizaciones, desarrollo del análisis y de los modelos.")

#Cargar df de municipios
df_municipios = pd.read_csv("data/municipios.csv")

#Cargar df de medias
df_medias = pd.read_csv("data/medias.csv")

#Cargar df merged
df_merge = pd.read_csv("data/precios_municipios.csv")

#Cargar df de distritos
df_distritos = pd.read_csv("data/distritos.csv")

#Cargar df límites
@st.cache_resource
def load_limites_geo():
    path = os.path.join(os.path.dirname(__file__), "..", "data", "limites_madrid.geojson")
    path = os.path.abspath(path)
    with open(path, "r", encoding="utf-8") as f:
        geo = json.load(f)
    return gpd.GeoDataFrame.from_features(geo["features"], crs="EPSG:4326")

gdf = load_limites_geo()

#Cargar df mercado inmobiliario para modelos
df_modelos = pd.read_csv("data/modelos.csv")

#df municipios
st.title("📊 Valor tasado medio (€/m²)")
st.write("Base de datos con el valor tasado medio por metro cuadrado de cada municipio de la Comunidad de Madrid.\
         Incluye los Municipios de más de 25000 habitantes del año 2005 al 2025 por trimestres, además del valor tasado y el número de tasaciones.")
st.dataframe(df_municipios)
st.caption("Fuente: Ministerio de Transportes, Movilidad y Agenda Urbana (MITMA)")

st.divider()

#df medias
st.title("📊 Medias de España y Comunidad de Madrid")
st.write("Base de datos con las medias del valor tasado medio por metro cuadrado en España y en la Comunidad de Madrid.\
         Incluye los datos desde el año 1995 al 2025 por trimestres.")
st.dataframe(df_medias)
st.caption("Fuente: Ministerio de Transportes, Movilidad y Agenda Urbana (MITMA)")

st.divider()

#df_merge
st.title("📊 Datos combinados")
st.write("Base de datos combinada que incluye el valor tasado medio por metro cuadrado de cada municipio de la Comunidad de Madrid junto con las medias de España y la Comunidad de Madrid.")
st.dataframe(df_merge)

st.divider()

#df_municipio
st.title("📊 Precio medio declarado (€/m²)")
st.write("Base de datos con el precio medio declarado por metro cuadrado de cada distrito del Municipio de Madrid.\
         Incluye los datos desde el año 2007 al 2024 por años.")
st.dataframe(df_distritos)
st.caption("Fuente: Colegio de Registradores de España")

st.divider()

#df límites
st.title("📊 Límites Municipales")
st.write("Datos geoespaciales que contienen los límites municipales de toda España (Se muestran solo las primeras 50 entradas). Se incluye también el valor tasado de cada año para los distintos municipios, ya que será usado conjuntamente con los límites para la creación de mapas.")
st.dataframe(gdf.drop(columns="geometry").head(50))
st.caption("Fuente: Instituto Geográfico Nacional (IGN)")

st.divider()

#df modelos
st.title("📊 Dataset de Portal Inmobiliario para Modelización")
st.write("Base de datos utilizada para el entrenamiento de los modelos de aprendizaje automático. Incluye variables estructurales y de localización del inmueble.")
st.dataframe(df_modelos)

st.caption("Fuente: Kaggle")






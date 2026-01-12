#Librerías necesarias
import streamlit as st
import pandas as pd
import geopandas as gpd
import pydeck as pdk
import json

#Título y descripción de la página
st.set_page_config(page_title="Dashboard Vivienda", layout="wide")
st.title("🏠 Dashboard Vivienda")
st.caption("Eloy Celaya López")
st.markdown("""Bienvenido al dashboard del TFG de Eloy Celaya López, para el grado de Estadística y Empresa en la Universidad Carlos III de Madrid.
         El objetivo de este dashboard es mostrar de forma interactiva todos los resultados obtenidos mediante el análisis además de poder probar los modelos creados.
         Es recomendable el uso de un ordenador para la utilización de la app.""")

st.markdown("### 🧭 ¿Cómo usar este dashboard?")

st.markdown("""
La web dispone de varios apartados a los que se puede acceder a través del menú de la izquierda:
- **Inicio**: visión general del estudio y métricas clave  
- **Datos**: descripción de los datasets y variables utilizadas  
- **Análisis histórico**: patrones temporales y espaciales del mercado  
- **Modelización**: comparación y evaluación de los modelos predictivos  
- **Predicción de precio**: simulación interactiva del precio de una vivienda  """)

st.divider()

st.title("Memoria del TFG")





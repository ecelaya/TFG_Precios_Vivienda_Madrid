import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

#Importar datos
df_modelos = pd.read_csv("data/modelos.csv")
df_modelos_final = pd.read_csv("data/modelos_final.csv")

st.title("🧠 Modelización")
st.write("""En esta sección se presentan los modelos de aprendizaje automático utilizados para
predecir el precio de la vivienda en la Comunidad de Madrid.

Los modelos se entrenan a partir de variables estructurales y de localización del inmueble.
Las transformaciones internas (logaritmos, escalado) se aplican únicamente durante el
entrenamiento y no se muestran aquí para facilitar la interpretación.""")

st.subheader("📊 Dataset utilizado para el entrenamiento")
st.dataframe(df_modelos.sample(200))
st.caption("Fuente: Kaggle")

st.divider()

### Preprocesamiento y transformaciones

st.subheader("Preprocesamiento y transformaciones")
st.markdown("""Antes del entrenamiento de los modelos se aplicó un preprocesamiento de los datos con el
objetivo de mejorar la estabilidad numérica y la capacidad predictiva de los algoritmos.

En concreto:

- Se eliminaron observaciones con valores inconsistentes o extremos no representativos.
- Las variables continuas presentan una fuerte asimetría, especialmente el precio y la superficie.
- Para el entrenamiento de los modelos se aplicaron transformaciones logarítmicas sobre el precio
  y la superficie, así como escalado de variables cuando fue necesario.

En esta sección se muestran los datos originales para facilitar la interpretación.
No obstante, algunas visualizaciones emplean escalas logarítmicas con el fin de representar
adecuadamente distribuciones muy asimétricas.""")

st.divider()

#Distribución precios
st.subheader("Distribución del precio de la vivienda")

fig = px.histogram(
    df_modelos_final,
    x="log_price",
    nbins=50,
    labels={"log_price": "Log Precio"},)

fig.update_layout(height=400)
st.plotly_chart(fig, use_container_width=True)
st.write("""Se observa que, tras aplicar una escala logarítmica, la distribución del precio presenta una
forma aproximadamente unimodal, lo que indica que la transformación reduce significativamente
la asimetría presente en los valores originales.""")

st.divider()

#Superficie vs Precio
st.subheader("Relación entre superficie y precio")

fig = px.scatter(
    df_modelos_final,
    x="log_surface",
    y="log_price",
    opacity=0.4,
    labels={
        "log_surface": "Log Superficie",
        "log_price": "Log Precio"},)

fig.update_layout(height=450)
st.plotly_chart(fig, use_container_width=True)
st.write("Se observa una relación lineal positiva muy clara entre la superficie y el precio")

st.divider()

#Variables categóricas
st.subheader("Efecto de variables cualitativas")

col = st.selectbox(
    "Selecciona una variable:",
    ["Elevator", "Air_Conditioner", "Heater", "Parking", "Balcony", "Terrace", "Swimming_Pool"])

fig = px.box(
    df_modelos_final,
    x=col,
    y="log_price",
    labels={
        col: col,
        "log_price": "Log Precio"
    },
    title=f"Distribución del precio según {col}")

fig.update_layout(height=400)
st.plotly_chart(fig, use_container_width=True)

st.write("""Las variables cualitativas muestran diferencias sistemáticas en el nivel de precios.
Por ejemplo, la presencia de ascensor se asocia con valores medianos más elevados,
lo que indica que estas variables aportan información relevante al modelo.""")

st.divider()

st.subheader("Implicaciones para la modelización")
st.write("""A partir del análisis exploratorio, se observa la presencia de relaciones no lineales,
asimetría en las distribuciones y efectos diferenciados de variables cualitativas
(como ascensor, parking o terraza). Estas características limitan la capacidad explicativa
de modelos estrictamente lineales.

Por este motivo, se plantean distintos enfoques de modelización, combinando un modelo
lineal como referencia con modelos no paramétricos basados en árboles, capaces de capturar
interacciones y no linealidades de forma flexible.""")

st.divider()

st.subheader("Modelos considerados")
st.markdown("""Los modelos considerados en el análisis son los siguientes:

- **Regresión lineal**: utilizada como modelo base, permite interpretar de forma directa
  el efecto medio de cada variable sobre el precio.

- **Decision Tree Regressor**: modelo no paramétrico que permite identificar relaciones
  no lineales y estructuras jerárquicas en los datos.

- **Random Forest Regressor**: método de ensamblado basado en múltiples árboles, que reduce
  la varianza del árbol individual y mejora la capacidad predictiva.

- **XGBoost Regressor**: algoritmo de boosting secuencial que optimiza el ajuste corrigiendo
  iterativamente los errores del modelo anterior, incorporando regularización explícita
  para evitar el sobreajuste.

- **Support Vector Regression (SVR)**: modelo basado en kernels que permite capturar
  relaciones no lineales mediante transformaciones implícitas del espacio de variables,
  actuando como enfoque alternativo para contrastar el rendimiento de los métodos basados
  en árboles.""")

st.divider()

st.subheader("Selección del modelo final")
st.markdown("""La comparación entre modelos se realiza utilizando validación cruzada, evaluando tanto
la capacidad explicativa (R²) como el error de predicción (RMSE).

Los resultados indican que el modelo **XGBoost** alcanza el mejor rendimiento global,
obteniendo el mayor valor medio de R² y el menor RMSE medio. No obstante, el modelo
**Random Forest** presenta resultados muy similares, con diferencias reducidas en ambas
métricas y un nivel de estabilidad comparable en validación cruzada.

Dado que la mejora aportada por XGBoost es consistente, aunque moderada, se selecciona
este modelo como el enfoque final del estudio. El Random Forest se mantiene como una
alternativa robusta, confirmando la solidez de los resultados y reforzando la confianza
en la modelización realizada.""")

st.divider()

st.subheader("Resultados de validación cruzada")
st.markdown("""| Modelo | R² (mean) | RMSE (mean) |
|:------:|:-------------:|:---------------:|
| Regresión lineal | 0.7767 | 0.3802 |
| Decision Tree | 0.8903 | 0.2665 |
| SVR | 0.9171 | 0.2320 |
| Random Forest | 0.9408 | 0.1960 |
| **XGBoost** | **0.9465** | **0.1862** |""")


st.markdown("""La similitud de resultados entre Random Forest y XGBoost sugiere que la información
contenida en las variables explicativas es capturada de forma consistente por distintos
métodos no paramétricos. Esto refuerza la validez de las conclusiones obtenidas y pone 
de manifiesto la robustez del análisis realizado.""")




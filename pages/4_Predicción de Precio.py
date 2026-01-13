import streamlit as st
import pandas as pd
import numpy as np
import joblib
from geopy.geocoders import Nominatim
import sklearn
import xgboost
import os

st.set_page_config(layout="wide")

st.title("🏷️ Predicción del Precio de la Vivienda")
st.write("""En esta sección se presenta una herramienta interactiva que permite estimar el precio
de una vivienda a partir de sus características estructurales y de localización.
La predicción se obtiene utilizando el modelo **XGBoost**, seleccionado como modelo
final del estudio por su mayor capacidad predictiva y estabilidad.""")

#Límites geográficos del Municipio de Madrid
def is_in_madrid(lat, lon):
    return (
        40.3120 <= lat <= 40.5630 and
        -3.8880 <= lon <= -3.5170)

# Cargar modelo
def load_model():
    return joblib.load("modelo_xgb_final.pkl")
model = load_model()

# Geocoder (dirección → lat/lon)
@st.cache_resource
def get_geocoder():
    return Nominatim(user_agent="tfg_real_state_app")
geolocator = get_geocoder()

# Entradas del usuario
st.subheader("Características de la vivienda")
col1, col2 = st.columns(2)

with col1:
    surface = st.slider("Superficie (m²)", 20, 300, 80)
    rooms = st.slider("Habitaciones", 1, 6, 3)
    bathrooms = st.slider("Baños", 1, 4, 2)
    floor = st.slider("Planta", 0, 15, 3)

# Ubicación
with col2:
    st.markdown("### Ubicación")
    use_address = st.checkbox("Introducir dirección (recomendado)", value=True)

    if use_address:
        address = st.text_input(
            "Dirección",
            "Calle Serrano, Madrid")

        if st.button("📍 Usar dirección"):
            location = geolocator.geocode(address)
            if location:
                st.session_state["latitude"] = location.latitude
                st.session_state["longitude"] = location.longitude
                st.success("Ubicación encontrada correctamente")
                st.write(
                    f"Latitud: {location.latitude:.6f} | "
                    f"Longitud: {location.longitude:.6f}")
            else:
                st.error("No se pudo encontrar la dirección. Prueba a ser más específico.")
    else:
        latitude = st.number_input("Latitud", value=40.4168, format="%.6f")
        longitude = st.number_input("Longitud", value=-3.7038, format="%.6f")
        st.session_state["latitude"] = latitude
        st.session_state["longitude"] = longitude

# Equipamientos
st.subheader("Equipamientos")

col3, col4, col5 = st.columns(3)

with col3:
    elevator = st.checkbox("Ascensor")
    parking = st.checkbox("Parking")

with col4:
    air = st.checkbox("Aire acondicionado")
    heater = st.checkbox("Calefacción")

with col5:
    terrace = st.checkbox("Terraza")
    balcony = st.checkbox("Balcón")
    pool = st.checkbox("Piscina")

# Predicción
if st.button("🔮 Predecir precio"):

    # Comprobar que hay coordenadas
    if "latitude" not in st.session_state or "longitude" not in st.session_state:
        st.warning("Introduce una dirección o coordenadas antes de predecir.")
        st.stop()

    latitude = st.session_state["latitude"]
    longitude = st.session_state["longitude"]

    # Validación límites del municipio de Madrid
    if not is_in_madrid(latitude, longitude):
        st.error(
            "La ubicación introducida está fuera del municipio de Madrid. "
            "El modelo solo es válido para viviendas situadas dentro de la ciudad.")
        st.stop()

    # Crear DataFrame con columnas del modelo
    input_data = pd.DataFrame({
        "log_surface": [np.log(surface)],
        "Rooms": [rooms],
        "Bathrooms": [bathrooms],
        "Floor": [floor],
        "Latitude": [latitude],
        "Longitude": [longitude],
        "Elevator": [int(elevator)],
        "Air_Conditioner": [int(air)],
        "Heater": [int(heater)],
        "Parking": [int(parking)],
        "Balcony": [int(balcony)],
        "Terrace": [int(terrace)],
        "Swimming_Pool": [int(pool)]})

    # Predicción en log-precio
    log_price_pred = model.predict(input_data)[0]

    # Volver a euros
    price_pred = np.exp(log_price_pred)

    # Resultado
    st.subheader("💰 Resultado de la predicción")
    st.metric(
        label="Precio estimado (€)",
        value=f"{price_pred:,.0f} €")

    st.caption(
        "La estimación se basa en patrones aprendidos a partir de datos históricos "
        "del mercado inmobiliario de Madrid en el año 2023. "

        "El resultado tiene carácter orientativo y no constituye una valoración oficial.")

















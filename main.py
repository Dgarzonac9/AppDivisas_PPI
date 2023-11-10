import streamlit as st
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Llave de acceso a la API de Exchange Rates
API_KEY = "T036e078875144954d119fab60c46078f"

# Función para obtener las tasas de cambio de la API
def obtener_tasas(base):
    endpoint = f"https://open.er-api.com/v6/latest/{base}"
    response = requests.get(endpoint)
    if response.status_code == 200:
        data = response.json()
        return data['rates']
    else:
        return None

# Interfaz de Streamlit
st.title("Conversor de Divisas")

divisas_disponibles = ['USD', 'EUR', 'GBP', 'JPY']  # Puedes añadir más divisas según necesites

divisa_base = st.selectbox('Elige la divisa base', divisas_disponibles)
cantidad = st.number_input('Ingresa la cantidad:', min_value=0.01, value=1.00)

tasas = obtener_tasas(divisa_base)

if tasas:
    divisa_objetivo = st.selectbox('Elige la divisa objetivo', divisas_disponibles)
    tasa_conversion = tasas.get(divisa_objetivo)
    resultado = cantidad * tasa_conversion

    st.write(f"{cantidad} {divisa_base} = {resultado} {divisa_objetivo}")

    # Gráfico de barras con tasas de cambio
    df = pd.DataFrame(list(tasas.items()), columns=['Divisa', 'Tasa'])
    st.write("Tasas de cambio:")
    st.bar_chart(df.set_index('Divisa'))

else:
    st.write("Error al obtener las tasas de cambio. Inténtalo más tarde.")

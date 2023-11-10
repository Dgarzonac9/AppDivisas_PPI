import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt  # iiImportar Matplotlib
import numpy as np

# API key proporcionada
API_KEY = "T036e078875144954d119fab60c46078f"

# Función para obtener las tasas de cambio de la API
def obtener_tasas(base):
    endpoint = f"https://open.er-api.com/v6/latest/{base}?apikey={API_KEY}"
    response = requests.get(endpoint)
    if response.status_code == 200:
        data = response.json()
        return data['rates']
    else:
        return None

# Interfaz de Streamlit
st.title("Conversor de Divisas")

divisas_disponibles = [
    'USD', 'AED', 'AFN', 'ALL', 'AMD',
    'ANG', 'AOA', 'ARS', 'AUD', 'AWG',
    'AZN', 'BAM', 'BBD', 'BDT', 'BGN',
    'BHD', 'BIF', 'BMD', 'BND', 'BOB',
    'BRL', 'BSD', 'BTN', 'BWP', 'BYN', 
    'BZD', 'CAD', 'CDF', 'CHF', 'CLP', 
    'CNY', 'COP', 'CRC', 'CUP', 'CVE', 
    'CZK', 'DJF', 'DKK', 'DOP', 'DZD', 
    'EGP', 'ERN', 'ETB', 'EUR', 'FJD', 
    'FKP', 'FOK', 'GBP', 'GEL', 'GGP', 
    'GHS', 'GIP', 'GMD', 'GNF', 'GTQ', 
     'GYD', 'HKD', 'HNL', 'HRK', 'HTG', 
     'HUF', 'IDR', 'ILS', 'IMP', 'INR', 
    'IQD', 'IRR', 'ISK', 'JEP', 'JMD', 
    'JOD', 'JPY', 'KES', 'KGS', 'KHR', 
    'KID', 'KMF', 'KRW', 'KWD', 'KYD', 
    'KZT', 'LAK', 'LBP', 'LKR', 'LRD', 
    'LSL', 'LYD', 'MAD', 'MDL', 'MGA', 
    'MKD', 'MMK', 'MNT', 'MOP', 'MRU', 
    'MUR', 'MVR', 'MWK', 'MXN', 'MYR', 
    'MZN', 'NAD', 'NGN', 'NIO', 'NOK', 
    'NPR', 'NZD', 'OMR', 'PAB', 'PEN', 
    'PGK', 'PHP', 'PKR', 'PLN', 'PYG', 
    'QAR', 'RON', 'RSD', 'RUB', 'RWF', 
    'SAR', 'SBD', 'SCR', 'SDG', 'SEK', 
    'SGD', 'SHP', 'SLE', 'SLL', 'SOS', 
    'SRD', 'SSP', 'STN', 'SYP', 'SZL', 
    'THB', 'TJS', 'TMT', 'TND', 'TOP', 
    'TRY', 'TTD', 'TVD', 'TWD', 'TZS', 
    'UAH', 'UGX', 'UYU', 'UZS', 'VES', 
    'VND', 'VUV', 'WST', 'XAF', 'XCD', 
    'XDR', 'XOF', 'XPF', 'YER', 'ZAR', 
     'ZMW', 'ZWL'
]

divisa_base = st.selectbox('Elige la divisa base', divisas_disponibles)
cantidad = st.number_input('Ingresa la cantidad:', min_value=0.01, value=1.00)

tasas = obtener_tasas(divisa_base)
print(tasas)
if tasas:
    divisa_objetivo = st.selectbox('Elige la divisa objetivo', divisas_disponibles)
    tasa_conversion = tasas.get(divisa_objetivo)
    resultado = cantidad * tasa_conversion

    st.write(f"{cantidad} {divisa_base} = {resultado} {divisa_objetivo}")

    # Gráfico de barras con tasas de cambio usando Matplotlib
    df = pd.DataFrame(list(tasas.items()), columns=['Divisa', 'Tasa'])
    st.write("Tasas de cambio:")
    st.bar_chart(df.set_index('Divisa'))

    # Utilizando NumPy para calcular la media de las tasas de cambio
    tasas_array = np.array(list(tasas.values()))
    media_tasas = np.mean(tasas_array)

    st.write(f"La media de las tasas de cambio es: {media_tasas}")

    # Gráfico adicional con Matplotlib
    fig, ax = plt.subplots()
    ax.bar(df['Divisa'], df['Tasa'])

    # Calculando la media de las tasas y agregando una línea con la media al gráfico
    media_tasas = np.mean(df['Tasa'])
    ax.axhline(y=media_tasas, color='r', linestyle='--', label=f'Media: {media_tasas:.2f}')
    ax.set_xlabel('Divisas')
    ax.set_ylabel('Tasa de cambio')
    ax.set_title('Tasas de cambio entre divisas')

    # Reducir el número de etiquetas mostradas en el eje x
    plt.xticks(range(0, len(df['Divisa']), 2), df['Divisa'][::2], rotation='vertical', fontsize='xx-small')

    plt.subplots_adjust(bottom=0.2)  # Ajustar el espacio entre las etiquetas del eje x

    st.pyplot(fig)  # Mostrar el gráfico de Matplotlib en Streamlit

else:
    st.write("Error al obtener las tasas de cambio. Inténtalo más tarde.")

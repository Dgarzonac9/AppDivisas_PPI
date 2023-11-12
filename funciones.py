import streamlit as st
from datetime import date
from utils import obtener_tasas, obtener_datos_historicos
import matplotlib.pyplot as plt 
import pandas as pd
import numpy as np



def vistas(vista):
    if vista == 'Inicio':
        principal_page()
    elif vista == 'Histórico':
        historico_page()

def principal_page():
    ruta_divisas = "https://raw.githubusercontent.com/Dgarzonac9/AppDivisas_PPI/main/divisas.json"
    divisas_disponibles = pd.read_json(ruta_divisas)
    divisas_disponibles = divisas_disponibles["divisas_disponibles"][0]
    
    divisa_base = st.selectbox('Elige la divisa base', divisas_disponibles)
    cantidad = st.number_input('Ingresa la cantidad:', min_value=0.01, value=1.00)

    tasas = obtener_tasas(divisa_base)
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

def historico_page():
    ruta_divisas = "https://raw.githubusercontent.com/Dgarzonac9/AppDivisas_PPI/main/divisas.json"
    divisas_disponibles = pd.read_json(ruta_divisas)
    divisas_disponibles = divisas_disponibles["divisas_disponibles"][0]
    
    fecha_deseada = st.date_input("Selecciona una fecha", max_value=date.today())
    divisa_base = st.selectbox('Elige la divisa base', divisas_disponibles)
    monedas_objetivo = st.multiselect('Elige las monedas objetivo', divisas_disponibles)
    submitted = st.button("Enviar")
    if submitted:
        datos_historicos = obtener_datos_historicos(fecha_deseada, divisa_base, monedas_objetivo)
        # Realiza acciones con los datos obtenidos, como mostrarlos o procesarlos de alguna manera

        if datos_historicos:
            monedas = []
            valores = []

            for key, value in datos_historicos['quotes'].items():
                moneda = key[3:]
                monedas.append(moneda)
                valores.append(value)

            # Creación de la gráfica
            plt.figure(figsize=(10, 6))
            plt.bar(monedas, valores)
            plt.title(f'Tasas de cambio para {datos_historicos["source"]} en la fecha {datos_historicos["date"]}')
            plt.xlabel('Monedas')
            plt.ylabel('Tasas de cambio')
            st.pyplot(plt)
        else:
            st.write("Error al obtener los datos históricos. Inténtalo más tarde.")


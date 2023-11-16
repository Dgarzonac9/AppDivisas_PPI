import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import date

import streamlit as st
from utils import obtener_tasas, obtener_datos_historicos


def vistas(vista):
    """
    En esta funcion se va a ir dividiendo las
    opciones que muestran en el sidebar
    """
    if vista == 'Inicio':
        principal_page()
    elif vista == 'Histórico':
        historico_page()
    elif vista == 'Rendimiento':
        rendimiento_cartera()


def principal_page():
    """
    Realiza el cambio de divisas utilizando datos de una API.

    La función realiza las siguientes acciones:
    1. Carga las divisas disponibles desde un archivo JSON remoto.
    2. Permite al usuario seleccionar la divisa base y la cantidad a convertir.
    3. Obtiene las tasas de cambio en función de la divisa base seleccionada.
    4. Permite al usuario seleccionar la divisa objetivo.
    5. Calcula y muestra el resultado de la conversión.
    6. Muestra un gráfico de barras con las tasas de cambio.
    7. Calcula la media de las tasas de cambio y muestra el resultado.

    Nota:
    La función utiliza Streamlit para la construcción de la interfaz y pandas,
    NumPy, y Matplotlib para realizar operaciones y visualizaciones.
    """
    # Cargar las divisas disponibles desde el archivo JSON remoto
    base_url = "https://raw.githubusercontent.com"
    path = "/Dgarzonac9/AppDivisas_PPI/main/divisas.json"
    ruta_divisas = f"{base_url}{path}"
    divisas_disponibles = pd.read_json(ruta_divisas)
    divisas_disponibles = divisas_disponibles["divisas_disponibles"][0]

    # Colocar titulo a la pagina
    st.title("DivisApp")

    # Permitir al usuario seleccionar la divisa base y la cantidad a convertir
    divisa_base = st.selectbox(
        'Elige la divisa base', divisas_disponibles)

    cantidad = st.number_input(
        'Ingresa la cantidad:', min_value=0.01, value=1.00)

    # Obtener las tasas de cambio en función de la divisa base seleccionada
    tasas = obtener_tasas(divisa_base)

    if tasas:
        # Filtrar tasas de cambio con valores bajos
        tasas_filtradas = {
            divisa: tasa for divisa, tasa in tasas.items() if tasa >= 3}
        tasas_filtradas_pequeñas = {
            divisa: tasa for divisa, tasa in tasas.items() if tasa < 3}

        # Permitir al usuario seleccionar la divisa objetivo
        divisa_objetivo = st.selectbox(
            'Elige la divisa objetivo', tasas_filtradas.keys())

        # Calcular y mostrar el resultado de la conversión
        tasa_conversion = tasas_filtradas.get(divisa_objetivo)
        resultado = cantidad * tasa_conversion
        st.write(f"{cantidad} {divisa_base} = {resultado} {divisa_objetivo}")

        # Mostrar un gráfico de barras con las tasas de cambio filtradas
        df = pd.DataFrame(list(tasas_filtradas.items()),
                          columns=['Divisa', 'Tasa'])

        # Calcular la media de las tasas de cambio y mostrar el resultado
        tasas_array = np.array(list(tasas_filtradas.values()))
        media_tasas = np.mean(tasas_array)

        # Mostrar un gráfico adicional con Matplotlib
        fig, ax = plt.subplots()
        ax.bar(df['Divisa'], df['Tasa'])

        mostrar_media = st.checkbox("Mostrar media de tasas de cambio")

        # Agregar una línea con la media al gráfico
        if mostrar_media:
            ax.axhline(y=media_tasas, color='r', linestyle='--',
                       label=f'Media: {media_tasas:.2f}')
        ax.set_xlabel('Divisas')
        ax.set_ylabel('Tasa de cambio')
        ax.set_title(
            'Tasas de cambio entre divisas para tasas grandes(mayores a 3)')

        # Reducir el número de etiquetas mostradas en el eje x
        plt.xticks(range(0, len(df['Divisa']), 2), df['Divisa'][::2],
                   rotation='vertical', fontsize='xx-small')

        # Ajustar el espacio entre las etiquetas del eje x
        plt.subplots_adjust(bottom=0.2)

        # Mostrar el gráfico de Matplotlib en Streamlit
        st.pyplot(fig)

        # Mostrar dataframe con tasas pequeñas
        df_pequeño = pd.DataFrame(list(
            tasas_filtradas_pequeñas.items()), columns=['Divisa', 'Tasa'])

        # Hacer segundo grafico
        tasas_array_pequeño = np.array(list(tasas_filtradas_pequeñas.values()))

        fig_pequeño, ax_pequeño = plt.subplots()

        # Filtrar el DataFrame para incluir solo tasas con valores
        # Mayores a cero
        df_pequeño_filtrado = df_pequeño[df_pequeño['Tasa'] > 0]

        ax_pequeño.bar(df_pequeño_filtrado['Divisa'],
                       df_pequeño_filtrado['Tasa'])

        mostrar_media_pequeño = st.checkbox(
            "Mostrar media de tasas, para la tasa de cambio pequeña")

        # Calcular la media de las tasas pequeñas
        media_tasas_pequeñas = np.mean(tasas_array_pequeño)

        # Agregar una línea con la media al gráfico
        if mostrar_media_pequeño:
            ax_pequeño.axhline(
                y=media_tasas_pequeñas,
                color='r',
                linestyle='--',
                label=f'Media: {media_tasas_pequeñas:.2f}')

        # Voltear las etiquetas en el eje x
        plt.xticks(rotation='vertical')

        # Ajustar las etiquetas de la gráfica
        ax_pequeño.set_xlabel('Divisas')
        ax_pequeño.set_ylabel('Tasa de cambio')
        ax_pequeño.set_title(
            'Tasas de cambio entre divisas para tasas pequeñas(menores a 3)')

        # Ajustar el espacio entre las etiquetas del eje x
        plt.subplots_adjust(bottom=0.2)

        # Mostrar el gráfico
        st.pyplot(fig_pequeño)

    else:
        st.write("Error al obtener las tasas de cambio. Inténtalo más tarde.")


def historico_page():
    """
    Muestra tasas de cambio históricas en una fecha específica.

    La función realiza las siguientes acciones:
    1. Carga las divisas disponibles desde un archivo JSON remoto.
    2. Permite al usuario seleccionar una fecha, divisa base y monedas
       objetivo.
    3. Obtiene los datos históricos en función de las selecciones del usuario.
    4. Muestra un gráfico de barras con las tasas de cambio históricas.

    Nota:
    La función utiliza Streamlit para la construcción de la interfaz, pandas,
    y Matplotlib para realizar operaciones y visualizaciones.
    """
    base_url = "https://raw.githubusercontent.com"
    path = "/Dgarzonac9/AppDivisas_PPI/main/divisas.json"
    ruta_divisas = f"{base_url}{path}"
    divisas_disponibles = pd.read_json(ruta_divisas)
    divisas_disponibles = divisas_disponibles["divisas_disponibles"][0]

    # Colocar titulo a la pagina
    st.title("Historico de tasas por dia")

    fecha_deseada = st.date_input("Selecciona una fecha",
                                  max_value=date.today())
    divisa_base = st.selectbox('Elige la divisa base',
                               divisas_disponibles)
    monedas_objetivo = st.multiselect('Elige las monedas objetivo',
                                      divisas_disponibles)
    submitted = st.button("Enviar")

    if submitted and len(monedas_objetivo) > 1:
        datos_historicos = obtener_datos_historicos(
            fecha_deseada, divisa_base, monedas_objetivo)

        # Verificar si 'quotes' es un diccionario
        if isinstance(datos_historicos.get('quotes'), dict):
            monedas = []
            valores = []

            for key, value in datos_historicos['quotes'].items():
                moneda = key[3:]
                monedas.append(moneda)
                valores.append(value)

            # Creación de la gráfica
            plt.figure(figsize=(10, 6))
            plt.bar(monedas, valores)
            plt.title(
                f'Tasas de cambio para {datos_historicos["source"]}'
                f'en la fecha'
                f'{datos_historicos["date"]}')
            plt.xlabel('Monedas')
            plt.ylabel('Tasas de cambio')
            st.pyplot(plt)
    elif len(monedas_objetivo) <= 1:
        st.write("Porfavor selecciona almenos dos monedas objetivo")
    else:
        st.write(
            "Por favor, selecciona una moneda diferente a la moneda base.")


def calcular_rendimiento_diario(precios):
    """
    Calcula el rendimiento diario de un conjunto de activos financieros.

    Args:
        precios (numpy.ndarray): Un arreglo bidimensional que contiene
        los precios
        diarios de los activos.
        Cada fila representa un activo, y cada columna representa un día.

    Returns:
        numpy.ndarray: Un arreglo bidimensional que contiene el rendimiento
        diario de los activos.
        Cada fila representa un activo, y cada columna representa el
        rendimiento diario de un día.
    """
    rendimiento_diario = np.diff(precios, axis=1) / precios[:, :-1]
    return rendimiento_diario


def calcular_rendimiento_cartera(precios, inversiones):
    """
    Calcula el rendimiento acumulado de una cartera de activos financieros.

    Args:
        precios (numpy.ndarray): Un arreglo bidimensional que contiene los
        precios diarios de los activos.
        Cada fila representa un activo, y cada columna representa un día.
        inversiones (numpy.ndarray): Un arreglo unidimensional que contiene las
        inversiones asociadas a cada activo.

    Returns:
        numpy.ndarray: Un arreglo unidimensional que representa el rendimiento
        acumulado de la cartera.
    """
    rendimiento_diario = calcular_rendimiento_diario(precios)
    rendimiento_cartera = np.dot(inversiones, rendimiento_diario)
    return rendimiento_cartera


def rendimiento_cartera():
    """
    Interfaz gráfica para calcular y visualizar el rendimiento diario de
    una cartera de activos financieros.

    La función utiliza Streamlit para crear una interfaz interactiva
    con el usuario, donde se ingresan los activos, los precios diarios
    y las inversiones correspondientes.Luego, calcula el rendimiento
    diario de la cartera y muestra un gráfico que representa el
    rendimiento de cada activo a lo largo del tiempo.

    Parámetros:
        No recibe parámetros directos, pero utiliza la función
        calcular_rendimiento_cartera.

    Returns:
        None
    """
    st.title("Calculadora de Rendimiento de Cartera")

    # Input de activos y precios
    numero_activos = st.number_input("Número de Activos",
                                     min_value=1, value=3, step=1)

    activos = []
    precios = []

    for i in range(numero_activos):
        nombre_activo = st.text_input(
            f"Nombre del Activo {i + 1}",
            f"Activo {i + 1}")
        activos.append(nombre_activo)

        precios_activo = st.text_input(
            f"Precios del {nombre_activo} (separados por coma)",
            "100, 105, 98, 102")
        precios_activo = [
            float(precio.strip()) for precio in precios_activo.split(',')]
        precios.append(precios_activo)

    # Inversiones
    inversiones = []
    for activo in activos:
        inversion = st.number_input(
            f"Inversión en {activo}",
            min_value=0.0, value=10000.0)
        inversiones.append(inversion)

    precios = np.array(precios)
    inversiones = np.array(inversiones)

    # Calcular rendimiento
    rendimiento_cartera = calcular_rendimiento_cartera(precios, inversiones)

    # Mostrar gráfico
    fig, ax = plt.subplots()
    for i in range(len(activos)):
        ax.plot(precios[i], label=activos[i])

    ax.set_xlabel('Días')
    ax.set_ylabel('Precio')
    ax.set_title('Rendimiento Diario de Activos')
    ax.legend()

    # Mostrar resultados
    st.header("Resultados:")
    st.write("Rendimiento diario de la cartera:", rendimiento_cartera)
    st.write("Media del rendimiento:", np.mean(rendimiento_cartera))
    st.write("Desviación estándar del rendimiento:",
             np.std(rendimiento_cartera))

    # Mostrar el gráfico en Streamlit
    st.pyplot(fig)
    
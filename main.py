import streamlit as st
import funciones


def sidebar():
    """
    Muestra una barra lateral en la interfaz de Streamlit con botones para navegar entre páginas.

    La función realiza las siguientes acciones:
    1. Recupera la página actual de la sesión de Streamlit.
    2. Crea botones en la barra lateral para las páginas 'Inicio' y 'Histórico'.
    3. Actualiza la variable de estado 'pagina' al hacer clic en los botones.
    4. Llama a la función 'vistas' del módulo 'funciones' para mostrar la página seleccionada.

    Nota:
    La función utiliza Streamlit para la construcción de la interfaz y depende de la variable
    de estado 'pagina' y la función 'vistas' del módulo 'funciones'.
    """
    # Recupera la página actual de la sesión de Streamlit
    pagina = st.session_state.get('pagina', 'Inicio')

    # Crea botones en la barra lateral para las páginas 'Inicio' y 'Histórico'
    if st.sidebar.button('Inicio', key='Inicio'):
        st.session_state.pagina = 'Inicio'
    if st.sidebar.button('Histórico', key='Histórico'):
        st.session_state.pagina = 'Histórico'

    # Llama a la función 'vistas' del módulo 'funciones' para mostrar la página seleccionada
    funciones.vistas(pagina)

# Llama a la función 'sidebar' para mostrar la barra lateral en la interfaz
sidebar()

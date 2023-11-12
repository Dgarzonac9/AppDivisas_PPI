import streamlit as st
import funciones



def sidebar():
    pagina = st.session_state.get('pagina', 'Inicio')

    if st.sidebar.button('Inicio', key = 'Inicio'):
        st.session_state.pagina = 'Inicio'
    if st.sidebar.button('Histórico', key = 'Histórico'):
        st.session_state.pagina = 'Histórico'
    funciones.vistas(pagina)


sidebar()
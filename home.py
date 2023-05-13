import streamlit as st


def app():
    st.title("Práctica 2")

    col1, col2 = st.columns([2, 1])
    with col1:
        st.write("## Integrantes")
        st.write("338803 - Saul Fernando Rodríguez Gutiérrez")
        st.write("338817 - Eric Alejandro Aguilar Marcial")
        st.write("338931 - Andrés Alexis Villalba García")

        st.write("## Información de la clase")
        st.write("M.S.I. Perla Ivonne Cordero De Los Ríos")
        st.write("Ingeniería de Software II")
        st.write("8CC2")

    with col2:
        st.image("https://uach.mx/assets/media/publications/2017/11/169_imagen-uach/escudo-color.png", width=200)
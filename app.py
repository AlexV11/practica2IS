import streamlit as st
import home, carreras, materias, planes

st.set_page_config(
    page_title = "Sistema de control escolar",
    page_icon = "📚",
    layout = "wide",
    initial_sidebar_state = "expanded",
    menu_items = {
        'About': 'https://github.com/AlexV11/practica2IS'
    }
)

opcion = st.sidebar.radio(
    'Seleccione una opción',
    (
        'Página de inicio',
        'Carreras',
        'Materias',
        'Planes'
    ),
    key = 'menu',
    index = 0
)

if opcion == 'Página de inicio':
    home.app()
elif opcion == 'Carreras':
    carreras.app()
elif opcion == 'Materias':
    materias.app()
elif opcion == 'Planes':
    planes.app()
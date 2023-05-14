import streamlit as st
import requests
import pandas as pd
import requests
from datetime import date

def app():
    st.title("Materias")

    url = "https://back-is.onrender.com/materias"

    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "Listado de materias",
            "Altas",
            "Bajas",
            "Cambios"
        ]
    )

    with tab1:
        st.write("Aquí se pueden ver todas las materias")

        url = "https://back-is.onrender.com/materias"

        response = requests.get(url)

        if response.status_code == 200:
            df = pd.DataFrame(response.json())
            columnas = [
                "idMateria",
                "descripcion",
                "nsesio",
                "durses",
                "taller",
                "fecalt",
                "fecbaj",
                "tipo"
            ]
            df = df[columnas]
            st.dataframe(df)
        else:
            st.error("El servidor está fuera de línea")

    with tab2:
        st.write("Aquí se pueden dar de alta nuevas materias")

        top1, top2, top3 = st.columns([3, 1, 1])
        bot1, bot2 = st.columns(2)

        top1.text_input("Nombre de la materia", key="descripcion")
        top2.number_input("Número de sesiones", key="nsesio", step=1, format="%i")
        top3.text_input("Tipo de materia", key="tipo")
        bot1.number_input("Duración de cada sesión", key="durses", step=0.5, format="%.1f")
        bot2.text_input("Defina el taller", key="taller")

        if st.button("Guardar"):
            datos = {
                "descripcion": st.session_state.descripcion,
                "nsesio": st.session_state.nsesio,
                "durses": st.session_state.durses,
                "taller": st.session_state.taller,
                "tipo": st.session_state.tipo,
                "fecalt": date.today().isoformat(),
                "fecbaj": None
            }
            guardar_materia(url, datos)
            st.experimental_rerun()

    with tab3:
        st.write("Aquí se pueden dar de baja materias existentes")

        response = requests.get(url)

        if response.status_code == 200:
            materias_columna = ["descripcion"]
            df = pd.DataFrame(response.json())
            df = df[materias_columna]
            materia = st.selectbox("Materia a eliminar", df)
            id_materia = df[df["descripcion"] == materia].index[0] + 1
            
            url2 = url + "/" + str(id_materia)

            if st.button("Eliminar"):
                datos = {
                    "fecbaj": date.today().isoformat()
                }
                eliminar_materia(url2, datos)
                st.experimental_rerun()

                
    with tab4:
        st.write("Aquí se pueden cambiar materias existentes")

        response = requests.get(url)

        if response.status_code == 200:
            materias_columna = ["descripcion", "nsesio", "durses", "taller", "tipo"]
            df = pd.DataFrame(response.json())
            df = df[materias_columna]
            materia = st.selectbox("Materia a cambiar", df)
            id_materia = df[df["descripcion"] == materia].index[0] + 1
            st.divider()

            nsesio_value = df[df["descripcion"] == materia]["nsesio"].values[0]
            durses_value = df[df["descripcion"] == materia]["durses"].values[0]
            taller_value = df[df["descripcion"] == materia]["taller"].values[0]
            tipo_value = df[df["descripcion"] == materia]["tipo"].values[0]

            url2 = url + "/" + str(id_materia)

            top1, top2, top3 = st.columns([3, 1, 1])
            bot1, bot2 = st.columns(2)

            nombre_materia_cambio = top1.text_input("Nombre de la materia", value = materia, key="descripcion_cambio")
            nsesio_materia_cambio = top2.number_input("Número de sesiones", key="nsesio_cambio", value=nsesio_value)
            durses_materia_cambio = top3.number_input("Duración de cada sesión", key="durses_cambio", value=durses_value)
            taller_materia_cambio = bot2.text_input("Defina el taller", key="taller_cambio", value=taller_value)
            tipo_materia_cambio = bot1.text_input("Tipo de materia", key="tipo_cambio", value=tipo_value)
            nombre_materia_cambio = nombre_materia_cambio.upper()

            if st.button("Guardar", key = "guardar_materia_cambio"):
                datos = {
                    "descripcion": nombre_materia_cambio,
                    "nsesio": nsesio_materia_cambio,
                    "durses": durses_materia_cambio,
                    "taller": taller_materia_cambio,
                    "tipo": tipo_materia_cambio,
                }
                cambiar_materia(url2, datos)
                st.experimental_rerun()

def guardar_materia(url, datos):
    response = requests.post(url, json=datos)
    if response.status_code == 200:
        st.success("La materia se guardó correctamente")
    else:
        st.error("Ocurrió un error al guardar la materia")
        st.error(response.text)

def eliminar_materia(url, datos):
    response = requests.patch(url, json=datos)
    if response.status_code == 200:
        st.success("La materia se eliminó correctamente")
    else:
        st.error("Ocurrió un error al eliminar la materia")
        
def cambiar_materia(url, datos):
    response = requests.patch(url, json=datos)
    if response.status_code == 200:
        st.success("La materia se actualizó correctamente")
    else:
        st.error("Ocurrió un error al actualizar la materia")
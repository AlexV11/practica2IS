import streamlit as st
import pandas as pd
import requests
from datetime import date

def app():
    st.title("Carreras")
    url = "https://back-is.onrender.com/carreras"

    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "Listado de carreras",
            "Altas",
            "Bajas",
            "Cambios"
        ]
    )

    with tab1:
        st.write("Aquí se pueden ver todas las carreras")

        response = requests.get(url)

        if response.status_code == 200:
            df = pd.DataFrame(response.json())
            columns = [
                "idCarrera",
                "nombre",
                "fecalt",
                "fecbaj"
            ]
            df = df[columns]
            st.dataframe(df)

    with tab2:
        st.write("Aquí se pueden dar de alta nuevas carreras")

        nombre_carrera = st.text_input("Nombre de la carrera")
        nombre_carrera = nombre_carrera.upper()

        datos = {
            "nombre": nombre_carrera,
            "fecalt": date.today().isoformat(),
            "fecbaj": None
        }

        if st.button("Guardar"):
            guardar_carrera(url, datos)
            st.experimental_rerun()

    with tab3:
        st.write("Aquí se pueden dar de baja carreras existentes")
        
        response = requests.get(url)

        if response.status_code == 200:
            carreras_columna = ["nombre"]
            df = pd.DataFrame(response.json())
            df = df[carreras_columna]
            carrera = st.selectbox("Carrera a eliminar", df)
            id_carrera = df[df["nombre"] == carrera].index[0] + 1
            url2 = url + "/" + str(id_carrera)

            if st.button("Eliminar"):
                datos = {
                    "fecbaj": date.today().isoformat()
                }
                eliminar_carrera(url2, datos)
                st.experimental_rerun()

    with tab4:
        st.write("Aquí se pueden cambiar carreras existentes")

        response = requests.get(url)

        if response.status_code == 200:
            carreras_columna = ["nombre"]
            
            df = pd.DataFrame(response.json())
            df = df[carreras_columna]
            carrera = st.selectbox("Carrera a cambiar", df, key="carrera_cambio")
            id_carrera = df[df["nombre"] == carrera].index[0] + 1
            url2 = url + "/" + str(id_carrera)

            nombre_carrera_cambio = st.text_input("Nombre de la carrera", value=carrera, key="nombre_carrera_cambio")
            nombre_carrera_cambio = nombre_carrera_cambio.upper()

            if st.button("Guardar", key="guardar_carrera_cambio"):
                datos = {
                    "nombre": nombre_carrera_cambio
                }
                cambiar_carrera(url2, datos)
                st.experimental_rerun()
            
        
def guardar_carrera(url, datos):
    respuesta = requests.post(url, json=datos)
    
    # Verificar el código de estado de la respuesta
    if respuesta.status_code == 200:
        print("Solicitud POST exitosa")
    else:
        print("Error en la solicitud POST")
    
    # Imprimir el contenido de la respuesta
    print(respuesta.content)

def eliminar_carrera(url, datos):
    respuesta = requests.patch(url, json=datos)
    
    # Verificar el código de estado de la respuesta
    if respuesta.status_code == 200:
        st.success("La carrera se eliminó correctamente")
    else:
        st.error("Ocurrió un error al eliminar la carrera")

def cambiar_carrera(url, datos):
    respuesta = requests.put(url, json=datos)
    
    # Verificar el código de estado de la respuesta
    if respuesta.status_code == 200:
        st.success("La carrera se actualizó correctamente")
    else:
        st.error("Ocurrió un error al actualizar la carrera")
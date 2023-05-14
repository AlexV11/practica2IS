import streamlit as st
import pandas as pd
import requests
from datetime import date
from pandas.io.json import json_normalize

def app():
    st.title("Planes de estudio")

    url = "https://back-is.onrender.com/planes"

    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "Listado de planes de estudio",
            "Altas",
            "Bajas",
            "Cambios"
        ]
    )

    with tab1:
        st.write("Aquí se pueden ver todos los planes de estudio")

        response = requests.get(url)

        if response.status_code == 200:
            df = pd.DataFrame(response.json())

            df = json_normalize(df.to_dict(orient='records'))
            
            df[["descripcion", "nombre"]] = df.apply(extract_desc_name, axis=1)
            df.drop([
                "createdAt",
                "updatedAt",
                "materias.idMateria",
                "materias.descripcion",
                "materias.nsesio",
                "materias.durses",
                "materias.taller",
                "materias.fecalt",
                "materias.fecbaj",
                "materias.tipo",
                "materias.createdAt",
                "materias.updatedAt",
                "carreras.idCarrera",
                "carreras.nombre",
                "carreras.fecalt",
                "carreras.fecbaj",
                "carreras.createdAt",
                "carreras.updatedAt"
            ], axis=1, inplace=True)
            
            orden_personalizado = [
                "id",
                "clave",
                "nombre",
                "descripcion",
                "area",
                "semestre",
                "reqsim",
                "requi1",
                "requi2",
                "requi3",
                "requi4",
                "id_materia",
                "id_carrera",
                "fecalt",
                "fecbaj"
            ]


            df = df.reindex(columns=orden_personalizado)
            st.dataframe(df)

            
        else:
            st.error("El servidor está fuera de línea")

    with tab2:
        st.write("Aquí se pueden dar de alta nuevos planes de estudio")

        url_mat = "https://back-is.onrender.com/materias"
        url_carr = "https://back-is.onrender.com/carreras"

        response_mat = requests.get(url_mat)
        response_carr = requests.get(url_carr)

        top1, top2 = st.columns(2)
        mid1, mid2, mid3 = st.columns(3)
        bot1, bot2, bot3, bot4, bot5 = st.columns(5)

        df_mat = pd.DataFrame(response_mat.json())
        materias_list = ["descripcion"]
        df_mat = df_mat[materias_list]
        df_mat.loc[-1] = [None]
        materia = top1.selectbox("Materia", df_mat)
        id_materia = df_mat[df_mat["descripcion"] == materia].index[0] + 1
    
        df_carr = pd.DataFrame(response_carr.json())
        carreras_list = ["nombre"]
        df_carr = df_carr[carreras_list]
        carrera = top2.selectbox("Carrera", df_carr)
        id_carrera = df_carr[df_carr["nombre"] == carrera].index[0] + 1
            
        index = len(df_mat) - 1

        clave_alta = mid1.number_input("Clave del plan de estudio", key="clave", step=1, format="%i")
        area_alta = mid2.text_input("Área", key="area")
        semestre_alta = mid3.number_input("Semestre", key="semestre", step=1, format="%i")
        reqsim = bot1.selectbox("Requisito similar", df_mat, index=index)
        requi1 = bot2.selectbox("Requisito 1", df_mat, index=index)
        requi2 = bot3.selectbox("Requisito 2", df_mat, index=index)
        requi3 = bot4.selectbox("Requisito 3", df_mat, index=index)
        requi4 = bot5.selectbox("Requisito 4", df_mat, index=index)

        if st.button("Guardar", key="guardar_materia"):
            datos = {
                "clave": int(clave_alta),
                "idMateria": int(id_materia),
                "idCarrera": int(id_carrera),
                "fecalt": date.today().isoformat(),
                "fecbaj": None,
                "area": area_alta,
                "reqsim": reqsim,
                "requi1": requi1,
                "requi2": requi2,
                "requi3": requi3,
                "requi4": requi4,
                "semestre": int(semestre_alta)
            }

            guardar_plan(url, datos)
            st.experimental_rerun()



    with tab3:
        st.write("Aquí se pueden dar de baja planes de estudio existentes")

        response = requests.get(url)

        if response.status_code == 200:
            df = pd.DataFrame(response.json())
            df = json_normalize(df.to_dict(orient='records'))
            df[["descripcion", "nombre"]] = df.apply(extract_desc_name, axis=1)
            columna_borrar = df["nombre"]
            plan_baja = st.selectbox("Plan de estudio", columna_borrar)
            id_plan = df[df["nombre"] == plan_baja]["id"].values[0]

            url2 = url + "/" + str(id_plan)

            if st.button("Eliminar", key="borrar_plan"):
                datos = {
                    "fecbaj": date.today().isoformat()
                }

                eliminar_plan(url2, datos)
                st.experimental_rerun()

    with tab4:
        st.write("Aquí se pueden cambiar planes de estudio existentes")

        response = requests.get(url)

        if response.status_code == 200:
            df = pd.DataFrame(response.json())
            df = json_normalize(df.to_dict(orient='records'))
            df[["descripcion", "nombre"]] = df.apply(extract_desc_name, axis=1)
            columna_cambiar = df["nombre"]
            plan_cambio = st.selectbox("Plan de estudio", columna_cambiar, key="plan_cambio")
            id_plan = df[df["nombre"] == plan_cambio]["id"].values[0]

            url2 = url + "/" + str(id_plan)

            top1, top2 = st.columns(2)
            mid1, mid2, mid3 = st.columns(3)
            bot1, bot2, bot3, bot4, bot5 = st.columns(5)

            df_mat = pd.DataFrame(response_mat.json())
            materias_list = ["descripcion"]
            df_mat = df_mat[materias_list]
            df_mat.loc[-1] = [None]
            materia = top1.selectbox("Materia", df_mat, key="materia_cambio")
            id_materia = df_mat[df_mat["descripcion"] == materia].index[0] + 1
    
            df_carr = pd.DataFrame(response_carr.json())
            carreras_list = ["nombre"]
            df_carr = df_carr[carreras_list]
            carrera = top2.selectbox("Carrera", df_carr, key="carrera_cambio")
            id_carrera = df_carr[df_carr["nombre"] == carrera].index[0] + 1
            
            index = len(df_mat) - 1

            clave_alta = mid1.number_input("Clave del plan de estudio", key="clave_cambio", step=1, format="%i")
            area_alta = mid2.text_input("Área", key="area_cambio")
            semestre_alta = mid3.number_input("Semestre", key="semestre_cambio", step=1, format="%i")
            reqsim = bot1.selectbox("Requisito similar", df_mat, index=index, key="reqsim_cambio")
            requi1 = bot2.selectbox("Requisito 1", df_mat, index=index, key="requi1_cambio")
            requi2 = bot3.selectbox("Requisito 2", df_mat, index=index, key="requi2_cambio")
            requi3 = bot4.selectbox("Requisito 3", df_mat, index=index, key="requi3_cambio")
            requi4 = bot5.selectbox("Requisito 4", df_mat, index=index, key="requi4_cambio")

            if st.button("Guardar", key = "guardar_plan_cambio"):
                datos = {
                    "clave": int(clave_alta),
                    "idMateria": int(id_materia),
                    "idCarrera": int(id_carrera),
                    "fecalt": date.today().isoformat(),
                    "fecbaj": None,
                    "area": area_alta,
                    "reqsim": reqsim,
                    "requi1": requi1,
                    "requi2": requi2,
                    "requi3": requi3,
                    "requi4": requi4,
                    "semestre": int(semestre_alta)
                }

                cambiar_plan(url2, datos)
                st.experimental_rerun()

def guardar_plan(url, datos):
    response = requests.post(url, json=datos)

    if response.status_code == 200:
        st.success("El plan de estudio se ha guardado correctamente")
    else:
        st.error("Ha ocurrido un error al guardar el plan de estudio")

def extract_desc_name(row):
                desc = row["materias.descripcion"]
                name = row["carreras.nombre"]
                return pd.Series({"descripcion": desc, "nombre": name})

def eliminar_plan(url, datos):
    response = requests.patch(url, json=datos)

    if response.status_code == 200:
        st.success("El plan de estudio se ha eliminado correctamente")
    else:
        st.error("Ha ocurrido un error al eliminar el plan de estudio")

def cambiar_plan(url, datos):
    response = requests.patch(url, json=datos)

    if response.status_code == 200:
        st.success("El plan de estudio se ha modificado correctamente")
    else:
        st.error("Ha ocurrido un error al modificar el plan de estudio")
import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="App Estadística", layout="wide")
st.title("📊 App de Análisis Estadístico")

# ─── MÓDULO 1: CARGA DE DATOS ──────────────────────────────────

st.header("📂 Carga de Datos")

tipo = st.radio("¿Cómo quieres cargar los datos?", 
                    ["Subir CSV", "Generar datos sintéticos"])

if tipo == "Subir CSV":
        archivo = st.file_uploader("Sube tu archivo CSV", type=["csv"])
        if archivo:
            df = pd.read_csv(archivo)
            st.success("✅ Archivo cargado correctamente")
            st.dataframe(df.head())
            
            # Selección de variable
            columnas_numericas = df.select_dtypes(include=np.number).columns.tolist()
            variable = st.selectbox("Selecciona la variable a analizar:", columnas_numericas)
            
            # Guardar en sesión
            st.session_state["datos"] = df[variable].dropna().values
            st.session_state["nombre_variable"] = variable
            st.info(f"Variable seleccionada: **{variable}** — {len(st.session_state['datos'])} datos")

else:  # Datos sintéticos
        st.subheader("Generador de datos sintéticos")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            n = st.number_input("Cantidad de datos (n)", min_value=30, max_value=10000, value=100)
        with col2:
            media = st.number_input("Media (μ)", value=50.0)
        with col3:
            desv = st.number_input("Desviación estándar (σ)", min_value=0.1, value=10.0)

        if st.button("🎲 Generar datos"):
            datos = np.random.normal(loc=media, scale=desv, size=int(n))
            st.session_state["datos"] = datos
            st.session_state["nombre_variable"] = "Variable sintética"
            
            df_preview = pd.DataFrame(datos, columns=["valor"])
            st.success(f"✅ {int(n)} datos generados")
            st.dataframe(df_preview.head(10))

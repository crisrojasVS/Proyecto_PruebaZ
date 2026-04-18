import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
load_dotenv()

st.header("🤖 Asistente IA con Gemini")

api_key = os.getenv("api_key")
if api_key:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-2.5-flash")

        # ── Modo 1: Análisis de distribución ──
        if "estadisticas" in st.session_state:
            st.subheader("📊 Análisis de distribución")
            est = st.session_state["estadisticas"]
            st.json(est)

            if st.button("🔍 Analizar distribución con IA"):
                prompt = f"""
                Analiza estos datos estadísticos y explica en lenguaje simple y directo qué está pasando:
                - Media: {est['media']}, Mediana: {est['mediana']}
                - Desviación estándar: {est['desv_est']}
                - Sesgo: {est['sesgo']}, Curtosis: {est['curtosis']}
                - Outliers: {est['outliers']}, ¿Normal?: {est['normal']}

                Responde en 3 puntos cortos y claros:
                1. Cómo se distribuyen los datos
                2. Si hay sesgo o valores atípicos
                3. Si la distribución es normal o no

                Usa lenguaje sencillo, sin fórmulas ni términos técnicos innecesarios.
                """
                with st.spinner("Consultando a Gemini..."):
                    respuesta = model.generate_content(prompt)
                    st.markdown("**Respuesta de Gemini:**")
                    st.write(respuesta.text)
        else:
            st.info("💡 Ve al módulo de Visualización primero para generar estadísticas.")

        # ── Modo 2: Análisis de Prueba Z ──
        if "resultado_z" in st.session_state:
            st.subheader("🔬 Análisis de Prueba Z")
            res = st.session_state["resultado_z"]
            st.json(res)

            if st.button("🤖 Analizar Prueba Z con IA"):
                decision = "Se rechaza H0" if res["rechazar"] else "No se rechaza H0"
                prompt = f"""
                Con base en estos resultados de una prueba Z:
                - Media obtenida: {res['media_muestral']}, Media esperada: {res['mu0']}
                - Z calculado: {res['z_calculado']}, Z crítico: {res['z_critico']}
                - p-value: {res['p_value']}, Alpha: {res['alpha']}
                - Decisión: {"Se rechaza H0" if res['rechazar'] else "No se rechaza H0"}

                Explica en 3 puntos cortos y en lenguaje simple:
                1. Qué significa el resultado obtenido
                2. Por qué se rechaza o no se rechaza H0
                3. Qué conclusión se puede sacar en términos reales

                Sin fórmulas ni tecnicismos, directo al punto.
                """
                with st.spinner("Consultando a Gemini..."):
                    respuesta = model.generate_content(prompt)
                    st.markdown("**Respuesta de Gemini:**")
                    st.write(respuesta.text)

                # Comparación con decisión del estudiante
                st.subheader("🆚 Compara con tu decisión")
                decision_estudiante = st.radio(
                    "Según tu criterio, ¿qué decidirías?",
                    ["Rechazar H0", "No rechazar H0"]
                )
                if st.button("Comparar"):
                    decision_app = "Rechazar H0" if res["rechazar"] else "No rechazar H0"
                    if decision_estudiante == decision_app:
                        st.success("✅ ¡Tu decisión coincide con la de la app!")
                    else:
                        st.error(f"❌ La app decide: **{decision_app}**. Revisa los criterios.")
        else:
            st.info("💡 Ve al módulo de Prueba Z primero para obtener resultados.")
else:
        st.warning("⚠️ Ingresa tu API Key para usar el asistente.")
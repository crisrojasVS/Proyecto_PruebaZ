import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from scipy import stats


st.header("📊 Visualización de Distribuciones")

if "datos" not in st.session_state:
        st.warning("⚠️ Primero carga datos en el módulo de Carga de Datos.")
else:
        datos = st.session_state["datos"]
        nombre = st.session_state["nombre_variable"]

        st.subheader(f"Variable: {nombre} — {len(datos)} observaciones")

        # ── Estadísticas básicas ──
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Media", f"{np.mean(datos):.4f}")
        col2.metric("Mediana", f"{np.median(datos):.4f}")
        col3.metric("Desv. Est.", f"{np.std(datos):.4f}")
        col4.metric("n", len(datos))

        # ── Histograma + KDE ──
        st.subheader("📈 Histograma + KDE")
        fig1, ax1 = plt.subplots(figsize=(8, 4))
        sns.histplot(datos, kde=True, ax=ax1, color="steelblue", edgecolor="white")
        ax1.set_xlabel(nombre)
        ax1.set_ylabel("Frecuencia")
        ax1.set_title("Histograma con KDE")
        st.pyplot(fig1)

        # ── Boxplot ──
        st.subheader("📦 Boxplot")
        fig2, ax2 = plt.subplots(figsize=(8, 3))
        sns.boxplot(x=datos, ax=ax2, color="lightcoral")
        ax2.set_xlabel(nombre)
        ax2.set_title("Boxplot")
        st.pyplot(fig2)

        # ── Análisis automático ──
        st.subheader("🔍 Análisis de la distribución")

        sesgo = stats.skew(datos)
        curtosis = stats.kurtosis(datos)
        stat_norm, p_norm = stats.shapiro(datos[:50] if len(datos) > 50 else datos)

        # ¿Normal?
        if p_norm > 0.05:
            st.success("✅ La distribución **parece normal** (Shapiro-Wilk p > 0.05)")
        else:
            st.error("❌ La distribución **NO parece normal** (Shapiro-Wilk p ≤ 0.05)")

        # ¿Sesgo?
        if abs(sesgo) < 0.5:
            st.info(f"📐 Sesgo: {sesgo:.4f} → Distribución aproximadamente **simétrica**")
        elif sesgo > 0:
            st.warning(f"📐 Sesgo: {sesgo:.4f} → Sesgo **positivo** (cola a la derecha)")
        else:
            st.warning(f"📐 Sesgo: {sesgo:.4f} → Sesgo **negativo** (cola a la izquierda)")

        # ¿Outliers?
        q1 = np.percentile(datos, 25)
        q3 = np.percentile(datos, 75)
        iqr = q3 - q1
        outliers = np.sum((datos < q1 - 1.5 * iqr) | (datos > q3 + 1.5 * iqr))

        if outliers == 0:
            st.success("✅ No se detectaron **outliers**")
        else:
            st.warning(f"⚠️ Se detectaron **{outliers} outlier(s)** usando el método IQR")

        # Guardar estadísticas para el módulo de IA
        st.session_state["estadisticas"] = {
            "media": round(np.mean(datos), 4),
            "mediana": round(np.median(datos), 4),
            "desv_est": round(np.std(datos), 4),
            "sesgo": round(sesgo, 4),
            "curtosis": round(curtosis, 4),
            "n": len(datos),
            "outliers": int(outliers),
            "normal": p_nom > 0.05 if (p_nom := p_norm) else False
        }

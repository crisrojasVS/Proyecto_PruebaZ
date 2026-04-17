import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

st.header("🔬 Prueba de Hipótesis Z")

if "datos" not in st.session_state:
        st.warning("⚠️ Primero carga datos en el módulo de Carga de Datos.")
else:

        datos = st.session_state["datos"]
        n = len(datos)
        media_muestral = np.mean(datos)

        st.subheader("⚙️ Parámetros de la prueba")

        col1, col2 = st.columns(2)
        with col1:
            mu0 = st.number_input("Hipótesis nula H0 (μ₀)", value=0.0)
            sigma = st.number_input("Desviación estándar poblacional (σ)", min_value=0.01, value=float(np.std(datos)))
            alpha = st.selectbox("Nivel de significancia (α)", [0.01, 0.05, 0.10], index=1)
        with col2:
            tipo_prueba = st.radio("Tipo de prueba:", [
                "Bilateral (H1: μ ≠ μ₀)",
                "Cola derecha (H1: μ > μ₀)",
                "Cola izquierda (H1: μ < μ₀)"
            ])

        st.markdown(f"""
        **Hipótesis planteadas:**
        - H0: μ = {mu0}
        - H1: {"μ ≠" if "Bilateral" in tipo_prueba else "μ >" if "derecha" in tipo_prueba else "μ <"} {mu0}
        """)

        if st.button("▶️ Ejecutar Prueba Z"):

            # ── Cálculo ──
            error_estandar = sigma / np.sqrt(n)
            z_calculado = (media_muestral - mu0) / error_estandar

            if "Bilateral" in tipo_prueba:
                p_value = 2 * (1 - stats.norm.cdf(abs(z_calculado)))
                z_critico = stats.norm.ppf(1 - alpha / 2)
                rechazar = abs(z_calculado) > z_critico
            elif "derecha" in tipo_prueba:
                p_value = 1 - stats.norm.cdf(z_calculado)
                z_critico = stats.norm.ppf(1 - alpha)
                rechazar = z_calculado > z_critico
            else:
                p_value = stats.norm.cdf(z_calculado)
                z_critico = stats.norm.ppf(alpha)
                rechazar = z_calculado < z_critico

            # ── Resultados ──
            st.subheader("📊 Resultados")
            col1, col2, col3 = st.columns(3)
            col1.metric("Z calculado", f"{z_calculado:.4f}")
            col2.metric("p-value", f"{p_value:.4f}")
            col3.metric("Z crítico", f"±{abs(z_critico):.4f}" if "Bilateral" in tipo_prueba else f"{z_critico:.4f}")

            if rechazar:
                st.error(f"❌ Se **RECHAZA** H0 (p = {p_value:.4f} ≤ α = {alpha})")
            else:
                st.success(f"✅ **No se rechaza** H0 (p = {p_value:.4f} > α = {alpha})")

            # ── Gráfica ──
            st.subheader("📈 Curva Normal con región de rechazo")
            fig, ax = plt.subplots(figsize=(10, 4))
            x = np.linspace(-4, 4, 300)
            y = stats.norm.pdf(x)
            ax.plot(x, y, color="black", linewidth=2)

            if "Bilateral" in tipo_prueba:
                ax.fill_between(x, y, where=(x <= -abs(z_critico)), color="red", alpha=0.4, label="Región de rechazo")
                ax.fill_between(x, y, where=(x >= abs(z_critico)), color="red", alpha=0.4)
                ax.axvline(-abs(z_critico), color="red", linestyle="--")
                ax.axvline(abs(z_critico), color="red", linestyle="--")
            elif "derecha" in tipo_prueba:
                ax.fill_between(x, y, where=(x >= z_critico), color="red", alpha=0.4, label="Región de rechazo")
                ax.axvline(z_critico, color="red", linestyle="--")
            else:
                ax.fill_between(x, y, where=(x <= z_critico), color="red", alpha=0.4, label="Región de rechazo")
                ax.axvline(z_critico, color="red", linestyle="--")

            ax.axvline(z_calculado, color="blue", linestyle="-", linewidth=2, label=f"Z calculado = {z_calculado:.4f}")
            ax.fill_between(x, y, where=((x >= -abs(z_critico)) & (x <= abs(z_critico))) if "Bilateral" in tipo_prueba else
                           (x < z_critico) if "derecha" in tipo_prueba else (x > z_critico),
                           color="green", alpha=0.2, label="Región de no rechazo")
            ax.legend()
            ax.set_title("Distribución Normal Estándar")
            ax.set_xlabel("Z")
            ax.set_ylabel("Densidad")
            st.pyplot(fig)

            # Guardar resultados para módulo IA
            st.session_state["resultado_z"] = {
                "media_muestral": round(media_muestral, 4),
                "mu0": mu0,
                "sigma": sigma,
                "n": n,
                "alpha": alpha,
                "tipo_prueba": tipo_prueba,
                "z_calculado": round(z_calculado, 4),
                "z_critico": round(z_critico, 4),
                "p_value": round(p_value, 4),
                "rechazar": rechazar
            }
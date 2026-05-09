import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import os

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Sabor Nacional Optimizer", layout="wide")

# --- DISEÑO MULTIMEDIA (CSS PERSONALIZADO) ---
# Aquí corregimos el error anterior y aplicamos tus preferencias estéticas
st.markdown("""
    <style>
    /* Fondo general con tonos crema */
    .main {
        background-color: #fdfaf5;
    }
    
    /* Imágenes laterales decorativas (Efecto visual de granos de café) */
    [data-testid="stAppViewContainer"]::before {
        content: "";
        position: fixed;
        top: 0; left: 0; width: 120px; height: 100%;
        background-image: url('https://images.unsplash.com/photo-1559056199-641a0ac8b55e?q=80&w=300');
        background-size: cover;
        opacity: 0.1;
        z-index: 0;
    }
    
    [data-testid="stAppViewContainer"]::after {
        content: "";
        position: fixed;
        top: 0; right: 0; width: 120px; height: 100%;
        background-image: url('https://images.unsplash.com/photo-1580915411954-282cb1b0d780?q=80&w=300');
        background-size: cover;
        opacity: 0.1;
        z-index: 0;
    }

    /* Estilo de los botones interactivos: se ponen grandes al seleccionarlos */
    div.stButton > button {
        background-color: #4b2c20 !important;
        color: white !important;
        border-radius: 25px !important;
        height: 3.5em !important;
        width: 100% !important;
        font-weight: bold !important;
        transition: all 0.4s ease-in-out !important;
        border: none !important;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
    }
    
    div.stButton > button:hover {
        transform: scale(1.08); /* Efecto de crecimiento solicitado */
        background-color: #6f4e37 !important;
        box-shadow: 0px 10px 20px rgba(0,0,0,0.3) !important;
        cursor: pointer;
    }

    /* Estilo de títulos */
    h1 {
        color: #4b2c20;
        font-family: 'Helvetica', sans-serif;
        text-align: center;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    
    .stMetric {
        background-color: white;
        padding: 15px;
        border-radius: 15px;
        box-shadow: 0px 4px 6px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# --- FUNCIONES DE CÁLCULO TÉCNICO ---
def calcular_metricas(pv, pt, tf, fc):
    try:
        m_f, s_f = map(int, tf.split(':'))
        m_c, s_c = map(int, fc.split(':'))
        sec_total = m_f * 60 + s_f
        sec_fc = m_c * 60 + s_c
        
        merma = ((pv - pt) / pv) * 100
        # DTR % = ((T. Total - T. First Crack) / T. Total) * 100
        dtr = ((sec_total - sec_fc) / sec_total) * 100
        return merma, dtr
    except:
        return None, None

# --- INTERFAZ DE USUARIO ---
st.markdown("<h1>☕ SABOR NACIONAL: OPTIMIZADOR DE TUESTE</h1>", unsafe_allow_html=True)
st.write("---")

# Layout centrado para el formulario
_, col_form, _ = st.columns([1, 2, 1])

with col_form:
    st.subheader("📝 Nuevo Registro de Tueste")
    lote = st.text_input("Nombre del Lote", placeholder="Ej: Santa Marta")
    
    c1, c2 = st.columns(2)
    peso_v = c1.number_input("Peso Verde (kg)", min_value=0.1, value=10.0, step=0.1)
    peso_t = c2.number_input("Peso Tostado (kg)", min_value=0.1, value=8.5, step=0.1)
    
    c3, c4 = st.columns(2)
    t_fc = c3.text_input("Tiempo First Crack (M:S)", value="13:50")
    t_fin = c4.text_input("Tiempo Saque (M:S)", value="15:30")

    if st.button("GUARDAR Y ANALIZAR"):
        m, d = calcular_metricas(peso_v, peso_t, t_fin, t_fc)
        
        if m is not None:
            # Mostrar métricas visuales atractivas
            res1, res2 = st.columns(2)
            res1.metric("MERMA", f"{m:.2f}%", delta=f"{m-15:.1f}% vs Ref")
            res2.metric("DTR (Desarrollo)", f"{d:.2f}%", delta=f"{d-20:.1f}% vs Ref")
            
            # Guardar en CSV para el historial
            archivo = 'historial_tuestes_sabor_nacional.csv'
            nuevo_dato = {
                'Fecha': datetime.now().strftime("%Y-%m-%d"),
                'Lote': lote,
                'Merma': round(m, 2),
                'DTR': round(d, 2)
            }
            df = pd.DataFrame([nuevo_dato])
            df.to_csv(archivo, mode='a', header=not os.path.exists(archivo), index=False)
            st.success("✅ ¡Lote registrado exitosamente!")
        else:
            st.error("❌ Error en el formato de tiempo. Usa Minutos:Segundos (ej. 13:50)")

# --- VISUALIZACIÓN DE DATOS HISTÓRICOS ---
st.write("---")
st.subheader("📊 Historial de Consistencia")

if os.path.exists('historial_tuestes_sabor_nacional.csv'):
    df_hist = pd.read_csv('historial_tuestes_sabor_nacional.csv')
    
    # Gráfica interactiva con estética de café
    fig = px.line(df_hist, x='Lote', y=['Merma', 'DTR'], 
                  title="Evolución de Calidad por Lote",
                  color_discrete_map={'Merma': '#4b2c20', 'DTR': '#d4a373'},
                  markers=True)
    
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)", 
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="#4b2c20"
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Mostrar tabla de datos para auditoría
    with st.expander("Ver tabla completa de registros"):
        st.dataframe(df_hist, use_container_width=True)
else:
    st.info("Aún no hay tuestes registrados. ¡Ingresa el primero arriba!")
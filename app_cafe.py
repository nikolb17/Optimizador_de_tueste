import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import os

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Sabor Nacional Optimizer", layout="wide")

# --- DISEÑO MULTIMEDIA (CSS PERSONALIZADO) ---
st.markdown("""
    <style>
    /* Fondo general con tonos crema */
    .main {
        background-color: #fdfaf5;
    }
    
    /* Imágenes laterales (Simuladas con bordes decorativos) */
    [data-testid="stAppViewContainer"]::before {
        content: "";
        position: fixed;
        top: 0; left: 0; width: 150px; height: 100%;
        background-image: url('https://images.unsplash.com/photo-1559056199-641a0ac8b55e?ixlib=rb-1.2.1&auto=format&fit=crop&w=300&q=80');
        background-size: cover;
        opacity: 0.15;
        z-index: 0;
    }
    
    [data-testid="stAppViewContainer"]::after {
        content: "";
        position: fixed;
        top: 0; right: 0; width: 150px; height: 100%;
        background-image: url('https://images.unsplash.com/photo-1580915411954-282cb1b0d780?ixlib=rb-1.2.1&auto=format&fit=crop&w=300&q=80');
        background-size: cover;
        opacity: 0.15;
        z-index: 0;
    }

    /* Estilo de los botones (Efecto de crecimiento al pasar el mouse) */
    div.stButton > button {
        background-color: #4b2c20 !important;
        color: white !important;
        border-radius: 20px !important;
        height: 3em !important;
        width: 100% !important;
        font-weight: bold !important;
        transition: all 0.3s ease-in-out !important;
        border: none !important;
    }
    
    div.stButton > button:hover {
        transform: scale(1.1); /* SE PONE GRANDE */
        background-color: #6f4e37 !important;
        box-shadow: 0px 10px 20px rgba(0,0,0,0.2) !important;
    }

    /* Títulos estilo Sabor Nacional */
    h1 {
        color: #4b2c20;
        font-family: 'Helvetica';
        text-align: center;
    }
    </style>
    """, unsafe_allow_stdio=True)

# --- LÓGICA DE CÁLCULO ---
def calcular_metricas(pv, pt, tf, fc):
    m_f, s_f = map(int, tf.split(':'))
    m_c, s_c = map(int, fc.split(':'))
    sec_total = m_f * 60 + s_f
    sec_fc = m_c * 60 + s_c
    
    merma = ((pv - pt) / pv) * 100
    dtr = ((sec_total - sec_fc) / sec_total) * 100
    return merma, dtr, sec_total

# --- INTERFAZ DE USUARIO ---
st.markdown("<h1>☕ SABOR NACIONAL: OPTIMIZADOR DE TUESTE</h1>", unsafe_allow_html=True)
st.write("---")

# Layout de columnas para centrar el formulario
col_img1, col_form, col_img2 = st.columns([1, 2, 1])

with col_form:
    st.subheader("📝 Registro del Lote")
    lote = st.text_input("Nombre del Lote", placeholder="Ej: Santa Marta Mayo")
    
    c1, c2 = st.columns(2)
    peso_v = c1.number_input("Peso Verde (kg)", min_value=0.1, value=10.0)
    peso_t = c2.number_input("Peso Tostado (kg)", min_value=0.1, value=8.5)
    
    c3, c4 = st.columns(2)
    t_fc = c3.text_input("Tiempo First Crack (M:S)", value="13:50")
    t_fin = c4.text_input("Tiempo Saque (M:S)", value="15:30")

    if st.button("CALCULAR Y GUARDAR REGISTRO"):
        m, d, st_total = calcular_metricas(peso_v, peso_t, t_fin, t_fc)
        
        # Mostrar Métricas Atractivas
        res1, res2 = st.columns(2)
        res1.metric("MERMA (%)", f"{m:.2f}%", delta=f"{m-15:.1f}% vs Ref")
        res2.metric("DTR (%)", f"{d:.2f}%", delta=f"{d-20:.1f}% vs Ref")
        
        # Guardar en CSV
        archivo = 'historial_tuestes_sabor_nacional.csv'
        nuevo_dato = {
            'Fecha': datetime.now().strftime("%Y-%m-%d"),
            'Lote': lote,
            'Merma': round(m, 2),
            'DTR': round(d, 2)
        }
        df = pd.DataFrame([nuevo_dato])
        df.to_csv(archivo, mode='a', header=not os.path.exists(archivo), index=False)
        st.success("¡Datos guardados con éxito!")

# --- GRÁFICAS VISUALES ---
st.write("---")
st.subheader("📈 Análisis de Consistencia")

if os.path.exists('historial_tuestes_sabor_nacional.csv'):
    df_hist = pd.read_csv('historial_tuestes_sabor_nacional.csv')
    
    # Gráfica interactiva con Plotly
    fig = px.line(df_hist, x='Lote', y=['Merma', 'DTR'], 
                  title="Tendencia de Calidad por Lote",
                  color_discrete_sequence=['#4b2c20', '#d4a373'],
                  markers=True)
    
    fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Aún no hay historial para mostrar gráficas.")
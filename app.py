{\rtf1\ansi\ansicpg1252\cocoartf2867
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 # -*- coding: utf-8 -*-\
import streamlit as st\
import pandas as pd\
import time\
\
# --- CONFIGURACI\'d3N DE LA P\'c1GINA ---\
st.set_page_config(page_title="ArgenCourier Cotizador", page_icon="\uc0\u55357 \u56550 ", layout="centered")\
\
# --- ESTILOS CSS ---\
st.markdown("""\
    <style>\
    .big-font \{ font-size:24px !important; font-weight: bold; color: #2E86C1; \}\
    .stButton>button \{ width: 100%; background-color: #2E86C1; color: white; \}\
    .result-box \{ background-color: #f0f2f6; padding: 20px; border-radius: 10px; border-left: 5px solid #2E86C1; \}\
    </style>\
    """, unsafe_allow_html=True)\
\
# --- 1. L\'d3GICA DE NEGOCIO & DATOS ---\
\
def get_carrier_rates(weight_kg, zone):\
    # Tarifas base ficticias para el ejemplo (USD)\
    base_fedex = 50 + (weight_kg * 12)\
    base_dhl = 45 + (weight_kg * 14)\
    \
    if zone == "USA/Canad\'e1":\
        multiplier = 1.0\
    elif zone == "Europa":\
        multiplier = 1.2\
    else:\
        multiplier = 1.5\
        \
    return \{\
        "FedEx": round(base_fedex * multiplier, 2),\
        "DHL": round(base_dhl * multiplier, 2)\
    \}\
\
def calculate_final_price(base_price, client_type):\
    if client_type == "P\'fablico General (C2C)":\
        margin = 0.40\
        fee = 5.0\
    elif client_type == "Partner E-commerce (B2B)":\
        margin = 0.20\
        fee = 2.0\
    elif client_type == "Cuenta VIP / Corporativo":\
        margin = 0.12\
        fee = 0.0\
    else:\
        margin = 0.30\
        fee = 3.0\
        \
    sell_price = (base_price * (1 + margin)) + fee\
    return round(sell_price, 2)\
\
# --- 2. INTERFAZ DE USUARIO (FRONTEND) ---\
\
st.title("\uc0\u9881 \u65039  Cotizador Inteligente v1.0")\
st.markdown("Calculadora de env\'edos internacionales con optimizaci\'f3n de tarifas.")\
\
# Sidebar\
with st.sidebar:\
    st.header("Configuraci\'f3n de Operador")\
    st.info("Panel interno de ArgenCourier.")\
    api_status = st.toggle("Simular Conexi\'f3n API", value=True)\
    if api_status:\
        st.success("APIs FedEx/DHL: ONLINE \uc0\u55357 \u57314 ")\
    else:\
        st.error("APIs Offline \uc0\u55357 \u56628 ")\
\
# Formulario\
col1, col2 = st.columns(2)\
\
with col1:\
    origin = st.selectbox("Origen", ["Buenos Aires (BUE)", "C\'f3rdoba (COR)", "Mendoza (MDZ)"])\
    destination_zone = st.selectbox("Zona de Destino", ["USA/Canad\'e1", "Europa", "Resto del Mundo"])\
\
with col2:\
    weight = st.number_input("Peso Real (kg)", min_value=0.1, value=1.0, step=0.5)\
    \
    st.markdown("---")\
    st.write("Dimensiones (cm)")\
    c1, c2, c3 = st.columns(3)\
    l = c1.number_input("Largo", value=0)\
    w = c2.number_input("Ancho", value=0)\
    h = c3.number_input("Alto", value=0)\
    \
    vol_weight = (l * w * h) / 5000\
    if vol_weight > weight:\
        st.warning(f"\uc0\u9888 \u65039  Peso Volum\'e9trico aplica: \{vol_weight\} kg")\
        final_weight = vol_weight\
    else:\
        final_weight = weight\
\
client_type = st.selectbox("Tipo de Cliente", ["P\'fablico General (C2C)", "Partner E-commerce (B2B)", "Cuenta VIP / Corporativo"])\
\
# Bot\'f3n\
if st.button("COTIZAR ENV\'cdO \uc0\u55357 \u56960 "):\
    with st.spinner('Consultando tarifas internacionales...'):\
        time.sleep(1)\
        \
        costs = get_carrier_rates(final_weight, destination_zone)\
        \
        price_fedex = calculate_final_price(costs["FedEx"], client_type)\
        price_dhl = calculate_final_price(costs["DHL"], client_type)\
        \
        best_option = "FedEx" if price_fedex < price_dhl else "DHL"\
        \
        st.markdown("### \uc0\u55357 \u56496  Opciones Disponibles")\
        \
        col_res1, col_res2 = st.columns(2)\
        \
        with col_res1:\
            is_best = best_option == 'FedEx'\
            st.markdown(f"""\
            <div class="result-box">\
                <h3>FedEx Priority</h3>\
                <p class="big-font">USD \{price_fedex\}</p>\
                <p style="color:grey; font-size:12px">Entrega: 2-3 d\'edas</p>\
                \{'<span style="background-color:#d4edda; color:#155724; padding:2px 5px; border-radius:3px;">\uc0\u11088  RECOMENDADO</span>' if is_best else ''\}\
            </div>\
            """, unsafe_allow_html=True)\
            \
        with col_res2:\
            is_best = best_option == 'DHL'\
            st.markdown(f"""\
            <div class="result-box">\
                <h3>DHL Express</h3>\
                <p class="big-font">USD \{price_dhl\}</p>\
                <p style="color:grey; font-size:12px">Entrega: 1-2 d\'edas</p>\
                 \{'<span style="background-color:#d4edda; color:#155724; padding:2px 5px; border-radius:3px;">\uc0\u11088  RECOMENDADO</span>' if is_best else ''\}\
            </div>\
            """, unsafe_allow_html=True)\
\
        with st.expander("\uc0\u55357 \u56592  Ver Desglose de Costos (Solo Admin)"):\
            st.write(f"**Costo Real FedEx:** USD \{costs['FedEx']\}")\
            st.write(f"**Costo Real DHL:** USD \{costs['DHL']\}")\
            st.write(f"**Tu Ganancia Neta:** USD \{round(price_fedex - costs['FedEx'], 2)\}")}
import streamlit as st
import utils.SQL.query as qq
from utils.SQL.conection import mysql_connector_connection, close_con_cur
import mysql.connector
import plotly.express as px
from utils.process import dashboard_p as p1
from utils.process import record_p as p3

# Set State
if "pagina" not in st.session_state:
    st.session_state.pagina = "menu"
if "subpagina" not in st.session_state:
    st.session_state.subpagina = None

def cambiar_pagina(pag):
    st.session_state.pagina = pag
    st.session_state.subpagina = None

def cambiar_subpagina(sub):
    st.session_state.subpagina = sub


# Main Menu
if st.session_state.pagina == "menu":
    st.title("Main menu")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("Dashboard"):
            cambiar_pagina("dashboard")

    with col2:
        if st.button("Table"):
            cambiar_pagina("ver_b")

    with col3:
        if st.button("Record data"):
            cambiar_pagina("record")


# Dashbaord tool
elif st.session_state.pagina == "dashboard":
    p1.dashboard()

    st.button("Volver", on_click=cambiar_pagina, args=("menu",))


# Table Tool
elif st.session_state.pagina == "ver_b":
    st.title("Visualización B")
    st.write("Aquí muestras datos tipo B")

    st.button("Volver", on_click=cambiar_pagina, args=("menu",))

# Record tool
elif st.session_state.pagina == "record":

    p3.record()

    st.button("Volver al menú", on_click=cambiar_pagina, args=("menu",))
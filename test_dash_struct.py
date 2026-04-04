import streamlit as st

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
    st.title("Menú principal")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("Dashboard"):
            cambiar_pagina("ver_a")

    with col2:
        if st.button("Table"):
            cambiar_pagina("ver_b")

    with col3:
        if st.button("Record data"):
            cambiar_pagina("registro")


# Dashbaord tool
elif st.session_state.pagina == "ver_a":
    st.title("Visualización A")
    st.write("Aquí muestras datos tipo A")

    st.button("Volver", on_click=cambiar_pagina, args=("menu",))


# Table Tool
elif st.session_state.pagina == "ver_b":
    st.title("Visualización B")
    st.write("Aquí muestras datos tipo B")

    st.button("Volver", on_click=cambiar_pagina, args=("menu",))


# Record tool
elif st.session_state.pagina == "registro":

    st.title("Registro de datos")

    # Submenú
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("Tipo 1"):
            cambiar_subpagina("tipo1")

    with col2:
        if st.button("Tipo 2"):
            cambiar_subpagina("tipo2")

    with col3:
        if st.button("Tipo 3"):
            cambiar_subpagina("tipo3")

    st.divider()

    # Contenido dinámico
    if st.session_state.subpagina == "tipo1":
        st.subheader("Registro Tipo 1")
        st.text_input("Nombre")
        st.number_input("Edad")
        st.button("Guardar")

    elif st.session_state.subpagina == "tipo2":
        st.subheader("Registro Tipo 2")
        st.text_input("Producto")
        st.number_input("Cantidad")
        st.button("Guardar")

    elif st.session_state.subpagina == "tipo3":
        st.subheader("Registro Tipo 3")
        st.date_input("Fecha")
        st.text_area("Notas")
        st.button("Guardar")

    st.button("Volver al menú", on_click=cambiar_pagina, args=("menu",))
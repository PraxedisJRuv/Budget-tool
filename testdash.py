import streamlit as st
import utils.SQL.query as qq
from utils.SQL.conection import mysql_connector_connection, close_con_cur
import mysql.connector

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
        import streamlit as st

        # Estado inicial
        if "fase" not in st.session_state:
            st.session_state.fase = "entrada"

        if "borrador" not in st.session_state:
            st.session_state.borrador = None

        if "n_registros" not in st.session_state:
            st.session_state.n_registros = 0


        # CAPTURA
        if st.session_state.fase == "entrada":

            st.subheader("Registro Tipo 1")

            with st.form("form_principal"):
                fecha = st.date_input("Fecha")
                valor = st.number_input("Valor")
                texto1 = st.text_input("Texto 1")
                texto2 = st.text_input("Texto 2")
                n = st.number_input("Cantidad de sub-registros", min_value=0, step=1)

                continuar = st.form_submit_button("Continuar")

                if continuar:
                    st.session_state.n_registros = int(n)
                    st.session_state.datos_principales = (fecha, valor, texto1, texto2, int(n))
                    st.session_state.fase = "subregistros"


        # SUBREGISTROS
        elif st.session_state.fase == "subregistros":

            st.write("Sub-registros")

            sub_datos = []

            with st.form("form_secundario"):

                for i in range(st.session_state.n_registros):
                    st.markdown(f"### Registro {i+1}")

                    s = st.text_input(f"Texto {i}", key=f"s_{i}")
                    f1 = st.number_input(f"Float 1 {i}", key=f"f1_{i}")
                    f2 = st.number_input(f"Float 2 {i}", key=f"f2_{i}")

                    sub_datos.append((s, f1, f2))

                revisar = st.form_submit_button("Revisar")

                if revisar:
                    st.session_state.borrador = (
                        st.session_state.datos_principales,
                        sub_datos
                    )
                    st.session_state.fase = "revision"


        # REVISIÓN Y EDICIÓN
        elif st.session_state.fase == "revision":

            st.subheader("Revisar y editar")

            datos_principales, sub_datos = st.session_state.borrador

            #Editar principales
            st.markdown("### Datos principales")

            fecha = st.date_input("Fecha", value=datos_principales[0])
            valor = st.number_input("Valor", value=datos_principales[1])
            texto1 = st.text_input("Texto 1", value=datos_principales[2])
            texto2 = st.text_input("Texto 2", value=datos_principales[3])
            n = datos_principales[4]

            nuevos_sub = []

            st.markdown("### Sub-registros")

            for i, (s_old, f1_old, f2_old) in enumerate(sub_datos):

                st.markdown(f"#### Registro {i+1}")

                s = st.text_input(f"Texto {i}", value=s_old, key=f"edit_s_{i}")
                f1 = st.number_input(f"Float 1 {i}", value=f1_old, key=f"edit_f1_{i}")
                f2 = st.number_input(f"Float 2 {i}", value=f2_old, key=f"edit_f2_{i}")

                nuevos_sub.append((s, f1, f2))

            col1, col2 = st.columns(2)

            with col1:
                if st.button("Volver a editar"):
                    st.session_state.fase = "entrada"

            with col2:
                if st.button("Confirmar y guardar"):
                    connection=mysql_connector_connection()
                    mycursor=connection.cursor()
                    values_buy=[(fecha,valor,texto1,texto2,n)]
                    qq.record_buy(values_buy,nuevos_sub,mycursor,connection)
                    close_con_cur(mycursor,connection)

                    st.success("Guardado")
                    st.write(values_buy,nuevos_sub)

                    # Reset opcional
                    st.session_state.fase = "entrada"
                    st.session_state.borrador = None

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
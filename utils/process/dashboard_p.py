import streamlit as st
import pandas as pd
import plotly.express as px
import utils.SQL.query as qq
from utils.SQL.conection import mysql_connector_connection
import utils.process.dataframe as daf
from utils.SQL.queries.load_queries import load_dict_query
import mysql.connector
from datetime import date

def dashboard():

    st.title("Dashboard financiero")

    # Selectors
    col1, col2 = st.columns(2)
    start = col1.date_input("Start", date(2025,1,1))
    end = col2.date_input("End", date.today())

    values=(start,end)

    if start and end:
        query=load_dict_query(r"utils/SQL/queries/filter_by_date.sql")


        df_exp=daf.get_datafame_wparam(query["Frequency_and_Amount_by_type_expense_bd"],values)
        df_income=daf.get_datafame_wparam(query["Frequency_and_Amount_by_type_income_bd"],values)

        connection=mysql_connector_connection()
        mycursor=connection.cursor()
        income = qq.get_query_value(values, query["Total_income_bd"],mycursor)
        expense = qq.get_query_value(values,query["Total_expense_bd"], mycursor)
        balance = income+expense

        col1, col2, col3 = st.columns(3)
        col1.metric("Ingresos", f"${income:,.2f}")
        col2.metric("Gastos", f"${expense:,.2f}")
        col3.metric("Balance", f"${balance:,.2f}")

        # Gráfico de barras (comparación)
        df_totales = pd.DataFrame({
            "Tipo": ["Ingresos", "Gastos", "Balance"],
            "Monto": [income, -(expense), balance]
        })

        fig_bar = px.bar(
            df_totales,
            x="Tipo",
            y="Monto",
            color="Tipo",
            title="Comparación",
            text="Monto"
        )

        fig_bar.update_traces(texttemplate='%{text:.2f}', textposition='outside')
        st.plotly_chart(fig_bar, use_container_width=True)

        #  Pie charts
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Gastos por concepto")
            if not df_exp.empty:
                fig_gastos = px.pie(
                    df_exp,
                    names="Concepto",
                    values="total",
                    title="Distribución de gastos",
                    hole=0.4  # donut opcional
                )
                st.plotly_chart(fig_gastos, use_container_width=True)
            else:
                st.info("No hay datos de gastos en este rango")

        with col2:
            st.subheader("Ingresos por concepto")
            if not df_income.empty:
                fig_ingresos = px.pie(
                    df_income,
                    names="Concepto",
                    values="total",
                    title="Distribución de ingresos",
                    hole=0.4
                )
                st.plotly_chart(fig_ingresos, use_container_width=True)
            else:
                st.info("No hay datos de ingresos en este rango")
import utils.SQL.query as qq
from utils.SQL.conection import mysql_connector_connection
import utils.process.dataframe as daf
from utils.SQL.queries.load_queries import load_dict_query
import mysql.connector
from datetime import date

config=mysql_connector_connection()
mycursor=config.cursor()

#values=[(date,amount,store,type,cantidad)]
start=date(2024,1,1)
end = date(2026,1,1)
#values=(start,end,start,end)
values=(start,end)
queries=load_dict_query(r"utils/SQL/queries/filter_by_date.sql")


a=qq.get_query_value(values,queries["Total_income_bd"],mycursor)

print(a[0])

df=daf.get_datafame_wparam(queries["Amount_type_expense_bd"],values)

print(df)
mycursor.close()
config.close()
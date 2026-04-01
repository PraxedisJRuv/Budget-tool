import utils.SQL.query as qq
from utils.SQL.conection import mysql_connector_connection
import mysql.connector

def init():
    config=mysql_connector_connection()
    mycursor=config.cursor()

    name="init.sql"
    qq.execute_sql_file(name,mycursor)

    mycursor.close()
    config.close()

def delete():
    config=mysql_connector_connection()
    mycursor=config.cursor()

    name="delete.sql"
    qq.execute_sql_file(name,mycursor)

    mycursor.close()
    config.close()

#init()
#delete()

from utils.SQL.queries.load_queries import load_dict_query
queries=load_dict_query("C:/Users/praxy/OneDrive/Escritorio/Progra/Budget_app/utils/SQL/queries/record_buy.sql")
print(queries)
print(queries["Add_buy"])
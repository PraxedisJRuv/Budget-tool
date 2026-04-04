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

from utils.process.dataframe import get_dataframe
query="SELECT * FROM producto"
df=get_dataframe(query)
print(df)
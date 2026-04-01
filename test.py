import utils.query as qq
from utils.conection import mysql_connector_connection
import mysql.connector

config=mysql_connector_connection()
mycursor=config.cursor()
sql = "INSERT INTO prueba (edad,conteo,gender,estado) VALUES(%s,%s,%s,%s)"
values=[(31,127.0,"femeino","vulnerable")]


qq.query_with_values(sql,values,mycursor,config)

mycursor.close()
config.close()
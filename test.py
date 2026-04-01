from utils.query import query_commit
from utils.conection import mysql_connector_connection
import mysql.connector

config=mysql_connector_connection()
mycursor=config.cursor()
sql = "UPDATE prueba SET estado = 'deteriorado' WHERE estado = 'en deterioro'"

query_commit(sql,mycursor,config)

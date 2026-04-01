import utils.SQL.query as qq
from utils.SQL.conection import mysql_connector_connection
import mysql.connector
from datetime import date

config=mysql_connector_connection()
mycursor=config.cursor()

#values=[(date,amount,store,type,cantidad)]
my_date=date(2010,12,8)
values_buy=[(my_date,235.22,"HEB","mandado",3)]

#values_product=[(Producto, Costo, Cantidad, IDcompra, IDgasto)]
values_product=[
    ("Manzana",35.22,1.22),
    ("Pene",100, 1),
    ("Putas",100,4)
]

qq.record_buy(values_buy,values_product,mycursor,config)

mycursor.close()
config.close()
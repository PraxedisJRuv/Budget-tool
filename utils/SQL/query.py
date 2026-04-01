import mysql.connector

def df_sqlalchemy(query, connection):
    import pandas as pd
    df=pd.read_sql(query, con=connection)
    return df

def query_with_values(query, values, cursor, connection):
    cursor.executemany(query, values)
    connection.commit()

def query_commit(query, cursor, connection):
    cursor.execute(query)
    connection.commit()

def execute_sql_file(name_file,cursor):
    #name_file="script.sql"
    with open(name_file,"r") as f:
        queries=f.read().split(";")
        for query in queries:
            if query.strip():
                cursor.execute(query)

def record_buy(values_buy,values_product, cursor, connection):
    query="INSERT INTO compras (Fecha, Monto, Comercio, Tipo, Cantidad_productos) VALUES (%s, %s, %s, %s,%s)"
    #values=[(date,amount,store,type,cantidad)]
    query_with_values(query, values_buy, cursor, connection)
    
    IDcompra=cursor.lastrowid
    query="INSERT INTO gastos (Fecha, Monto, Concepto) VALUES (%s, %s, %s)"
    values_aux=[(values_buy[0][0],values_buy[0][1],"compra")]
    query_with_values(query,values_aux,cursor,connection)
    IDgasto=cursor.lastrowid
    
    query="UPDATE compras SET ID_gasto = %s WHERE ID_compra = %s"
    values_aux=[(IDgasto,IDcompra)]
    query_with_values(query,values_aux,cursor,connection)

    #for i in range(cantidad): 
    #en general definir la función captura para productos
    for i in range(len(values_product)):
        aux_tuple=(*values_product[i],IDcompra,IDgasto)
        values_product[i]=aux_tuple

    query="INSERT INTO producto (Producto, Costo, Cantidad, ID_compra, ID_gasto) VALUES (%s, %s, %s, %s,%s)"
    #values_product=[(Producto, Costo, Cantidad, IDcompra, IDgasto)]
    query_with_values(query,values_product, cursor, connection)

    for i in range(len(values_product)):
        query = "INSERT INTO productos (Producto) SELECT %s WHERE NOT EXISTS (SELECT 1 FROM productos WHERE Producto = %s)"
        values=[(values_product[i][0],values_product[i][0])]
        query_with_values(query,values,cursor,connection)
    
    query="UPDATE producto p JOIN productos ps ON p.Producto=ps.Producto SET p.ID_producto=ps.ID_producto"
    query_commit(query, cursor,connection)

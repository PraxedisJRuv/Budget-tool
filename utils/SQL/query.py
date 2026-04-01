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
    from utils.SQL.queries.load_queries import load_dict_query
    queries=load_dict_query("utils/SQL/queries/record_buy.sql")
    #values=[(date,amount,store,type,cantidad)]
    query_with_values(queries["Add_buy"], values_buy, cursor, connection)
    
    IDcompra=cursor.lastrowid
    values_aux=[(values_buy[0][0],values_buy[0][1],"compra")]
    query_with_values(queries["Add_expense"],values_aux,cursor,connection)
    IDgasto=cursor.lastrowid
    
    values_aux=[(IDgasto,IDcompra)]
    query_with_values(queries["Update_IDexpense_in_buy"],values_aux,cursor,connection)

    #for i in range(cantidad): 
    #en general definir la función captura para productos
    for i in range(len(values_product)):
        aux_tuple=(*values_product[i],IDcompra,IDgasto)
        values_product[i]=aux_tuple

    #values_product=[(Producto, Costo, Cantidad, IDcompra, IDgasto)]
    query_with_values(queries["Update_productos_from_buy"],values_product, cursor, connection)

    for i in range(len(values_product)):
        values=[(values_product[i][0],values_product[i][0])]
        query_with_values(queries["Update_product_record"],values,cursor,connection)
    
    query_commit(queries["Update-product_IDs"], cursor,connection)

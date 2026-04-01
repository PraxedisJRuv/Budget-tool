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

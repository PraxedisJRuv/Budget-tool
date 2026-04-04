def sql_alchemy_connection():
    from sqlalchemy import create_engine
    
    connection_str = 'mysql+mysqlconnector://root:EsUnaPrueba123@localhost/hello_mysql'
    connection = create_engine(connection_str)
    
    return connection

def get_dataframe(query):
    import pandas as pd
    connection=sql_alchemy_connection()
    df = pd.read_sql(query, connection)
    connection.dispose()
    return df


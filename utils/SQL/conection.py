def sql_alchemy_connection():
    from sqlalchemy import create_engine
    
    connection_str = 'mysql+mysqlconnector://root:EsUnaPrueba123@localhost/hello_mysql'
    connection = create_engine(connection_str)
    
    return connection

def mysql_connector_connection():
    import mysql.connector
    
    config = mysql.connector.connect(
    host="localhost",
    user="root",
    password="EsUnaPrueba123",
    database="hello_mysql"
    )
    return config

def mysql_conncector_cursor():
    config=mysql_connector_connection()
    cursor=config.cursor()
    return cursor

def close_con_cur(cursor, connection):
    cursor.close()
    connection.close()
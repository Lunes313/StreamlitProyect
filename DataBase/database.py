import mysql.connector 
from mysql.connector import Error

def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            database='seminario'
        )
        if connection.is_connected():
            print('Conectado a la base de datos')
            return connection
    except Error as e:
        print("Error: {e}")
        return None
    
def close_connection(connection):
        if connection.is_connected():
            connection.close()

def create_user(connection,username,password,key):
     cursor = connection.cursor()
     sql="insert into usuarios(password,clave,usuario) values(%s,%s,%s)"
     val=(password,key,username,)
     cursor.execute(sql,val)
     connection.commit()
    
def delete_user(connection,username):
        cursor = connection.cursor()
        sql="delete from usuarios where usuario=%s"
        val=(username,)
        cursor.execute(sql,val)
        connection.commit()
     

import mysql.connector
from mysql.connector import Error

def create_connection():
    try: 
        connection=mysql.connector.connect(
            host='localhost',
            user='root',
            database='gestor'
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
       print('Desconectado a la base de datos')

def select_user(connection,username):
    cursor=connection.cursor()
    sql="select * from usuarios where username=%s"
    val=(username,)
    cursor.execute(sql,val)
    result=cursor.fetchall()
    if result: 
        return True
    else:
        return False
    
def create_user(connection, username, key, level, correo, contrasena):
    cursor = connection.cursor()
    sql = "INSERT INTO usuarios (username, keey, level, correo, password) VALUES (%s, %s, %s, %s, %s)"
    val = (username, key, level, correo, contrasena)
    cursor.execute(sql, val)
    connection.commit()



def select_users(connection):
    cursor=connection.cursor()
    sql="select * from usuarios"
    cursor.execute(sql)
    result=cursor.fetchall()
    return result

def update_password(connection,username,password):
    cursor=connection.cursor()
    sql="update usuarios set password=%s where username=%s"
    val=(password,username)
    cursor.execute(sql,val)
    connection.commit()
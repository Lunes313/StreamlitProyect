import mysql.connector
from mysql.connector import Error
import string
import random
from cryptography.fernet import Fernet
import time


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
    return True if result else False

def get_user(connection, username):
    cursor = connection.cursor()
    sql = "SELECT * FROM usuarios WHERE username=%s"
    val = (username,)
    cursor.execute(sql, val)
    result = cursor.fetchone()
    return result
def create_user(connection, username, key, level, correo, contrasena, clave):
    cursor = connection.cursor()
    sql = "INSERT INTO usuarios (username, keey, level, correo, password, clave) VALUES (%s, %s, %s, %s, %s, %s)"
    val = (username, key, level, correo, contrasena, clave)
    cursor.execute(sql, val)
    connection.commit()

def select_users(connection):
    cursor=connection.cursor()
    sql="select * from usuarios"
    cursor.execute(sql)
    result=cursor.fetchall()
    return result

def update_password(connection, username, password, key, keey):
    cursor = connection.cursor()
    sql = "UPDATE usuarios SET password=%s, clave=%s, keey=%s WHERE username=%s"
    val = (password, key, keey, username,)
    cursor.execute(sql, val)
    connection.commit()

def generar_contrasena():
    caracteres = string.ascii_letters + string.digits + string.punctuation
    contrasena = []
    for i in range(25):
        contrasena.append(random.choice(caracteres))
    return ''.join(contrasena)

def cifrar_contrasena(contrasena):
    key = Fernet.generate_key()
    cifrador = Fernet(key)
    contrasena_cifrada = cifrador.encrypt(contrasena.encode())
    return key, contrasena_cifrada

def descifrar_contrasena(key, contrasenaC):
    cifrado = Fernet(key)
    contrasenaDesC = cifrado.decrypt(contrasenaC).decode()
    return contrasenaDesC

def update_email_clave(connection, correo, keey):
    cursor = connection.cursor()
    sql = "update email set clave=%s where username=%s"
    val = (keey, correo)
    cursor.execute(sql, val)
    connection.commit()

def actualizar_contrasenas_periodicamente(connection):
    while True:
        if connection:
            usuarios = select_users(connection)
            for usuario in usuarios:
                username = usuario[0]
                correo=usuario[5]
                nueva_contrasena = generar_contrasena()
                key, contrasena = cifrar_contrasena(nueva_contrasena)
                keey = contrasena[10:16].decode('utf-8')
                update_password(connection, username, contrasena, key, keey)
                update_email_clave(connection, correo, keey)
                print(f"Contraseña actualizada para el usuario {username}")
        print("Esperando 3 minutos...")
        time.sleep(180)
        print("3 minutos han pasado.")

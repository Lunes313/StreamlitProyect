import mysql.connector
from mysql.connector import Error
import string
import random
from cryptography.fernet import Fernet
from datetime import datetime, timedelta
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
    now = datetime.now()
    sql = "INSERT INTO usuarios (username, keey, level, correo, password, clave, actualizacion) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    val = (username, key, level, correo, contrasena, clave, now)
    cursor.execute(sql, val)
    connection.commit()

def select_users(connection):
    cursor=connection.cursor()
    sql="select * from usuarios"
    cursor.execute(sql)
    result=cursor.fetchall()
    return result

def update_password(connection, username, password, key):
    cursor = connection.cursor()
    now = datetime.now()
    sql = "UPDATE usuarios SET password=%s, clave=%s, actualizacion=%s WHERE username=%s"
    val = (password, key, now, username)
    cursor.execute(sql, val)
    connection.commit()

def check_password_expiry(connection, username):
    cursor = connection.cursor()
    sql = "SELECT actualizacion FROM usuarios WHERE username=%s"
    val = (username,)
    cursor.execute(sql, val)
    result = cursor.fetchone()
    if result:
        actualizacion = result[0]
        if datetime.now() - actualizacion > timedelta(minutes=2):
            return True
    return False

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

def actualizar_contrasenas_periodicamente():
    while True:
        connection = create_connection()
        if connection:
            usuarios = select_users(connection)
            for usuario in usuarios:
                username = usuario[0]
                if check_password_expiry(connection, username):
                    nueva_contrasena = generar_contrasena()
                    key, contrasena_cifrada = cifrar_contrasena(nueva_contrasena)
                    update_password(connection, username, contrasena_cifrada, key)
                    print(f"Contraseña para {username} ha sido actualizada.")
        time.sleep(10)


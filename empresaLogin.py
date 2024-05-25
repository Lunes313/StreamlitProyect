import streamlit as st
import mysql.connector
from database import create_connection
import random
import socket

def get_network_name():
    try:
        hostname = socket.gethostname()
        network_name = socket.gethostbyname(hostname)
        return network_name
    except socket.error as e:
        print(f"Error al obtener el nombre de la red: {e}")
        return None

network_name = get_network_name()
if network_name:
    st.write(f"El dispositivo está conectado a la red: {network_name}")
else:
    st.write("No se pudo obtener el nombre de la red.")


def find_user(connection, username, key):
    cursor = connection.cursor()
    sql = "select * from usuarios where username=%s and keey=%s"
    val = (username, key)
    cursor.execute(sql, val)
    result = cursor.fetchall()
    if result:
        return result
    else:
        i = 1
        while i <= 5:
            username = f"{username}{i}"
            result = select_user(connection, username, key)
            if result:
                return result
            i += 1
        return False

def select_user(connection, username, key):
    cursor = connection.cursor()
    sql = "select * from usuarios where username=%s and keey=%s"
    val = (username,key)
    cursor.execute(sql, val)
    result = cursor.fetchall()
    if result:
        return result
    else:
        return False

def update_mensaje(connection, username, codigo):
    cursor = connection.cursor()
    sql = "update email set mensajes=%s where username=%s"
    val = (codigo, username)
    cursor.execute(sql, val)
    connection.commit()

# Inicializar el estado de la sesión
if "resultado" not in st.session_state:
    st.session_state.resultado = None
if "codigo" not in st.session_state:
    st.session_state.codigo = None
if "username" not in st.session_state:
    st.session_state.username = None
if "key" not in st.session_state:
    st.session_state.key = None

st.title("Inciar Sesion")
nombre_empleado = st.text_input("Ingresa tu Nombre Completo")
key = st.text_input("Ingresa tu key")
if st.button("Ingresar"):
    nombre_empleado_split = nombre_empleado.split(" ")
    if len(nombre_empleado_split) >= 4:
        username = nombre_empleado_split[0][0] + nombre_empleado_split[1][0] + nombre_empleado_split[2][
                                                                   0:len(nombre_empleado_split[1]) - 2] + \
                   nombre_empleado_split[3][0]
    elif len(nombre_empleado_split) == 3:
        username = nombre_empleado_split[0][0] + nombre_empleado_split[1][0:len(nombre_empleado_split[1]) - 1] + \
                   nombre_empleado_split[2][0]
    else:
        st.danger("Nombre de empleado no valido")

    st.session_state.codigo = random.randint(10000, 99999)
    st.session_state.username = username.lower()
    st.session_state.key = key

    connection = create_connection()
    if connection:
        resultado = find_user(connection, st.session_state.username, st.session_state.key)
    if resultado:
        st.session_state.resultado = resultado
        st.success(resultado)
        if resultado[0][5] == 0:
            st.success("Nivel de acceso bajo")
        elif resultado[0][5] == 1:
            st.success("Nivel de acceso medio")
            username_email = resultado[0][6]
            update_mensaje(connection, username_email, st.session_state.codigo)
        elif resultado[0][5] == 2:
            st.success("Nivel de acceso alto")
    else:
        st.error("Usuario o clave incorrecta")

# Verificación del código después de ingresar
if st.session_state.resultado:
    if st.session_state.resultado[0][5] == 1:
        codigo_email = st.text_input("Ingresa el codigo enviado a tu email")
        if st.button("Verificar"):
            if codigo_email == str(st.session_state.codigo):
                st.success("Código Correcto")
            else:
                st.error("Código incorrecto")


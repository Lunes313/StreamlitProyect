import streamlit as st
import pandas as pd
import mysql.connector
from database import create_connection, close_connection


def login(connection, username, password):
    cursor = connection.cursor()
    sql = "SELECT * FROM email WHERE username = %s AND password = %s"
    val = (username, password)
    cursor.execute(sql, val)
    result = cursor.fetchall()
    return result

def create_user(connection,username, password):
    cursor=connection.cursor()
    sql="insert into email(username,password) values(%s,%s)"
    val=(username,password,)
    cursor.execute(sql,val)
    connection.commit()


col1, col2 = st.columns(2)

with col1:
    st.title("Inicia Sesión")
    name_login = st.text_input("Ingresa tu usuario", key='nombre_input_col1')
    password_login = st.text_input("Ingresa tu contraseña", type='password', key='password_input_col1')
    if st.button("Iniciar Sesión"):
        connection = create_connection()
        resultado = login(connection, name_login, password_login)
        if resultado:
            st.success("¡Bienvenido!")
            url = "http://localhost:8510/?username={}".format(name_login)
            st.markdown("[Ir a la página de bienvenida](%s)" % url, unsafe_allow_html=True)
        else:
            st.error("¡Usuario o contraseña incorrectos!")
    
    

with col2:
    st.title("Regístrate")
    st.subheader("¿No tienes una cuenta?")
    name_register = st.text_input("Ingresa tu usuario", key='nombre_input_col2')
    password_register = st.text_input("Ingresa tu contraseña", type='password', key='password_input_col2')
    if st.button("Regístrate"):
        connection = create_connection()
        create_user(connection, name_register, password_register)
        st.success("¡Usuario creado exitosamente!")



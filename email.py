import streamlit as st
import mysql.connector 
from database import create_connection, close_connection

def mensaje(username):
    connection=create_connection()
    if connection:
        cursor=connection.cursor()
        sql="select * from email where username=%s"
        val=(username,)
        cursor.execute(sql,val)
        result=cursor.fetchall()
        return result
    else:
        return None

# Obtener los parámetros de la consulta de la URL
url_params = st.query_params
if "username" in url_params:
    username = url_params["username"]
    st.write("¡Bienvenido, {}!".format(username))
    username=format(username)
    st.write(username)
else:
    st.error("No se encontró el parámetro 'username' en la URL")

resultado=mensaje(username)
st.write("Ingresa el siguiente codigo de verificacion: ",resultado[0][2])
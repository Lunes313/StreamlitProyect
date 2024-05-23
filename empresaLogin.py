import streamlit as st
import mysql.connector
from database import create_connection
import random

def select_user(connection,username,key):
    cursor=connection.cursor()
    sql="select * from usuarios where username=%s and keey=%s"
    val=(username,key)
    cursor.execute(sql,val)
    result=cursor.fetchall()
    if result: 
        return result
    else:
        return False



st.title("Inciar Sesion")
nombre_empleado=st.text_input("Ingresa tu Nombre Completo")
key=st.text_input("Ingresa tu key")
if st.button("Ingresar"):
    nombre_empleado = nombre_empleado.split(" ")
    if(len(nombre_empleado)>=4):
        username=nombre_empleado[0][0]+nombre_empleado[1][0]+nombre_empleado[2][0:len(nombre_empleado[1])-2]+nombre_empleado[3][0]
    else:    
        username=nombre_empleado[0][0]+nombre_empleado[1][0:len(nombre_empleado[1])-1]+nombre_empleado[2][0]
           
        key=random.randint(1000,9999)
        username=username.lower()
        st.write(username)

    connection = create_connection()
    if connection:
        resultado=select_user(connection,username,key)
        if resultado:
            st.success(resultado)
            if resultado[4]==0:
                st.success("Nivel de acceso bajo")
            elif resultado[4]==1:
                st.success("Nivel de acceso medio")
        else:
            st.error("Usuario o clave incorrecta")
        
        
    

#Gerente
import streamlit as st
import mysql.connector
from database import create_connection, select_user, create_user, select_users
import random
import string
from cryptography.fernet import Fernet

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

def main():
    connection=create_connection()
    st.title("Bienvenido Gerente, Mateo")
    st.sidebar.title("Menu")
    option = st.sidebar.selectbox("Seleccionar Proceso",["Agregar Empleado","Consultar Empleado"])

    if option == "Agregar Empleado":
        st.subheader("Opcion: Agregar Empleado")
        nombre_empleado=st.text_input("Nombre Completo del Empleado: ")
        nivel=st.text_input("Nivel de acceso")
        correo=st.text_input("Correo de acceso")
        if st.button("Agregar"):
            nombre_empleado = nombre_empleado.split(" ")
            if(len(nombre_empleado)>=4):
                username=nombre_empleado[0][0]+nombre_empleado[1][0]+nombre_empleado[2][0:len(nombre_empleado[1])-2]+nombre_empleado[3][0]
            else:
                
                username=nombre_empleado[0][0]+nombre_empleado[1][0:len(nombre_empleado[1])-1]+nombre_empleado[2][0]
           
            key=random.randint(1000,9999)
            username=username.lower()

            result=select_user(connection,username)
            
            i=1
            while result==True:
                st.title("El usuario ya existe")
                username=username+str(i)
                i=i+1
                result=select_user(connection,username)
            
            create_user(connection,username,key,nivel,correo,)
            st.success("Record created successfully")

            st.title(username)
            st.title(key)
    elif option == "Consultar Empleado":
        st.subheader("Opcion: Consultar empleados")
        result=select_users(connection)
        for row in result:
            st.write(row)
        st.success("Record created successfully")


if __name__== '__main__':
    main()




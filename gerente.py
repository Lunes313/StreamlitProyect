import streamlit as st
import pandas as pd
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


def eliminar_usuario(connection, username):
    cursor = connection.cursor()
    sql = "DELETE FROM usuarios WHERE username = %s"
    val = (username,)
    cursor.execute(sql, val)
    connection.commit()


def main():
    connection = create_connection()
    st.title("Bienvenido Gerente, Mateo")
    st.sidebar.title("Menu")
    option = st.sidebar.selectbox("Seleccionar Proceso", ["Agregar Empleado", "Consultar Empleado"])

    if option == "Agregar Empleado":
        st.subheader("Opcion: Agregar Empleado")
        nombre_empleado = st.text_input("Nombre Completo del Empleado: ")
        nivel = st.text_input("Nivel de acceso")
        correo = st.text_input("Correo de acceso")
        if st.button("Agregar"):
            nombre_empleado = nombre_empleado.split(" ")
            if len(nombre_empleado) >= 4:
                username = nombre_empleado[0][0] + nombre_empleado[1][0] + nombre_empleado[2][
                                                                           0:len(nombre_empleado[1]) - 2] + \
                           nombre_empleado[3][0]
            elif len(nombre_empleado) == 3:
                username = nombre_empleado[0][0] + nombre_empleado[1][0:len(nombre_empleado[1]) - 1] + \
                           nombre_empleado[2][0]
            else:
                username = nombre_empleado[0][0] + nombre_empleado[1][0]

            key = random.randint(1000, 9999)
            username = username.lower()
            contrasena = generar_contrasena()

            result = select_user(connection, username)

            i = 1
            while result:
                st.warning("El usuario ya existe")
                username = username + str(i)
                i += 1
                result = select_user(connection, username)

            create_user(connection, username, key, nivel, correo, contrasena)
            st.success("Usuario creado exitosamente")

    elif option == "Consultar Empleado":
        st.subheader("Consulta de empleados")
        result = select_users(connection)
        df = pd.DataFrame(result, columns=["username", "password", "keey", "ip", "level", "correo"])
        df = df[["username", "keey", "level", "correo"]]
        col1, col2, col3, col4, col5 = st.columns(5)
        col1.write("**Usuario**")
        col2.write("**Key**")
        col3.write("**Nivel**")
        col4.write("**Correo**")
        col5.write("**Eliminar**")
        def render_row(row):
            col1, col2, col3, col4, col5 = st.columns(5)
            col1.write(row["username"])
            col2.write(row["keey"])
            col3.write(row["level"])
            col4.write(row["correo"])
            if col5.button("Eliminar", key=f"del_{row['username']}"):
                eliminar_usuario(connection, row["username"])
                st.experimental_rerun()

        df.apply(render_row, axis=1)

        st.success("Consulta completada exitosamente")


if __name__ == '__main__':
    main()
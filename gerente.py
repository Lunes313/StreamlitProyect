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
                st.danger("Nombre de empleado no valido")

            key = random.randint(1000000, 99999999)
            username = username.lower()
            clave, contrasena = cifrar_contrasena(generar_contrasena())

            result = select_user(connection, username)

            i = 1
            while result:
                username = f"{username}{i}"
                i += 1
                result = select_user(connection, username)

            create_user(connection, username, key, nivel, correo, contrasena, clave)
            st.success("Usuario creado exitosamente" + f" Usuario: {username}")

    elif option == "Consultar Empleado":
        st.subheader("Consulta de empleados")
        result = select_users(connection)
        df = pd.DataFrame(result, columns=["username","password", "clave", "keey", "ip", "level", "correo"])
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        col1.write("**Usuario**")
        col2.write("**Key**")
        col3.write("**Contraseña**")
        col4.write("**Correo**")
        col5.write("**Nivel**")
        col6.write("**Eliminar**")
        def render_row(row):
            col1, col2, col3, col4, col5, col6 = st.columns(6)
            col1.write(row["username"])
            col2.write(row["keey"])
            try:
                col3.write(descifrar_contrasena(row["clave"], row["password"]))
            except Exception as e:
                col3.write(f"Error: {e}")
            col4.write(row["correo"])
            col5.write(row["level"])
            if col6.button("Eliminar", key=f"del_{row['username']}"):
                eliminar_usuario(connection, row["username"])
                st.experimental_rerun()

        df.apply(render_row, axis=1)

        st.success("Consulta completada exitosamente")


if __name__ == '__main__':
    main()

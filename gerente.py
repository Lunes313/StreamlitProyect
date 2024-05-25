import streamlit as st
import pandas as pd
from database import create_connection
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
if not network_name:
    st.write("No se pudo obtener el nombre de la red.")
    

def created_IPS(connection, network_name):
    cursor = connection.cursor()
    sql = "INSERT INTO ips (ip) VALUES (%s)"
    val = (network_name,)
    cursor.execute(sql, val)
    connection.commit()
    

def select_IPS(connection):
    cursor = connection.cursor()
    sql = "SELECT * FROM ips"
    cursor.execute(sql)
    result = cursor.fetchall()
    return result

def eliminar_usuario(connection, ip):
    cursor = connection.cursor()
    sql = "DELETE FROM ips WHERE IP = %s"
    val = (ip,)
    cursor.execute(sql, val)
    connection.commit()

def select_IP(connection, ip):
    cursor = connection.cursor()
    sql = "SELECT * FROM ips WHERE ip = %s"
    val = (ip,)
    cursor.execute(sql, val)
    result = cursor.fetchall()
    return result

def main():
    connection = create_connection()
    st.title("Hola Gerente,Mateo")
    col1,col3=st.columns(2)

    with col1:
        st.sidebar.title("Tablas De IPS")
        result=select_IPS(connection)
        df = pd.DataFrame(result, columns=["IP"])
        col1, col2= st.columns(2)
        col1.write("**IP**")
        col2.write("**Eliminar**")
        def render_row(row):
            col1, col2= st.columns(2)
            col1.write(row["IP"])
            
            if col2.button("Eliminar", key=f"del_{row['IP']}"):
                eliminar_usuario(connection, row["IP"])
                st.experimental_rerun()
        df.apply(render_row, axis=1)

    with col3:
        ips=get_network_name()
        st.write("La IP que se tome de tu dispositivo es: "+ips)
    
        if st.button("Agregar"):
            result=select_IP(connection,ips)
            if result:
                st.error("La IP ya se encuentra registrada")
            else:
                st.write(created_IPS(connection,ips))
                st.success("La IP se ha agregado exitosamente")

if __name__ == '__main__':
    main()

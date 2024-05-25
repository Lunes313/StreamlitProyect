import streamlit as st
import subprocess
import threading
import mysql.connector
from database import actualizar_contrasenas_periodicamente, create_connection
def main():
    st.title("Menú de Navegación")

    # Menú desplegable para seleccionar la página
    paginas = {
        "Login Email": "loginEmail.py",
        "Empresa Login": "empresaLogin.py",
        "Gerente": "gerente.py",
        "ad":"administador.py"
        
    }

    seleccion = st.selectbox("Selecciona una página", [""] + list(paginas.keys()))

    if seleccion:
        seleccionP = paginas[seleccion]
        run(seleccionP)

def run(archivo):
    # Ejecutar el archivo seleccionado
    process = subprocess.Popen(['streamlit', 'run', archivo], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    if process.returncode == 0:
        st.success(f'Página {archivo} ejecutada exitosamente.')
    else:
        st.error(f'Error al ejecutar la página {archivo}.')
        st.error(stderr.decode())
connection = create_connection()
if __name__ == '__main__':
    main()
thread = threading.Thread(target=actualizar_contrasenas_periodicamente(connection))
thread.daemon = True
thread.start()
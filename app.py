import streamlit as st
import subprocess
def main():
    st.title("Menú de Navegación")

    # Menú desplegable para seleccionar la página
    paginas = {
        "login Email": "loginEmail.py",
        "empresa Login": "empresaLogin.py",
        "gerente": "gerente.py"
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

if __name__ == '__main__':
    main()

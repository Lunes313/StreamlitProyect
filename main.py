import streamlit as st
import random
import string

def generar_contrasena():
    caracteres = string.ascii_letters + string.digits + string.punctuation + string.whitespace
    contrasena = []
    for i in range(25):
        contrasena.append(random.choice(caracteres))
    return ''.join(contrasena)

def main():
    st.title('Generador de contraseñas seguras')
    if st.button('Generar nueva contraseña'):
        contrasena = generar_contrasena()
        st.write(contrasena)



if __name__ == '__main__':
    main()

import streamlit as st
import mysql.connector
from database import create_connection,close_connection,delete_user,create_user

#Establish connection to MySQL server

mybd=mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    database = 'seminario'
)

mycursor=mybd.cursor()

print("established connection")

#Create a Streamlit app

def main():
    st.title("Test Database Connection with Streamlit")
    #Display options for CRUD operations
    st.sidebar.title("CRUD Operations")
    option = st.sidebar.selectbox("Select Operation",["Create","Read","Update","Delete"])
    #Perfom select CRUD operations
    if option =="Create":
        st.subheader("Create a RECORD")
        name=st.text_input("Enter name")
        contasena=st.text_input("Contaseña")
        clave=st.text_input("Clave")

        if st.button("Create"):
           connection=create_connection()
           if connection:
               create_user(connection,name,contasena,clave)
               st.success("Record created successfully")
               close_connection(connection)

    elif option =="Read":
        sql="select * from usuarios"
        mycursor.execute(sql)
        result=mycursor.fetchall()
        for row in result:
            st.write(row)
        st.success("Record created successfully")
        st.subheader("Read a RECORD")

    elif option =="Update":
        st.subheader("Update a RECORD")
        clave=st.text_input("Enter clave")
        if st.button("Update"):
            sql="update usuarios set clave=%s where password=%s"
            val=(clave,1)
            mycursor.execute(sql,val)
            mybd.commit()
            st.success("Record updated successfully")
        
    elif option =="Delete":
        st.subheader("Delete a RECORD")
        name=st.text_input("Name")
        if st.button("Delete"):
           connection = create_connection()
           if connection:
               delete_user(connection,name)
               st.success("Record deleted successfully")
               close_connection(connection)
               


if __name__ == '__main__':
    main()
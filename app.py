
import streamlit as st
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

def main():

    st.title('Chatbot')
    chatbot = ChatBot('Chatty')
    trainer = ChatterBotCorpusTrainer(chatbot)
    trainer.train('chatterbot.corpus.spanish')
    mensaje = st.text_input('Escribe un mensaje:')
    respuesta = chatbot.get_response(mensaje)
    st.write(respuesta)


if __name__ == '__main__':
    main()
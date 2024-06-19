import streamlit as st

import base_langchain as lcb


st.title("Consultas de Emails")

question = st.sidebar.text_area(label="Faça uma pergunta")
# altere o diretório para o usuário correto
#directory = "./downloaded_emails/valderlan.nobre/"
if st.sidebar.button("Obter Resposta"):
    #response = lcb.get_insights(question, directory)
    response = lcb.get_insights(question)
    st.write("Resposta:", response)

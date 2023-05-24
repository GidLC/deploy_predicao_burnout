
#Importando Pacotes 
import pickle
import streamlit as st
import plotly.express as px
import datetime
import pandas as pd
import numpy as np
 
# Carregando a Máquina Preditiva
pickle_in = open('maquina_preditiva.pkl', 'rb') 
maquina_preditiva = pickle.load(pickle_in)

#Manter a sessão em cache 
@st.cache_data
# Criando a função que irá fazer a predição usando os dados impostados pelo usuário do Sistema 
def prediction(sexo, atuacao, home_office, fadiga_mental, dias):   
 
    # Pre-processando a entrada do Usuário    
    if sexo == "Masculino":
        sexo = 1
    else:
        sexo = 0
 
    if atuacao == "Servicos":
        atuacao = 1
    else:
        atuacao = 0
    
    if home_office == "Sim":
        home_office = 1
    else:
        home_office = 0

 
    # Fazendo Predições
    prediction = maquina_preditiva.predict( 
        [[sexo, atuacao, home_office, fadiga_mental, dias]])
     
    pred = prediction * 100

    return pred
      
  
# Essa função é para criação da webpage  
def main():

    with st.container():
        ##CABECALHO
        st.markdown("<h1 style='text-align: center; background-color: black; color: white;'>SVB <br><p>By: Gideone Costa e Gabriel Baumer<br></h1>", unsafe_allow_html=True)

        st.markdown("<h2 style='text-align: center;'>Sistema de Verificação de Burnout</h2>", unsafe_allow_html=True)

        st.markdown("Com esse sistema você passará algumas informações referentes ao seu trabalho e lhe informaremos de 0 a 100 qual o seu nível de Burnout")
      
    # Função do streamlit que faz o display da webpage
   ## st.markdown(fig, unsafe_allow_html = True) 
      
    # As linhas abaixo criam as caixas na qual o usuário vai entrar com dados da pessoa que quer o empréstimo para fazer a Predição
    sexo = st.selectbox('Sexo',("Masculino","Feminino"))
    atuacao = st.selectbox('Área de Atuação',("Servicos","Produtos"))  
    home_office = st.selectbox('Atua em Home Office',("Sim","Nao")) 
    fadiga = st.number_input("De 0 a 10 qual é o nível da sua fadiga mental?", min_value=0, max_value=10)

    data_contratacao_str = st.text_input("Quando você foi contratado? (DD/MM/YYYY)")

    try:
        data_contratacao = datetime.datetime.strptime(data_contratacao_str, '%d/%m/%Y')
        dias = (datetime.date.today() - data_contratacao.date()).days

    except ValueError:
        if data_contratacao_str == '':
            st.empty()
        else:
            st.error("Por favor, insira uma data válida no formato DD/MM/YYYY.")


    result =""
      
    #Quando o Usuário clicar no botão "Verificar" a Máquina Preditiva faz seu trabalho
    if st.button("Verificar"): 
        if data_contratacao.date() > datetime.date.today():
            st.error("A data da contratação não pode ser maior que a data atual")
        else:
            result = prediction(sexo, atuacao, home_office, fadiga, dias) 
            st.success('O seu nível de Burnout é de: {}'.format(result))
            ##print(type(result))
            print(result)
     
if __name__=='__main__': 
    main()

import streamlit as st
from pymongo import MongoClient
import pandas as pd

# Conexão com o banco de dados MongoDB
uri = "mongodb+srv://ciromenescal:clCS5dremGHkmrVx@cluster0.sowongv.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri)

# Função para inserir dados no banco de dados
def inserir_dados(nome, tem_figurinhas, quer_figurinhas):
    db = client.test_database  # Altere 'test_database' para o nome do seu banco de dados
    collection = db.test_collection  # Altere 'test_collection' para o nome da sua coleção
    collection.insert_one({
        "Nome": nome,
        "TemFigurinhas": tem_figurinhas,
        "QuerFigurinhas": quer_figurinhas
    })

# Função para retirar dados do banco de dados
def retirar_dados(nome):
    db = client.test_database  # Altere 'test_database' para o nome do seu banco de dados
    collection = db.test_collection  # Altere 'test_collection' para o nome da sua coleção
    collection.delete_one({"Nome": nome})

# Função para atualizar dados no banco de dados
def atualizar_dados(nome, novos_dados):
    db = client.test_database  # Altere 'test_database' para o nome do seu banco de dados
    collection = db.test_collection  # Altere 'test_collection' para o nome da sua coleção
    collection.update_one({"Nome": nome}, {"$set": novos_dados})

# Função para visualizar todos os dados no banco de dados
def visualizar_todos_dados():
    db = client.test_database  # Altere 'test_database' para o nome do seu banco de dados
    collection = db.test_collection  # Altere 'test_collection' para o nome da sua coleção
    cursor = collection.find()
    df = pd.DataFrame(list(cursor))
    return df

# Função para juntar quem tem e quem quer as mesmas figurinhas
def juntar_dados():
    db = client.test_database  # Altere 'test_database' para o nome do seu banco de dados
    collection = db.test_collection  # Altere 'test_collection' para o nome da sua coleção
    documents = collection.find().sort("Nome", 1)  # Ordena os documentos pelo nome em ordem ascendente
    
    quem_tem_com_quem_quer = {}
    
    for doc in documents:
        nome = doc["Nome"]
        quer_figurinhas = doc["QuerFigurinhas"]
        
        for figurinha in quer_figurinhas:
            pessoas_que_tem = []
            for outro_doc in collection.find():
                if outro_doc["Nome"] != nome and figurinha in outro_doc["TemFigurinhas"]:
                    pessoas_que_tem.append(outro_doc["Nome"])
            
            quem_tem_com_quem_quer.setdefault(figurinha, {"QuemQuer": nome, "QuemTem": pessoas_que_tem})
    
    return quem_tem_com_quem_quer



# Página principal do aplicativo
def main():
    st.title("Aplicativo para Gerenciar Dados no MongoDB")

    # Formulário para adicionar dados
    st.subheader("Adicionar Dados")
    nome = st.text_input("Nome")
    tem_figurinhas = st.text_input("Número das Figurinhas que Você Tem (separadas por vírgula)")
    quer_figurinhas = st.text_input("Número das Figurinhas que Você Quer (separadas por vírgula)")
    if st.button("Adicionar"):
        tem_figurinhas = [int(x.strip()) for x in tem_figurinhas.split(",")]
        quer_figurinhas = [int(x.strip()) for x in quer_figurinhas.split(",")]
        inserir_dados(nome, tem_figurinhas, quer_figurinhas)
        st.success("Dados inseridos com sucesso!")

    # Botão para visualizar todos os dados
    st.subheader("Visualizar Todos os Dados")
    if st.button("Visualizar Todos os Dados"):
        df = visualizar_todos_dados()
        st.write(df)

    # Botão para juntar quem tem e quem quer as figurinhas
    st.subheader("Juntar Dados")
    if st.button("Juntar Dados"):
        dados_juntos = juntar_dados()
        st.subheader("Quem Tem e Quem Quer as Figurinhas:")
        for figurinha, dados in dados_juntos.items():
            st.write(f"Figurinha {figurinha}:")
            st.write(f"  {dados['QuemQuer']} quer a figurinha.")
            if dados['QuemTem']:
                st.write(f"  Quem tem: {', '.join(dados['QuemTem'])}")
            else:
                st.write("  Ninguém tem esta figurinha.")


    # Formulário para retirar dados
    st.subheader("Retirar Dados")
    nome_para_retirar = st.text_input("Nome do Registro para Retirar")
    if st.button("Retirar"):
        retirar_dados(nome_para_retirar)
        st.success(f"Dados do registro '{nome_para_retirar}' retirados com sucesso!")

    # Formulário para atualizar dados
    st.subheader("Atualizar Dados")
    nome_para_atualizar = st.text_input("Nome do Registro para Atualizar")
    tem_figurinhas_atualizado = st.text_input("Novo Número das Figurinhas que Você Tem (separadas por vírgula)")
    quer_figurinhas_atualizado = st.text_input("Novo Número das Figurinhas que Você Quer (separadas por vírgula)")
    if st.button("Atualizar"):
        tem_figurinhas_atualizado = [int(x.strip()) for x in tem_figurinhas_atualizado.split(",")]
        quer_figurinhas_atualizado = [int(x.strip()) for x in quer_figurinhas_atualizado.split(",")]
        atualizar_dados(nome_para_atualizar, {"TemFigurinhas": tem_figurinhas_atualizado, "QuerFigurinhas": quer_figurinhas_atualizado})
        st.success(f"Dados do registro '{nome_para_atualizar}' atualizados com sucesso!")

if __name__ == "__main__":
    main()

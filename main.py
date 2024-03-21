import streamlit as st
from pymongo import MongoClient
import pandas as pd

db_username = st.secrets["DB_USERNAME"]
db_token = st.secrets["DB_TOKEN"]

# Conexão com o banco de dados MongoDB
uri = f"mongodb+srv://{db_username}:{db_token}@cluster0.sowongv.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
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

# Função para ordenar cada lista individualmente
def ordenar_lista(lista):
    return sorted(lista)

# Função para visualizar todos os dados no banco de dados
def visualizar_todos_dados():
    db = client.test_database  # Altere 'test_database' para o nome do seu banco de dados
    collection = db.test_collection  # Altere 'test_collection' para o nome da sua coleção
    cursor = collection.find()
    df = pd.DataFrame(list(cursor))
    df = df.drop('_id', axis=1)
    df['TemFigurinhas'] = df['TemFigurinhas'].apply(ordenar_lista)
    df['QuerFigurinhas'] = df['QuerFigurinhas'].apply(ordenar_lista)
    return df

# Função para juntar quem tem e quem quer as mesmas figurinhas
def juntar_dados():
    db = client.test_database  # Altere 'test_database' para o nome do seu banco de dados
    collection = db.test_collection  # Altere 'test_collection' para o nome da sua coleção
    documents = collection.find().sort("Nome", 1)  # Ordena os documentos pelo nome em ordem ascendente
    
    quem_tem_e_quer = {f'Figurinha {i}': {'QuemTem': [], 'QuemQuer': []} for i in range(1, 51)}
    
    for doc in documents:
        nome = doc["Nome"]
        tem_figurinhas = doc["TemFigurinhas"]
        quer_figurinhas = doc["QuerFigurinhas"]
        
        for figurinha in tem_figurinhas:
            quem_tem_e_quer[f'Figurinha {figurinha}']['QuemTem'].append(nome)
        
        for figurinha in quer_figurinhas:
            quem_tem_e_quer[f'Figurinha {figurinha}']['QuemQuer'].append(nome)
    
    return quem_tem_e_quer

# Função para adicionar novas figurinhas ao array TemFigurinhas
def adicionar_figurinhas(nome, novas_figurinhas):
    db = client.test_database  # Altere 'test_database' para o nome do seu banco de dados
    collection = db.test_collection  # Altere 'test_collection' para o nome da sua coleção
    novas_figurinhas = [int(x.strip()) for x in novas_figurinhas.split(",")]
    collection.update_one({"Nome": nome}, {"$push": {"TemFigurinhas": {"$each": novas_figurinhas}}})
    st.success(f"Figurinhas {novas_figurinhas} adicionadas para {nome} com sucesso!")

# Função para remover figurinhas do array QuerFigurinhas
def remover_figurinhas(nome, figurinhas_remover):
    db = client.test_database  # Altere 'test_database' para o nome do seu banco de dados
    collection = db.test_collection  # Altere 'test_collection' para o nome da sua coleção
    figurinhas_remover = [int(x.strip()) for x in figurinhas_remover.split(",")]
    collection.update_one({"Nome": nome}, {"$pull": {"QuerFigurinhas": {"$in": figurinhas_remover}}})
    st.success(f"Figurinhas {figurinhas_remover} removidas para {nome} com sucesso!")


# Página principal do aplicativo
def main():
    st.title("Aplicativo para Trocar Figurinhas LegendsROO! ")

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
    st.subheader("Juntar Figurinhas")
    if st.button("Juntar Figurinhas"):
        dados_juntos = juntar_dados()
        st.subheader("Quem Tem e Quem Quer as Figurinhas:")
        for figurinha, dados in dados_juntos.items():
            st.write(f"**{figurinha}:**")
            st.write(f"  Quem tem: {', '.join(dados['QuemTem'])}")
            st.write(f"  Quem quer: {', '.join(dados['QuemQuer'])}")

    # Formulário para adicionar uma nova figurinha ao TemFigurinhas
    st.subheader("Adicionar Nova Figurinha ao TemFigurinhas")
    nome_adicionar_figurinha = st.text_input("Nome do Registro para Adicionar Figurinha")
    nova_figurinha = st.text_input("Nova Figurinha a ser Adicionada")
    if st.button("Adicionar Figurinha"):
        adicionar_figurinhas(nome_adicionar_figurinha, nova_figurinha)

    # Formulário para remover uma figurinha do QuerFigurinhas
    st.subheader("Remover Figurinha do QuerFigurinhas")
    nome_remover_figurinha = st.text_input("Nome do Registro para Remover Figurinha")
    figurinha_remover = st.text_input("Figurinha a ser Removida")
    if st.button("Remover Figurinha"):
        remover_figurinhas(nome_remover_figurinha, figurinha_remover)
    
    # Formulário para retirar dados
    st.subheader("Retirar Dados - Utilizar nome cadastrado!")
    nome_para_retirar = st.text_input("Nome do Registro para Retirar")
    if st.button("Retirar"):
        retirar_dados(nome_para_retirar)
        st.success(f"Dados do registro '{nome_para_retirar}' retirados com sucesso!")


if __name__ == "__main__":
    main()

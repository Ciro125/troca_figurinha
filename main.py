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

# Função para adicionar número à lista TemFigurinha
def adicionar_figurinha(nome, numero_figurinha):
    # Conectar ao banco de dados MongoDB
    client = MongoClient(uri)
    db = client.test_database  # Substitua "test_database" pelo nome do seu banco de dados
    collection = db.test_collection  # Substitua "test_collection" pelo nome da sua coleção
    
    # Verificar se o nome já existe no banco de dados
    if collection.find_one({"Nome": nome}):
        # Atualizar documento adicionando o número da figurinha à lista TemFigurinha
        collection.update_one({"Nome": nome}, {"$addToSet": {"TemFigurinhas": numero_figurinha}})
        st.success(f"Figurinha {numero_figurinha} adicionada para {nome}.")
    else:
        st.error(f"Não foi possível adicionar a figurinha para {nome}. O nome não foi encontrado no banco de dados.")

    # Fechar conexão com o banco de dados
    client.close()

# Função para remover número da lista QuerFigurinha
def remover_figurinha(nome, numero_figurinha):
    # Conectar ao banco de dados MongoDB
    client = MongoClient(uri)
    db = client.test_database  # Substitua "test_database" pelo nome do seu banco de dados
    collection = db.test_collection  # Substitua "test_collection" pelo nome da sua coleção
    
    # Verificar se o nome já existe no banco de dados
    if collection.find_one({"Nome": nome}):
        # Atualizar documento removendo o número da figurinha da lista QuerFigurinhas
        collection.update_one({"Nome": nome}, {"$pull": {"QuerFigurinhas": numero_figurinha}})
        st.success(f"Figurinha {numero_figurinha} removida para {nome}.")
    else:
        st.error(f"Não foi possível remover a figurinha para {nome}. O nome não foi encontrado no banco de dados.")
    
    # Fechar conexão com o banco de dados
    client.close()

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

    # Formulário para adicionar ou remover figurinhas
    st.subheader("Adicionar ou Remover Figurinhas")
    
    # Campo de entrada para o nome
    nome = st.text_input("Nome:")
    
    # Campo de entrada para o número da figurinha
    numero_figurinha = st.number_input("Número da Figurinha:", min_value=1, max_value=50, step=1)
    
    # Opções para adicionar ou remover figurinhas
    opcao = st.radio("Selecione uma opção:", ["Adicionar Figurinha (Tenho uma figurinha nova!)", "Remover Figurinha (Consegui trocar uma figurinha!)"])
    
    # Botão para executar a ação selecionada
    if st.button("Executar"):
        if opcao == "Adicionar Figurinha":
            adicionar_figurinha(nome, numero_figurinha)
            st.success(f"Figurinha {numero_figurinha} adicionada para {nome}.")
        elif opcao == "Remover Figurinha":
            remover_figurinha(nome, numero_figurinha)
            st.success(f"Figurinha {numero_figurinha} removida para {nome}.")

    # Formulário para retirar dados
    st.subheader("Retirar Dados - Utilizar nome cadastrado!")
    nome_para_retirar = st.text_input("Nome do Registro para Retirar")
    if st.button("Retirar"):
        retirar_dados(nome_para_retirar)
        st.success(f"Dados do registro '{nome_para_retirar}' retirados com sucesso!")


if __name__ == "__main__":
    main()

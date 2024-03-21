import streamlit as st

# Função para encontrar correspondências de figurinhas
def encontrar_correspondencias(usuarios):
    correspondencias = {}

    for nome1, dados1 in usuarios.items():
        for nome2, dados2 in usuarios.items():
            if nome1 != nome2:  # Garante que não estamos comparando o mesmo usuário
                figurinhas_troca = dados1['tem'] & dados2['precisa']
                if figurinhas_troca:
                    if nome1 in correspondencias:
                        correspondencias[nome1][nome2] = figurinhas_troca
                    else:
                        correspondencias[nome1] = {nome2: figurinhas_troca}

    return correspondencias

def main():
    st.title("Troca de Figurinhas")

    st.write("Insira os dados dos usuários:")

    usuarios = {}
    i = 0  # Identificador único para cada widget
    while True:
        i += 1
        nome = st.text_input(f"Nome do usuário {i}:")
        tem = st.text_input(f"Figurinhas que {nome} possui (separe por vírgula):", key=f"figurinhas_tem_{i}")
        precisa = st.text_input(f"Figurinhas que {nome} precisa (separe por vírgula):", key=f"figurinhas_precisa_{i}")
        if nome and tem and precisa:
            usuarios[nome] = {'tem': set([int(figurinha.strip()) for figurinha in tem.split(",")]),
                              'precisa': set([int(figurinha.strip()) for figurinha in precisa.split(",")])}
        else:
            break

    if usuarios:
        if st.button("Encontrar Correspondências"):
            correspondencias = encontrar_correspondencias(usuarios)

            st.write("Correspondências encontradas:")
            for nome1, amigos in correspondencias.items():
                for nome2, figurinhas_troca in amigos.items():
                    figurinhas_str = ", ".join(str(figurinha) for figurinha in figurinhas_troca)
                    st.write(f"{nome1} e {nome2} podem trocar as seguintes figurinhas: {figurinhas_str}")

if __name__ == "__main__":
    main()

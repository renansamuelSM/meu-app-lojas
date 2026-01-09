import streamlit as st
import pandas as pd
import os

# 1. Configuração da Página
st.set_page_config(page_title="Busca Filial", page_icon="🔍", layout="centered")

# 2. CSS para o Visual Dark e o Botão HTML
st.markdown("""
    <style>
    #MainMenu, footer, header {visibility: hidden;}
    .stApp { background-color: #000000; }
    
    .stTextInput>div>div>input {
        background-color: #1a1a1a; color: white !important; border: 1px solid #333;
        border-radius: 5px; font-size: 20px; padding: 10px;
    }

    .caixa-resultado {
        background-color: #ffffff; padding: 25px; border-radius: 15px;
        text-align: center; margin-top: 20px; margin-bottom: 20px;
    }

    .cnpj-texto {
        font-size: 48px; font-weight: 800; color: #000000 !important;
        margin: 0; letter-spacing: -1px;
    }
    
    .legenda-preta { color: #666666 !important; font-size: 14px; margin-bottom: 5px; font-weight: bold; }

    /* Estilo do nosso novo botão HTML */
    .botao-container {
        display: flex;
        justify-content: center;
        width: 100%;
    }

    .meu-botao-copiar {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: none !important;
        width: 300px !important;
        height: 55px !important;
        border-radius: 10px !important;
        font-weight: bold !important;
        font-size: 18px !important;
        cursor: pointer;
        transition: 0.3s;
    }

    .meu-botao-copiar:hover {
        background-color: #dddddd !important;
    }

    /* Balão de aviso */
    [data-testid="stToast"] {
        background-color: #ffffff !important;
        border: 2px solid #1f77b4 !important;
    }
    [data-testid="stToast"] div p {
        color: #000000 !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.write("### 🔍 Consultar Filial")

NOME_ARQUIVO = "pasta_teste.xlsx"

if os.path.exists(NOME_ARQUIVO):
    @st.cache_data
    def carregar_dados():
        return pd.read_excel(NOME_ARQUIVO, engine='openpyxl')
    
    df = carregar_dados()
    busca = st.text_input("Busca", placeholder="Digite o código...", label_visibility="collapsed")

    if busca:
        col_filial = df.columns[0]
        col_cnpj = df.columns[1]
        resultado = df[df[col_filial].astype(str).str.strip() == str(busca).strip()]

        if not resultado.empty:
            cnpj = str(resultado.iloc[0][col_cnpj])
            
            # 1. Mostra o Card Branco
            st.markdown(f"""
                <div class="caixa-resultado">
                    <p class="legenda-preta">CNPJ ENCONTRADO</p>
                    <p class="cnpj-texto">{cnpj}</p>
                </div>
                """, unsafe_allow_html=True)

            # 2. BOTÃO DE CÓPIA REAL (HTML + JAVASCRIPT)
            # Esse botão ignora o servidor do Streamlit e fala direto com o seu navegador
            st.components.v1.html(f"""
                <div style="display: flex; justify-content: center; width: 100%;">
                    <button id="btnCopiar" class="meu-botao-copiar" 
                        style="background-color: white; color: black; border: none; 
                        width: 300px; height: 55px; border-radius: 10px; 
                        font-weight: bold; font-size: 18px; cursor: pointer;">
                        COPIAR CNPJ
                    </button>
                </div>

                <script>
                document.getElementById('btnCopiar').addEventListener('click', function() {{
                    const texto = "{cnpj}";
                    navigator.clipboard.writeText(texto).then(function() {{
                        // Avisa o usuário que funcionou mudando a cor do botão por um segundo
                        const btn = document.getElementById('btnCopiar');
                        btn.style.backgroundColor = '#4CAF50';
                        btn.style.color = 'white';
                        btn.innerText = 'COPIADO!';
                        setTimeout(() => {{
                            btn.style.backgroundColor = 'white';
                            btn.style.color = 'black';
                            btn.innerText = 'COPIAR CNPJ';
                        }}, 1000);
                    }});
                }});
                </script>
            """, height=70)
            
        else:
            st.error("Filial não encontrada.")
else:
    st.warning("Arquivo 'pasta_teste.xlsx' não encontrado.")
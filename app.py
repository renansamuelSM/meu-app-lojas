import streamlit as st
import pandas as pd
import os

# 1. Configuração da Página
st.set_page_config(page_title="Busca Filial", page_icon="🔍", layout="centered")

# 2. CSS para o Visual Dark e o Botão HTML
st.markdown("""
    <style>
    #MainMenu, footer, header {visibility: hidden;}
    .stApp { background-color: #339900; }
    
    .stTextInput>div>div>input {
        background-color: #xxxxxx; color: black !important; border: 1px solid #333;
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

    .meu-botao-copiar {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 2px solid #333 !important;
        width: 300px !important;
        height: 55px !important;
        border-radius: 10px !important;
        font-weight: bold !important;
        font-size: 18px !important;
        cursor: pointer;
        transition: 0.3s;
    }
    </style>
    """, unsafe_allow_html=True)

st.write("### 🔍 Consultar Filial")

NOME_ARQUIVO = "pasta_teste.xlsx"

if os.path.exists(NOME_ARQUIVO):
    @st.cache_data
    def carregar_dados():
        # Lendo de forma simples, sem motores complexos
        return pd.read_excel(NOME_ARQUIVO)
    
    df = carregar_dados()
    busca = st.text_input("Busca", placeholder="Digite o código...", label_visibility="collapsed")

    if busca:
        col_filial = df.columns[0] # Primeira coluna (Filial)
        col_cnpj = df.columns[1]   # Segunda coluna (CNPJ)
        
        # Filtra os dados
        resultado = df[df[col_filial].astype(str).str.strip() == str(busca).strip()]

        if not resultado.empty:
            cnpj = str(resultado.iloc[0][col_cnpj])
            
            # Mostra o Card Branco
            st.markdown(f"""
                <div class="caixa-resultado">
                    <p class="legenda-preta">CNPJ ENCONTRADO</p>
                    <p class="cnpj-texto">{cnpj}</p>
                </div>
                """, unsafe_allow_html=True)

            # Botão de Cópia via JavaScript
            st.components.v1.html(f"""
                <div style="display: flex; justify-content: center; width: 100%;">
                    <button id="btnCopiar" style="background-color: white; color: black; border: 2px solid #333; 
                        width: 300px; height: 55px; border-radius: 10px; font-weight: bold; font-size: 18px; cursor: pointer;">
                        COPIAR CNPJ
                    </button>
                </div>
                <script>
                document.getElementById('btnCopiar').addEventListener('click', function() {{
                    const texto = "{cnpj}";
                    navigator.clipboard.writeText(texto).then(function() {{
                        const btn = document.getElementById('btnCopiar');
                        btn.style.backgroundColor = '#000'; btn.style.color = '#fff'; btn.innerText = 'COPIADO!';
                        setTimeout(() => {{
                            btn.style.backgroundColor = 'white'; btn.style.color = 'black'; btn.innerText = 'COPIAR CNPJ';
                        }}, 1000);
                    }});
                }});
                </script>
            """, height=70)
            
        else:
            st.error("Filial não encontrada.")
else:

    st.warning("Arquivo 'pasta_teste.xlsx' não encontrado na pasta.")




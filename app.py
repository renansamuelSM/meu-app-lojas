import streamlit as st
import pandas as pd
import os

# 1. Configuração da Página
st.set_page_config(page_title="Busca Filial", page_icon="🔍", layout="centered")

# 2. CSS Original (Mantido exatamente como você enviou)
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
        text-align: center; margin-top: 20px; margin-bottom: 10px;
    }

    .cnpj-texto {
        font-size: 42px; font-weight: 800; color: #000000 !important;
        margin: 0; letter-spacing: -1px;
    }
    
    .legenda-preta { color: #666666 !important; font-size: 14px; margin-bottom: 5px; font-weight: bold; }

    .grid-info { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; text-align: left; margin-top: 15px; border-top: 1px solid #eee; padding-top: 15px; }
    .item-info { padding: 5px; }
    .valor-preto { color: #000000 !important; font-size: 18px; font-weight: 600; margin: 0; }

    .meu-botao-copiar {
        background-color: #ffffff !important; color: #000000 !important;
        border: 2px solid #333 !important; width: 300px !important; height: 55px !important;
        border-radius: 10px !important; font-weight: bold !important;
        font-size: 18px !important; cursor: pointer; transition: 0.3s;
    }
    </style>
    """, unsafe_allow_html=True)

st.write("### 🔍 Consultar Filial")

NOME_ARQUIVO = "pasta_teste.xlsx"

# Função auxiliar para evitar o erro de campos vazios (NaN)
def formatar_valor(valor):
    if pd.isna(valor) or str(valor).lower() == 'nan':
        return "Não informado"
    return str(valor).strip()

if os.path.exists(NOME_ARQUIVO):
    @st.cache_data
    def carregar_dados():
        # engine='openpyxl' às vezes falha com estilos, por isso deixamos o pandas escolher o melhor motor
        df_lido = pd.read_excel(NOME_ARQUIVO)
        # Limpa espaços nos nomes das colunas
        df_lido.columns = [str(c).strip() for c in df_lido.columns]
        return df_lido
    
    df = carregar_dados()
    busca = st.text_input("Busca", placeholder="Digite o código...", label_visibility="collapsed")

    if busca:
        col_filial = df.columns[0]
        # Busca a filial
        resultado = df[df[col_filial].astype(str).str.strip() == str(busca).strip()]

        if not resultado.empty:
            # Pegando os dados com segurança usando a função de formatação
            cnpj = formatar_valor(resultado.iloc[0].get('CNPJ'))
            ie = formatar_valor(resultado.iloc[0].get('Inscrição estadual'))
            celular = formatar_valor(resultado.iloc[0].get('Celular'))
            telefone = formatar_valor(resultado.iloc[0].get('Telefone'))
            
            # 1. Card Branco com todas as informações
            st.markdown(f"""
                <div class="caixa-resultado">
                    <p class="legenda-preta">CNPJ ENCONTRADO</p>
                    <p class="cnpj-texto">{cnpj}</p>
                    
                    <div class="grid-info">
                        <div class="item-info">
                            <p class="legenda-preta">I.E.</p>
                            <p class="valor-preto">{ie}</p>
                        </div>
                        <div class="item-info">
                            <p class="legenda-preta">CELULAR</p>
                            <p class="valor-preto">{celular}</p>
                        </div>
                        <div class="item-info" style="grid-column: span 2;">
                            <p class="legenda-preta">TELEFONE</p>
                            <p class="valor-preto">{telefone}</p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # 2. BOTÃO DE CÓPIA (HTML + JS)
            st.components.v1.html(f"""
                <div style="display: flex; justify-content: center; width: 100%;">
                    <button id="btnCopiar" style="background-color: white; color: black; border: 2px solid #333; 
                        width: 300px; height: 55px; border-radius: 10px; 
                        font-weight: bold; font-size: 18px; cursor: pointer;">
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
    st.warning("Arquivo 'pasta_teste.xlsx' não encontrado.")

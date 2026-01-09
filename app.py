import streamlit as st
import pandas as pd

# 1. Configuração da Página
st.set_page_config(
    page_title="Consulta de CNPJ | Filiais",
    page_icon="🔍",
    layout="wide"
)

# 2. Estilo CSS para melhorar o visual
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_content_label=True)

st.title("🏢 Localizador de CNPJ por Filial")
st.markdown("---")

# 3. Barra Lateral para Upload
with st.sidebar:
    st.header("📂 Configurações")
    arquivo = st.file_uploader("Carregue a planilha das filiais", type="xlsx")
    
    if arquivo:
        df = pd.read_excel(arquivo, engine='openpyxl')
        st.success("Planilha carregada!")
        
        st.divider()
        colunas = df.columns.tolist()
        col_filial = st.selectbox("Coluna da Filial", colunas, index=0)
        col_cnpj = st.selectbox("Coluna do CNPJ", colunas, index=1)

# 4. Área Principal de Busca
if arquivo:
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.subheader("🔍 Realizar Consulta")
        busca = st.text_input("Digite o código da filial:", placeholder="Ex: 101")
        
        if busca:
            # Filtro inteligente (remove espaços e converte para texto)
            resultado = df[df[col_filial].astype(str).str.strip() == str(busca).strip()]
            
            if not resultado.empty:
                cnpj_encontrado = str(resultado.iloc[0][col_cnpj])
                
                # Exibe o CNPJ em destaque
                st.metric(label=f"CNPJ DA FILIAL {busca}", value=cnpj_encontrado)
                
                # Botão para facilitar copiar o CNPJ
                st.code(cnpj_encontrado, language="text")
                
                with st.expander("📄 Detalhes completos da linha"):
                    st.table(resultado)
            else:
                st.error(f"⚠️ Nenhuma filial com o código '{busca}' foi encontrada.")

    # 5. Visualização Geral
    st.divider()
    with st.expander("📊 Ver planilha completa"):
        st.dataframe(df, use_container_width=True)

else:
    st.info("👈 Por favor, carregue o arquivo Excel na barra lateral para começar.")
    # Exemplo visual
    st.write("### Exemplo de formato aceito:")
    exemplo = pd.DataFrame({'Filial': ['10', '20'], 'CNPJ': ['00.000.000/0001-00', '11.111.111/0001-11']})
    st.table(exemplo)
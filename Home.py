import streamlit as st
import time

# Page config
st.set_page_config(
    page_title="Login - 4º BPM",
    page_icon="brasao.jpg",
    layout="wide"
)

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

# Lista de usuários autorizados
efetivo = [
    {"nome": "TC PM Alvarenga", "usuario": "02508041408", "senha": "1142879"},
    {"nome": "Maj PM Gustavo", "usuario": "03411465441", "senha": "1757253"},
    {"nome": "Cap PM Leonardo", "usuario": "04759772464", "senha": "1759698"},
    {"nome": "1º Ten PM Ramon", "usuario": "06340907474", "senha": "1960997"},
    {"nome": "2º Ten PM Silva", "usuario": "09575289498", "senha": "2452146"},
    {"nome": "ST PM João", "usuario": "05294764440", "senha": "1763903"},
    {"nome": "1º SGT PM Pedro", "usuario": "03593678446", "senha": "1669311"},
    {"nome": "2º SGT PM José", "usuario": "10950056421", "senha": "2452456"},
    {"nome": "3º SGT PM Maria", "usuario": "03691812120", "senha": "2452936"},
    {"nome": "3º SGT PM Aécio", "usuario": "01112841474", "senha": "1948059"},
    {"nome": "CB PM Ana", "usuario": "10435836455", "senha": "2276747"},
    {"nome": "CB PM Carlos", "usuario": "02408188490", "senha": "1642294"},
    {"nome": "SD PM Paulo", "usuario": "05563794466", "senha": "2397765"},
    {"nome": "SD PM Lucas", "usuario": "02488491403", "senha": "1637673"}
]

# Custom CSS for login form and hide sidebar
st.markdown("""<style>
[data-testid="stSidebar"][aria-expanded="true"] {
    visibility: hidden;
    width: 0px;
}



.login-form {
    background-color: rgba(255, 255, 255, 0.9);
    padding: 2rem;
    border-radius: 10px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.stButton > button {
    width: 100%;
    background-color: #0066cc;
    color: white;
    font-weight: bold;
    padding: 10px;
    border-radius: 5px;
    transition: all 0.3s;
}

.stButton > button:hover {
    background-color: #0052a3;
    transform: scale(1.02);
}
</style>""", unsafe_allow_html=True)

# Background image and login form
with st.container():
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.image("pontuacao.png", use_column_width=True)

    username = st.text_input("Usuário", type="password", max_chars=11)
    password = st.text_input("Senha", type="password", max_chars=7)
    
    if st.button("ACESSAR"):
        # Verificar credenciais
        user = next((u for u in efetivo if u["usuario"] == username and u["senha"] == password), None)
        if user:
            st.session_state['authenticated'] = True
            st.session_state['user_name'] = user["nome"]
            st.success(f"Bem vindo {user['nome']}!")
            time.sleep(2)
            st.switch_page("pages/produtividade.py")
        else:
            st.error("Usuário ou senha inválidos!")
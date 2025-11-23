import streamlit as st
import requests
import socket
import folium
from streamlit_folium import st_folium

# === Configuração da Página ===
st.set_page_config(page_title="Olho de Deus - Tony", page_icon="🌍", layout="centered")

# === Estilo Personalizado ===
st.markdown("""
    <style>
    .stMetric {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 10px;
        border: 1px solid #d6d6d6;
    }
    </style>
""", unsafe_allow_html=True)

# === Cabeçalho ===
st.title("🌍 Olho de Deus")
st.caption("Rastreador de IP e Domínios com Geolocalização")

# === Sidebar ===
with st.sidebar:
    st.header("Painel de Controle")
    st.info("Digite um domínio (ex: google.com) ou um IP para rastrear a origem física do servidor.")
    st.markdown("---")
    st.markdown("### 👑 Desenvolvido por **Tony**")
    st.text("60 anos de precisão.")

# === Entrada de Dados ===
alvo = st.text_input("Digite o IP ou Site (ex: tiktok.com):", placeholder="ex: 8.8.8.8 ou openai.com")

# === Funções do Sistema ===
def resolver_dominio(entrada):
    """Tenta converter site em IP. Se já for IP, retorna ele mesmo."""
    try:
        # Remove http:// se o usuário colocar sem querer
        entrada = entrada.replace("https://", "").replace("http://", "").replace("/", "")
        ip = socket.gethostbyname(entrada)
        return ip, entrada
    except socket.gaierror:
        return None, entrada

def buscar_geolocalizacao(ip_address):
    """Consulta a API de geolocalização pública"""
    try:
        url = f"http://ip-api.com/json/{ip_address}"
        response = requests.get(url)
        dados = response.json()
        if dados['status'] == 'fail':
            return None
        return dados
    except Exception as e:
        return None

# === Lógica Principal ===
if st.button("Rastrear Alvo 🛰️"):
    if alvo:
        with st.spinner("Triangulando sinal..."):
            # 1. Resolver DNS
            ip_real, dominio_limpo = resolver_dominio(alvo)
            
            if ip_real:
                # 2. Buscar Dados
                dados = buscar_geolocalizacao(ip_real)
                
                if dados:
                    st.success(f"Alvo Localizado: {dominio_limpo} -> {ip_real}")
                    
                    # 3. Mostrar Métricas (Dados Rápidos)
                    col1, col2, col3 = st.columns(3)
                    col1.metric("País", dados.get('country', 'N/A'), dados.get('countryCode', ''))
                    col2.metric("Cidade", dados.get('city', 'N/A'))
                    col3.metric("Provedor (ISP)", dados.get('isp', 'N/A'))
                    
                    st.markdown("---")
                    st.subheader("📍 Localização Exata")
                    
                    # 4. Gerar Mapa
                    lat = dados['lat']
                    lon = dados['lon']
                    
                    # Cria o mapa centrado no alvo
                    m = folium.Map(location=[lat, lon], zoom_start=12)
                    
                    # Adiciona o pino
                    tooltip_texto = f"{dominio_limpo} ({ip_real})"
                    folium.Marker(
                        [lat, lon], 
                        popup=f"Região: {dados.get('regionName')}", 
                        tooltip=tooltip_texto,
                        icon=folium.Icon(color="red", icon="info-sign")
                    ).add_to(m)
                    
                    # Renderiza o mapa no Streamlit
                    st_folium(m, width=700, height=500)
                    
                    # Dados Técnicos Extras
                    with st.expander("Ver Dados Técnicos Brutos (JSON)"):
                        st.json(dados)
                        
                else:
                    st.error("Não foi possível obter a geolocalização deste IP.")
            else:
                st.error("Domínio inválido ou site fora do ar.")
    else:
        st.warning("Digite um alvo primeiro.")

# === Rodapé ===
st.markdown("---")
st.markdown("<center>Sistema Operacional Tony v2.0</center>", unsafe_allow_html=True)

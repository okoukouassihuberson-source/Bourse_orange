import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime
import requests


# 1. Configuration de la page
st.set_page_config(
    page_title="Orange CI Financial Analytics",
    page_icon="🍊",
    layout="wide"
)

# 2. CSS Expert (Bootstrap + Custom Professional Styles)
st.html("""
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css">
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');

:root {
    --orange-orange: #FF7900;
    --pure-white: #FFFFFF;
    --text-dark: #1a1a1a;
    --text-light: #FFFFFF;
}

[data-testid="stAppViewContainer"] {
    background-image: url("https://raw.githubusercontent.com/okoukouassihuberson-source/Bourse_orange/main/okou.png");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}

[data-testid="stHeader"] {
    background-color: rgba(0,0,0,0);
}

.block-container {
    background-color: rgba(241, 243, 246, 0.8);
    padding: 2.5rem;
    border-radius: 20px;
    backdrop-filter: blur(8px);
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.1);
    color: var(--text-dark);
}

.f-card {
    background: white;
    border-radius: 15px;
    border: none;
    border-left: 6px solid var(--orange-orange);
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    color: var(--text-dark);
}

.f-card:hover {
    transform: translateY(-8px);
    box-shadow: 0 12px 25px rgba(255, 121, 0, 0.15);
    border-left: 8px solid #000;
}

.f-card h1, .f-card h2, .f-card h3, .f-card h4, .f-card h5, .f-card h6 {
    color: #000 !important;
}

.f-card .text-muted {
    color: #6c757d !important;
}

h1, h2, h3 { 
    color: var(--text-dark) !important; 
    font-weight: 800; 
}

p, div, span {
    color: inherit;
}

.badge-trend {
    padding: 0.5em 1em;
    border-radius: 50px;
    font-weight: 600;
    font-size: 0.9rem;
    color: white;
    background-color: var(--orange-orange);
}

.stTabs [role="tablist"] {
    background-color: #f8f9fa;
    border-radius: 10px;
    padding: 0.5rem;
    margin-bottom: 1rem;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}
.stTabs [role="tab"] {
    background-color: white;    
    border: none;
    border-radius: 8px;
    margin: 0 0.25rem;
    padding: 0.5rem 1rem;
    font-weight: 600;
    color: #212529;
    transition: background-color 0.3s ease;
    border-left: 6px solid transparent;
}
.stTabs [role="tab"][aria-selected="true"] {
    background-color: var(--orange-orange);
    color: white;
    border-left: 6px solid var(--orange-orange);
}
.stTabs [role="tab"]:hover {
    background-color: #ffe6cc;
    color: #c05400;
    border-left: 6px solid var(--orange-orange);
}

[data-testid="stMarkdownContainer"] {
    color: var(--text-dark);
}

.stDataFrame {
    color: var(--text-dark);
}
</style>

""")

# Watermark dynamique
st.markdown(
    f"""
    <style>
    .stApp::after {{
        content: "OKOU HUBERSON";
        position: fixed;
        top: 50%; left: 50%;
        font-size: 100px;
        color: rgba(255, 121, 0, 0.05);
        transform: translate(-50%, -50%) rotate(-30deg);
        z-index: -1;
        pointer-events: none;
        user-select: none;
        white-space: nowrap;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# 3. Sidebar Professionnelle
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/c/c8/Orange_logo.svg", width=80)
    st.title("💡 Paramètres")
    risk_free_rate = st.slider("Taux sans risque (BCEAO %)", 0.0, 10.0, 5.5) / 100
    window_ma = st.number_input("Fenêtre Moyenne Mobile", 5, 100, 20)
    st.divider()
    st.info("📊 Analyse de l'action Orange CI (ORAC) - Marché BRVM.")

# 4. Data Engine
@st.cache_data
def fetch_and_clean_data(url):
    try:

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        tables = pd.read_html(response.content)
        df = tables[0]
        df['Clôture'] = df['Clôture'].astype(str).str.replace(r'\s+', '', regex=True).str.replace(',', '.')
        df['Clôture'] = pd.to_numeric(df['Clôture'], errors='coerce')
        df = df.dropna(subset=['Clôture'])
        df = df.iloc[::-1].reset_index(drop=True)
        return df
    except Exception as e:
        st.error(f"Erreur de flux : {e}")
        return pd.DataFrame()

df = fetch_and_clean_data("https://www.sikafinance.com/marches/historiques/ORAC.ci")

if not df.empty:
    # Calculs
    df['Returns'] = df['Clôture'].pct_change()
    df['MA_selected'] = df['Clôture'].rolling(window_ma).mean()
    mean_return_annual = df['Returns'].mean() * 252
    volatility_annual = df['Returns'].std() * np.sqrt(252)
    sharpe_ratio = (mean_return_annual - risk_free_rate) / volatility_annual if volatility_annual != 0 else 0

    # UI HEADER
    st.title("Orange CI Financial Dashboard")
    st.markdown(f"**Analyse temps réel** • {datetime.now().strftime('%d %B %Y')}")

    # KPI ROW
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        current_val = df['Clôture'].iloc[-1]
        last_ret = df['Returns'].iloc[-1]
        color = "text-success" if last_ret > 0 else "text-danger"
        icon = "bi-arrow-up-right-circle-fill" if last_ret > 0 else "bi-arrow-down-right-circle-fill"
        
        st.markdown(f"""
            <div class="card f-card shadow-sm p-4">
                <div class="text-muted small fw-bold text-uppercase mb-2">Cours Actuel</div>
                <div class="d-flex align-items-baseline">
                    <h1 class="mb-0">{current_val:,.0f}</h1>
                    <span class="ms-2 text-muted">XOF</span>
                </div>
                <div class="{color} mt-2 fw-bold">
                    <i class="bi {icon}"></i> {last_ret:+.2%}
                </div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <div class="card f-card shadow-sm p-4">
                <div class="text-muted small fw-bold text-uppercase mb-2">Performance Ann.</div>
                <h1 class="mb-0" style="color:var(--orange-orange)!important;">{mean_return_annual:.1%}</h1>
                <div class="text-muted mt-2 small"><i class="bi bi-clock-history"></i> Projection 252j</div>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
            <div class="card f-card shadow-sm p-4">
                <div class="text-muted small fw-bold text-uppercase mb-2">Risque (Volatilité)</div>
                <h1 class="mb-0">{volatility_annual:.1%}</h1>
                <div class="mt-2">
                    <span class="badge {'bg-success' if volatility_annual < 0.2 else 'bg-warning'} badge-trend">
                        {'Sain' if volatility_annual < 0.2 else 'Agressif'}
                    </span>
                </div>
            </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
            <div class="card f-card shadow-sm p-4">
                <div class="text-muted small fw-bold text-uppercase mb-2">Sharpe Ratio</div>
                <h1 class="mb-0">{sharpe_ratio:.2f}</h1>
                <div class="mt-2 small text-muted">Qualité du rendement</div>
            </div>
        """, unsafe_allow_html=True)

    # GRAPHS
    st.divider()
    tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Performance Historique", 
    "📊 Analyse Statistique",
    "📋 Données de Marché",
    "📑 Rapport Expert"
])
    with tab1:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df.index, y=df['Clôture'], name="Prix", line=dict(color='#FF7900', width=4)))
        fig.add_trace(go.Scatter(x=df.index, y=df['MA_selected'], name="MA", line=dict(color="#ECF2F7", dash='dot')))
        fig.update_layout(template="plotly_white", hovermode="x unified", height=500)
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.dataframe(df.style.background_gradient(subset=['Returns'], cmap='RdYlGn'), use_container_width=True)
        st.subheader("Analyse de la Distribution des Rendements")
        # Création de l'histogramme avec Plotlyfig_hist = go.Figure()
        fig_hist = go.Figure()
        fig_hist.add_trace(go.Histogram(x=df['Returns'].dropna(), nbinsx=50, marker_color='#FF7900', opacity=0.75))
        fig_hist.update_layout(
            title="Distribution des Rendements Quotidiens",
            xaxis_title="Rendement",
            yaxis_title="Fréquence",
            template="plotly_white",
        )
        st.plotly_chart(fig_hist, use_container_width=True)

    with tab3:
        st.dataframe(df, use_container_width=True)

    with tab4:
        st.markdown("""
        <div style="color: black;">
            Rapport d'Analyse Financière - Orange CI (ORAC) sur le Marché BRVM
            
            Cette analyse fournit une vue d'ensemble complète de la performance de l'action Orange CI (ORAC) sur le marché BRVM. 
            Les indicateurs clés tels que le rendement annuel, la volatilité et le ratio de Sharpe sont essentiels pour évaluer la qualité des investissements.

            Interprétation des Indicateurs Clés :
                    Rendement Annuel: 
                        Indique la performance moyenne attendue sur une année.
                    Volatilité:
                     Mesure le risque associé à l'action; une volatilité plus faible est généralement préférable.
                    Ratio de Sharpe:
                     Évalue le rendement ajusté au risque; un ratio plus élevé indique une meilleure performance par rapport au risque pris.
                    
            

            Recommandations :
            
                Surveiller les tendances du marché et ajuster les stratégies d'investissement en conséquence.
                Considérer la diversification pour atténuer les risques liés à la volatilité.

            Pour toute question ou analyse approfondie, n'hésitez pas à me contacter au +225 0708817409.
        </div>
        """, unsafe_allow_html=True)


    # Footer
    st.markdown(f"""
        <div class="mt-5 p-4 text-center border-top">
            <p class="text-muted mb-0">Expertise : <b>Data Science Financière</b></p>
            <p class="fw-bold" style="color:var(--orange-orange)">OKOU KOUASSI HUBERSON</p>
        </div>
    """, unsafe_allow_html=True)
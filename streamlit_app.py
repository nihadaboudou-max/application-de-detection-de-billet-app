import streamlit as st
import pandas as pd
import requests
import io

# CONFIGURATION DE LA PAGE
st.set_page_config(
    page_title="Détection de faux billets",
    page_icon="💵",
    layout="wide"
)

# CSS DESIGN MODERNE VERT
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #a7f3d0 0%, #6ee7b7 50%, #34d399 100%);
        font-family: 'Poppins', sans-serif;
    }
    
    .main-header {
        background: linear-gradient(135deg, rgba(255,255,255,0.9), rgba(255,255,255,0.7));
        backdrop-filter: blur(20px);
        padding: 3rem 2rem;
        border-radius: 20px;
        text-align: center;
        margin: 2rem 0;
        box-shadow: 0 20px 40px rgba(16, 185, 129, 0.2);
        border: 1px solid rgba(255,255,255,0.3);
    }
    
    .main-header h1 {
        background: linear-gradient(135deg, #065f46, #10b981);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .main-header p {
        color: #047857;
        font-size: 1.3rem;
        font-weight: 400;
        margin: 0;
    }

    .glass-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.8), rgba(255,255,255,0.6));
        backdrop-filter: blur(15px);
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 15px 35px rgba(16, 185, 129, 0.15);
        border: 1px solid rgba(255,255,255,0.4);
        margin: 1rem 0;
    }

    .metric-card {
        background: linear-gradient(135deg, #10b981, #059669);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 10px 25px rgba(16, 185, 129, 0.3);
        transform: translateY(-5px);
    }
    
    .metric-card h3 {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
    }
    
    .metric-card p {
        margin: 0.5rem 0 0;
        opacity: 0.9;
        font-weight: 500;
    }

    .stButton > button {
        background: linear-gradient(135deg, #10b981, #059669);
        color: white;
        border: none;
        padding: 1rem 2rem;
        border-radius: 12px;
        font-weight: 600;
        font-size: 1.1rem;
        box-shadow: 0 8px 20px rgba(16, 185, 129, 0.4);
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 30px rgba(16, 185, 129, 0.5);
    }

    .upload-zone {
        border: 3px dashed #10b981;
        border-radius: 15px;
        padding: 2rem;
        text-align: center;
        background: rgba(16, 185, 129, 0.05);
        transition: all 0.3s ease;
    }
    
    .upload-zone:hover {
        background: rgba(16, 185, 129, 0.1);
        border-color: #059669;
    }

    .result-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.95), rgba(255,255,255,0.8));
        backdrop-filter: blur(10px);
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 10px 25px rgba(16, 185, 129, 0.1);
        border: 1px solid rgba(16, 185, 129, 0.2);
    }

    .success-badge {
        background: linear-gradient(135deg, #10b981, #059669);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        display: inline-block;
        margin: 0.5rem 0;
    }

    .danger-badge {
        background: linear-gradient(135deg, #ef4444, #dc2626);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        display: inline-block;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# HEADER PRINCIPAL
st.markdown("""
<div class="main-header">
    <h1>🎯 Détecteur de Faux Billets IA</h1>
    <p>Technologie avancée pour l'authentification automatique des billets</p>
</div>
""", unsafe_allow_html=True)

# INITIALISATION STATS
if 'stats' not in st.session_state:
    st.session_state.stats = {'total': 0, 'vrais': 0, 'faux': 0}

# MÉTRIQUES VISUELLES
st.markdown("## 📊 Tableau de Bord")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <h3>{st.session_state.stats['total']}</h3>
        <p>📊 Total Analysé</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card" style="background: linear-gradient(135deg, #10b981, #047857);">
        <h3>{st.session_state.stats['vrais']}</h3>
        <p>✅ Authentiques</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card" style="background: linear-gradient(135deg, #ef4444, #dc2626);">
        <h3>{st.session_state.stats['faux']}</h3>
        <p>❌ Suspects</p>
    </div>
    """, unsafe_allow_html=True)

# FORMULAIRE D'UPLOAD
st.markdown("## 📤 Zone d'Analyse")

with st.container():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    
    with st.form("formulaire_prediction"):
        st.markdown('<div class="upload-zone">', unsafe_allow_html=True)
        
        charger_file = st.file_uploader(
            "📁 Glissez votre fichier CSV ici",
            type="csv",
            help="Formats supportés: CSV avec données des billets"
        )
        
        col_form1, col_form2 = st.columns(2)
        with col_form1:
            separateur = st.selectbox(
                "🔧 Séparateur de données",
                options=["-- Sélectionner --", ",", ";", ".", "/", "|", "\\t", " "]
            )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        bouton_valider = st.form_submit_button("🚀 Lancer l'Analyse IA")
    
    st.markdown('</div>', unsafe_allow_html=True)

# TRAITEMENT ET RÉSULTATS
if bouton_valider:
    if charger_file is not None:
        if separateur == "-- Sélectionner --":
            st.warning("⚠️ Veuillez sélectionner un séparateur")
        else:
            try:
                # Animation de chargement
                with st.spinner('🔄 Analyse par Intelligence Artificielle...'):
                    df = pd.read_csv(charger_file, sep=separateur)
                    
                st.markdown('<div class="success-badge">✅ Fichier chargé avec succès</div>', unsafe_allow_html=True)
                
                # Aperçu élégant
                st.markdown('<div class="result-card">', unsafe_allow_html=True)
                st.markdown("### 👀 Aperçu des Données")
                st.dataframe(df.head(), use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Appel API
                reponse = requests.post(
                    "http://127.0.0.1:8000/predict",
                    files={"file": charger_file.getvalue()},
                    data={"separateur": separateur}
                )
                
                if reponse.status_code == 200:
                    resultat_json = reponse.json()
                    df_resultat = pd.DataFrame(resultat_json['resultat'])
                    
                    # Mise à jour des statistiques
                    compter = df_resultat['prediction'].value_counts()
                    st.session_state.stats['total'] = len(df_resultat)
                    st.session_state.stats['vrais'] = compter.get(1, 0)
                    st.session_state.stats['faux'] = compter.get(0, 0)
                    
                    # Résultats avec style
                    st.markdown("## 🎯 Résultats de l'Analyse IA")
                    
                    # Graphique et stats
                    col_res1, col_res2 = st.columns([1, 1])
                    
                    with col_res1:
                        st.markdown('<div class="result-card">', unsafe_allow_html=True)
                        st.markdown("### 📊 Visualisation")
                        
                        chart_data = pd.DataFrame({
                            'Authentiques': [st.session_state.stats['vrais']],
                            'Suspects': [st.session_state.stats['faux']]
                        })
                        st.bar_chart(chart_data, color=["#10b981", "#ef4444"], height=300)
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    with col_res2:
                        st.markdown('<div class="result-card">', unsafe_allow_html=True)
                        st.markdown("### 📈 Analyse Détaillée")
                        
                        total = st.session_state.stats['total']
                        pct_vrais = (st.session_state.stats['vrais'] / total) * 100
                        pct_faux = (st.session_state.stats['faux'] / total) * 100
                        
                        st.markdown(f"""
                        <div style="text-align: center;">
                            <div style="background: linear-gradient(135deg, #10b981, #059669); color: white; padding: 1rem; margin: 0.5rem 0; border-radius: 10px;">
                                <h4>✅ Billets Authentiques</h4>
                                <h2>{pct_vrais:.1f}%</h2>
                                <p>{st.session_state.stats['vrais']} sur {total}</p>
                            </div>
                            <div style="background: linear-gradient(135deg, #ef4444, #dc2626); color: white; padding: 1rem; margin: 0.5rem 0; border-radius: 10px;">
                                <h4>❌ Billets Suspects</h4>
                                <h2>{pct_faux:.1f}%</h2>
                                <p>{st.session_state.stats['faux']} sur {total}</p>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Alerte selon résultats
                    if st.session_state.stats['faux'] > 0:
                        st.error(f"⚠️ ATTENTION: {st.session_state.stats['faux']} billet(s) suspect(s) détecté(s)!")
                    else:
                        st.success("🎉 Excellente nouvelle! Tous les billets sont authentiques.")
                    
                    # Données complètes
                    st.markdown('<div class="result-card">', unsafe_allow_html=True)
                    st.markdown("### 📋 Rapport Complet")
                    st.dataframe(df_resultat, use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Téléchargement stylisé
                    csv_data = df_resultat.to_csv(index=False)
                    st.download_button(
                        "💾 Télécharger le Rapport Complet",
                        data=csv_data,
                        file_name="rapport_billets.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
                    
                else:
                    st.error(f"❌ Erreur de connexion API (Code: {reponse.status_code})")
                    
            except Exception as e:
                st.error(f"❌ Erreur lors du traitement: {str(e)}")
    else:
        st.error("📁 Veuillez d'abord télécharger un fichier CSV")

# FOOTER ÉLÉGANT
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem; color: #047857;">
    <h4>🔒 Système de Détection Sécurisé</h4>
    <p>Propulsé par l'Intelligence Artificielle • Version 2.0</p>
</div>
""", unsafe_allow_html=True)
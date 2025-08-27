import streamlit as st
import pandas as pd
import requests
import io
import plotly.express as px
import plotly.graph_objects as go

# CONFIGURATION DE LA PAGE
st.set_page_config(
    page_title="Détection de faux billets",
    page_icon="💵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS SIMPLE ET ATTRACTIF
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }
    
    .custom-header {
        background: rgba(255, 255, 255, 0.1);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .custom-header h1 {
        color: white;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .custom-header p {
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.2rem;
        margin: 0;
    }

    .stat-card {
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        box-shadow: 0 8px 25px rgba(0,0,0,0.2);
        margin-bottom: 1rem;
    }
    
    .stat-card h3 {
        margin: 0;
        font-size: 2rem;
        font-weight: bold;
    }
    
    .stat-card p {
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
    }

    .upload-zone {
        background: rgba(255, 255, 255, 0.1);
        padding: 2rem;
        border-radius: 15px;
        border: 2px dashed rgba(255, 255, 255, 0.5);
        backdrop-filter: blur(10px);
    }

    .stButton > button {
        background: linear-gradient(135deg, #10b981, #059669);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 10px;
        font-weight: bold;
        font-size: 1rem;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.4);
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(16, 185, 129, 0.5);
    }

    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #4f46e5, #7c3aed);
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #4f46e5, #7c3aed);
    }

    .metric-container {
        background: rgba(255, 255, 255, 0.1);
        padding: 1rem;
        border-radius: 10px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
</style>
""", unsafe_allow_html=True)

# HEADER PRINCIPAL
st.markdown("""
<div class="custom-header">
    <h1>🎯 Détecteur de Faux Billets</h1>
    <p>Analyse intelligente et prédiction automatique</p>
</div>
""", unsafe_allow_html=True)

# SIDEBAR AVEC INFORMATIONS
with st.sidebar:
    st.markdown("## 📊 Tableau de Bord")
    
    # Initialisation des statistiques
    if 'stats' not in st.session_state:
        st.session_state.stats = {
            'total_analyses': 0,
            'billets_authentiques': 0,
            'billets_suspects': 0
        }
    
    # Affichage des statistiques dans la sidebar
    st.markdown(f"""
    <div class="stat-card">
        <h3>{st.session_state.stats['total_analyses']}</h3>
        <p>Total Analysé</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div style="background: #10b981; padding: 1rem; border-radius: 8px; text-align: center; color: white;">
            <h4 style="margin: 0;">{st.session_state.stats['billets_authentiques']}</h4>
            <p style="margin: 0; font-size: 0.8rem;">✅ Vrais</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="background: #ef4444; padding: 1rem; border-radius: 8px; text-align: center; color: white;">
            <h4 style="margin: 0;">{st.session_state.stats['billets_suspects']}</h4>
            <p style="margin: 0; font-size: 0.8rem;">❌ Faux</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 🔧 Guide d'utilisation")
    st.markdown("""
    1. **Téléchargez** votre fichier CSV
    2. **Sélectionnez** le séparateur
    3. **Lancez** l'analyse
    4. **Visualisez** les résultats
    5. **Téléchargez** le rapport
    """)

# SECTION PRINCIPALE
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("## 📤 Zone d'Analyse")
    
    with st.form("formulaire_prediction"):
        st.markdown('<div class="upload-zone">', unsafe_allow_html=True)
        
        # Upload de fichier
        charger_file = st.file_uploader(
            "📁 Sélectionnez votre fichier CSV",
            type="csv",
            help="Téléchargez un fichier CSV contenant les caractéristiques des billets"
        )
        
        # Sélection du séparateur
        separateur = st.selectbox(
            "🔧 Choisissez le séparateur",
            options=["-- Sélectionner --", ",", ";", ".", "/", "|", "\\t", " "],
            help="Sélectionnez le caractère qui sépare vos données"
        )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Bouton de validation
        bouton_valider = st.form_submit_button("🚀 Analyser les Billets")

# Informations système dans la colonne droite
with col2:
    st.markdown("## ⚙️ Statut Système")
    
    st.markdown("""
    <div class="metric-container">
        <p style="color: white; margin: 0;"><strong>🟢 API Active</strong></p>
        <p style="color: rgba(255,255,255,0.8); margin: 0; font-size: 0.9rem;">Modèle IA opérationnel</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### 📈 Fonctionnalités")
    st.markdown("""
    - ✅ **Analyse rapide**
    - ✅ **Visualisations**  
    - ✅ **Export CSV**
    - ✅ **Interface intuitive**
    """)

# TRAITEMENT DU FORMULAIRE
if bouton_valider:
    if charger_file is not None:
        if separateur == "-- Sélectionner --":
            st.warning("⚠️ Veuillez choisir un séparateur pour traiter vos données")
        else:
            try:
                # Barre de progression
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                status_text.text('🔄 Chargement du fichier...')
                progress_bar.progress(25)
                
                # Lecture du fichier
                df = pd.read_csv(charger_file, sep=separateur)
                st.success("✅ Fichier chargé avec succès!")
                
                status_text.text('📊 Préparation des données...')
                progress_bar.progress(50)
                
                # Aperçu des données
                st.markdown("### 👀 Aperçu des Données")
                st.dataframe(df.head(), use_container_width=True)
                
                status_text.text('🤖 Analyse par IA en cours...')
                progress_bar.progress(75)
                
                # Appel API
                reponse = requests.post(
                    "http://127.0.0.1:8000/predict",
                    files={"file": charger_file.getvalue()},
                    data={"separateur": separateur}
                )
                
                progress_bar.progress(100)
                status_text.text('✅ Analyse terminée!')
                
                if reponse.status_code == 200:
                    resultat_json = reponse.json()
                    df_resultat = pd.DataFrame(resultat_json['resultat'])
                    
                    # Mise à jour des statistiques
                    compter = df_resultat['prediction'].value_counts()
                    st.session_state.stats['total_analyses'] = len(df_resultat)
                    st.session_state.stats['billets_authentiques'] = compter.get(1, 0)
                    st.session_state.stats['billets_suspects'] = compter.get(0, 0)
                    
                    # RÉSULTATS
                    st.markdown("## 🎯 Résultats de l'Analyse")
                    
                    # Métriques principales
                    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
                    
                    with col_m1:
                        st.metric("📊 Total", len(df_resultat))
                    with col_m2:
                        st.metric("✅ Authentiques", st.session_state.stats['billets_authentiques'])
                    with col_m3:
                        st.metric("❌ Suspects", st.session_state.stats['billets_suspects'])
                    with col_m4:
                        pourcentage_authentiques = (st.session_state.stats['billets_authentiques'] / len(df_resultat)) * 100
                        st.metric("📈 Taux Validité", f"{pourcentage_authentiques:.1f}%")
                    
                    # Graphiques
                    col_g1, col_g2 = st.columns(2)
                    
                    with col_g1:
                        # Graphique en secteurs
                        labels = ['Authentiques', 'Suspects']
                        values = [st.session_state.stats['billets_authentiques'], 
                                 st.session_state.stats['billets_suspects']]
                        colors = ['#10b981', '#ef4444']
                        
                        fig_pie = go.Figure(data=[go.Pie(
                            labels=labels, 
                            values=values,
                            hole=0.3,
                            marker_colors=colors,
                            textfont_size=16
                        )])
                        
                        fig_pie.update_layout(
                            title="Répartition des Prédictions",
                            title_font_size=18,
                            height=400
                        )
                        
                        st.plotly_chart(fig_pie, use_container_width=True)
                    
                    with col_g2:
                        # Graphique en barres
                        fig_bar = go.Figure(data=[
                            go.Bar(x=labels, y=values, 
                                  marker_color=colors,
                                  text=values,
                                  textposition='auto')
                        ])
                        
                        fig_bar.update_layout(
                            title="Nombre par Catégorie",
                            title_font_size=18,
                            height=400,
                            yaxis_title="Nombre de billets"
                        )
                        
                        st.plotly_chart(fig_bar, use_container_width=True)
                    
                    # Tableau des résultats
                    st.markdown("### 📋 Données Détaillées")
                    st.dataframe(df_resultat, use_container_width=True)
                    
                    # Téléchargement
                    csv_memoire = io.StringIO()
                    df_resultat.to_csv(csv_memoire, index=False)
                    csv_data = csv_memoire.getvalue()
                    
                    st.download_button(
                        label="💾 Télécharger les Résultats",
                        data=csv_data,
                        file_name="predictions_billets.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
                    
                else:
                    st.error(f"❌ Erreur API (Code: {reponse.status_code})")
                    st.text(reponse.text)
                    
            except Exception as e:
                st.error(f"❌ Erreur: {str(e)}")
    else:
        st.error("📁 Veuillez télécharger un fichier CSV")

# FOOTER
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 1rem; color: rgba(255,255,255,0.8);">
    <p><strong>🔒 Détection Sécurisée de Faux Billets</strong> - Propulsé par l'IA</p>
</div>
""", unsafe_allow_html=True)
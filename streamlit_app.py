import streamlit as st
import pandas as pd
import requests
import io

# CONFIGURATION DE LA PAGE
st.set_page_config(
    page_title="Détection de faux billets",
    page_icon="",
    layout="wide"
)

# CSS 
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        min-height: 100vh;
    }
    
    .custom-header {
        background: #10c501;
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        border: 1px solid rgba(16, 185, 129, 0.2);
    }
    
    .custom-header h1 {
        color: #FFFFFF;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    
    .custom-header p {
        color: #FFFFFF;
        font-size: 1.2rem;
        margin: 0;
    }

    .stat-card {
        background: rgba(255, 255, 255, 0.95);
        padding: 1.5rem;
        border-radius: 12px;
        color: #1e293b;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        border: 1px solid #e2e8f0;
    }
    
    .stat-card h3 {
        margin: 0;
        font-size: 2rem;
        font-weight: bold;
        color: #10b981;
    }
    
    .stat-card p {
        margin: 0.5rem 0 0 0;
        color: #64748b;
    }

    .upload-zone {
        background: rgba(255, 255, 255, 0.9);
        padding: 2rem;
        border-radius: 15px;
        border: 2px dashed #10b981;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }

    .stButton > button {
        background: #10c501;
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 10px;
        font-weight: bold;
        font-size: 1rem;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(16, 185, 129, 0.4);
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f8fafc, #f1f5f9);
    }

    .metric-container {
        background: rgba(255, 255, 255, 0.9);
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        border: 1px solid #e2e8f0;
        margin-bottom: 1rem;
    }

    .result-card {
        background: rgba(255, 255, 255, 0.95);
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        border: 1px solid #e2e8f0;
    }

    .chart-container {
        background: rgba(255, 255, 255, 0.8);
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border: 1px solid #f1f5f9;
    }

    .success-accent {
        color: #059669 !important;
        font-weight: 600;
    }

    .danger-accent {
        color: #dc2626 !important;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# HEADER PRINCIPAL
st.markdown("""
<div class="custom-header">
    <h1>Détecteur de Faux Billets</h1>
    <p>Analyse intelligente et prédiction automatique</p>
</div>
""", unsafe_allow_html=True)

# SIDEBAR AVEC INFORMATIONS
with st.sidebar:
    st.markdown("Tableau de Bord")
    
    # Initialisation des statistiques
    if 'stats' not in st.session_state:
        st.session_state.stats = {
            'total_analyses': 0,
            'billets_authentiques': 0,
            'billets_suspects': 0
        }
    
    st.markdown("---")
    st.markdown("Guide d'utilisation")
    st.markdown("""
    1. Téléchargez votre fichier CSV
    2. Sélectionnez le séparateur
    3. Lancez l'analyse
    4. Visualisez les résultats
    5. Téléchargez le rapport
    """)

# SECTION PRINCIPALE
with st.form("formulaire_prediction"):
 
        # Upload de fichier
    charger_file = st.file_uploader("Sélectionnez votre fichier CSV", type="csv", help="Téléchargez un fichier CSV contenant les caractéristiques des billets")
        
        # Sélection du séparateur
    separateur = st.selectbox("Choisissez le séparateur",
        options=["-- Sélectionner --", ",", ";", ".", "/", "|", "\\t", " "],
        help="Sélectionnez le caractère qui sépare vos données")
        
    st.markdown('</div>', unsafe_allow_html=True)
        
        # Bouton de validation
    bouton_valider = st.form_submit_button("Analyser les Billets")

# TRAITEMENT DU FORMULAIRE
if bouton_valider:
    if charger_file is not None:
        if separateur == "-- Sélectionner --":
            st.warning("Veuillez choisir un séparateur pour traiter vos données")
        else:
            try:
                # Barre de progression
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                status_text.text('Chargement du fichier...')
                progress_bar.progress(25)
                
                # Lecture du fichier
                df = pd.read_csv(charger_file, sep=separateur)
                st.toast("Fichier chargé avec succès!")
                
                status_text.text('Préparation des données...')
                progress_bar.progress(50)
                
                # Aperçu des données
                st.markdown("Aperçu des Données")
                st.dataframe(df.head(), use_container_width=True)
                
                status_text.text('Analyse en cours...')
                progress_bar.progress(75)
                
                # Appel API
                reponse = requests.post(
                    "https://api-detection-billet.onrender.com/predict",
                    files={"file": charger_file.getvalue()},
                    data={"separateur": separateur}
                )
                
                progress_bar.progress(100)
                status_text.text('Analyse terminée!')
                
                if reponse.status_code == 200:
                    resultat_json = reponse.json()
                    df_resultat = pd.DataFrame(resultat_json['resultat'])
                    
                    # Mise à jour des statistiques
                    compter = df_resultat['prediction'].value_counts()
                    st.session_state.stats['total_analyses'] = len(df_resultat)
                    st.session_state.stats['billets_authentiques'] = compter.get(1, 0)
                    st.session_state.stats['billets_suspects'] = compter.get(0, 0)
                    
                    # RÉSULTATS
                    st.markdown("Résultats de l'Analyse")
                    
                    # Métriques principales
                    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
                    
                    with col_m1:
                        st.metric("Total", len(df_resultat))
                    with col_m2:
                        st.metric("Authentiques", st.session_state.stats['billets_authentiques'])
                    with col_m3:
                        st.metric("Suspects", st.session_state.stats['billets_suspects'])
                    with col_m4:
                        pourcentage_authentiques = (st.session_state.stats['billets_authentiques'] / len(df_resultat)) * 100
                        st.metric("Taux Validité", f"{pourcentage_authentiques:.1f}%")

                                    
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
                        <div style="background: #10c501; padding: 1rem; border-radius: 8px; text-align: center; color: white; box-shadow: 0 2px 8px rgba(16, 185, 129, 0.3);">
                            <h4 style="margin: 0;">{st.session_state.stats['billets_authentiques']}</h4>
                            <p style="margin: 0; font-size: 0.8rem;">Vrais</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col2:
                        st.markdown(f"""
                        <div style="background: #EF4444; padding: 1rem; border-radius: 8px; text-align: center; color: white; box-shadow: 0 2px 8px rgba(100, 116, 139, 0.3);">
                            <h4 style="margin: 0;">{st.session_state.stats['billets_suspects']}</h4>
                            <p style="margin: 0; font-size: 0.8rem;">Faux</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Graphiques avec Streamlit natif
                    st.markdown('<div class="chart-container">', unsafe_allow_html=True
                    st.markdown("Visualisations des Résultats")
                    
                    col_g1, col_g2 = st.columns(2)
                    
                    with col_g1:
                    
                        st.markdown("Répartition des Prédictions")
                        
                        # Création d'un DataFrame pour le graphique
                        chart_data = pd.DataFrame({
                            'Type': ['Authentiques', 'Suspects'],
                            'Nombre': [st.session_state.stats['billets_authentiques'], 
                                      st.session_state.stats['billets_suspects']]
                        })
                        
                        # Graphique en barres avec Streamlit
                        st.bar_chart(chart_data.set_index('Type'), height=300)
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    with col_g2:
                        
                        st.markdown("Statistiques Détaillées")
                        
                        # Affichage des pourcentages
                        total = st.session_state.stats['total_analyses']
                        pct_auth = (st.session_state.stats['billets_authentiques'] / total) * 100
                        pct_susp = (st.session_state.stats['billets_suspects'] / total) * 100
                        
                        st.markdown(f"""
                        <div style="text-align: center;">
                            <div style="background: #10c501; border: 1px solid #10b981; color: #FFFFFF; padding: 1rem; margin: 0.5rem 0; border-radius: 8px;">
                                <h4>Billets Authentiques</h4>
                                <p style="font-size: 1.5rem; margin: 0; color: #FFFFFF; font-weight: bold;">{pct_auth:.1f}%</p>
                                <p style="margin: 0; color: #FFFFFF;">({st.session_state.stats['billets_authentiques']} sur {total})</p>
                            </div>
                            <div style="background: #EF4444; border: 1px solid #64748b; color: #FFFFFF; padding: 1rem; margin: 0.5rem 0; border-radius: 8px;">
                                <h4>Billets Suspects</h4>
                                <p style="font-size: 1.5rem; margin: 0; color: #FFFFFF; font-weight: bold;">{pct_susp:.1f}%</p>
                                <p style="margin: 0; color: #FFFFFF;">({st.session_state.stats['billets_suspects']} sur {total})</p>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Tableau des résultats
                    st.markdown("Données Détaillées après prédiction")
                    st.dataframe(df_resultat.head(3), use_container_width=True)
                    
                    # Téléchargement
                    csv_memoire = io.StringIO()
                    df_resultat.to_csv(csv_memoire, index=False)
                    csv_data = csv_memoire.getvalue()
                    
                    st.download_button(
                        label="Télécharger les Résultats",
                        data=csv_data,
                        file_name="predictions_billets.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
                    
                else:
                    st.error(f"Erreur API (Code: {reponse.status_code})")
                    st.text(reponse.text)
                    
            except Exception as e:
                st.error(f"Erreur: {str(e)}")
    else:
        st.error("Veuillez télécharger un fichier CSV")

# FOOTER
st.markdown("""
<div style="text-align: center; padding: 1rem; color: #64748b;">
    <p><strong>Détection de Faux Billets</strong> - Réaliser par Nihad ABOUDOU TRAORE</p>
</div>
""", unsafe_allow_html=True)

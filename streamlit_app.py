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

# CSS SIMPLE ET VERT
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #a7f3d0 0%, #34d399 100%);
    }
    
    .header {
        background: rgba(16, 185, 129, 0.2);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        border: 1px solid rgba(16, 185, 129, 0.3);
    }
    
    .header h1 {
        color: #065f46;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }

    .upload-box {
        background: rgba(255, 255, 255, 0.9);
        padding: 2rem;
        border-radius: 10px;
        border: 2px dashed #10b981;
        margin: 1rem 0;
    }

    .stButton > button {
        background: linear-gradient(135deg, #10b981, #059669);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 8px;
        font-weight: bold;
        width: 100%;
    }

    .metric-card {
        background: rgba(16, 185, 129, 0.1);
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid rgba(16, 185, 129, 0.3);
        text-align: center;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# HEADER
st.markdown("""
<div class="header">
    <h1>🎯 Détecteur de Faux Billets</h1>
    <p>Analyse rapide et intelligente</p>
</div>
""", unsafe_allow_html=True)

# STATISTIQUES
if 'stats' not in st.session_state:
    st.session_state.stats = {'total': 0, 'vrais': 0, 'faux': 0}

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("📊 Total", st.session_state.stats['total'])
with col2:
    st.metric("✅ Authentiques", st.session_state.stats['vrais'])
with col3:
    st.metric("❌ Suspects", st.session_state.stats['faux'])

# FORMULAIRE
st.markdown("## 📤 Analyse de fichier")

with st.form("formulaire_prediction"):
    st.markdown('<div class="upload-box">', unsafe_allow_html=True)
    
    charger_file = st.file_uploader("Sélectionnez votre fichier CSV", type="csv")
    
    separateur = st.selectbox(
        "Séparateur", 
        options=["-- Sélectionner --", ",", ";", ".", "/", "|", "\\t", " "]
    )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    bouton_valider = st.form_submit_button("🚀 Analyser")

# TRAITEMENT
if bouton_valider:
    if charger_file is not None:
        if separateur == "-- Sélectionner --":
            st.warning("⚠️ Choisissez un séparateur")
        else:
            try:
                # Lecture fichier
                df = pd.read_csv(charger_file, sep=separateur)
                st.success("✅ Fichier chargé !")
                
                # Aperçu
                st.write("**Aperçu des données :**")
                st.dataframe(df.head())
                
                # Appel API
                with st.spinner('Analyse en cours...'):
                    reponse = requests.post(
                        "http://127.0.0.1:8000/predict",
                        files={"file": charger_file.getvalue()},
                        data={"separateur": separateur}
                    )
                
                if reponse.status_code == 200:
                    resultat_json = reponse.json()
                    df_resultat = pd.DataFrame(resultat_json['resultat'])
                    
                    # Mise à jour stats
                    compter = df_resultat['prediction'].value_counts()
                    st.session_state.stats['total'] = len(df_resultat)
                    st.session_state.stats['vrais'] = compter.get(1, 0)
                    st.session_state.stats['faux'] = compter.get(0, 0)
                    
                    # Résultats
                    st.markdown("## 🎯 Résultats")
                    
                    # Graphique simple
                    chart_data = pd.DataFrame({
                        'Authentiques': [st.session_state.stats['vrais']],
                        'Suspects': [st.session_state.stats['faux']]
                    })
                    st.bar_chart(chart_data, color=["#10b981", "#ef4444"])
                    
                    # Détails
                    st.write("**Comptage :**", compter)
                    
                    # Tableau résultats
                    st.write("**Données complètes :**")
                    st.dataframe(df_resultat)
                    
                    # Téléchargement
                    csv_data = df_resultat.to_csv(index=False)
                    st.download_button(
                        "💾 Télécharger résultats",
                        data=csv_data,
                        file_name="predictions.csv",
                        mime="text/csv"
                    )
                    
                else:
                    st.error(f"❌ Erreur API: {reponse.status_code}")
                    
            except Exception as e:
                st.error(f"❌ Erreur: {str(e)}")
    else:
        st.error("📁 Téléchargez un fichier d'abord")

# FOOTER
st.markdown("---")
st.markdown("**🔒 Détection sécurisée de faux billets**")
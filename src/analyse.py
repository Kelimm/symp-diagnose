import streamlit as st
import streamlit as st
from streamlit_option_menu import option_menu
import time 
import pandas as pd
import joblib
from dictionnaire import *


@st.cache_resource
def load_resources():
    # Chargement du modèle de Régression Logistique
    model = joblib.load("models/Random_Forest.pkl")
    
    # Chargement de l'encodeur de labels
    label_encoder = joblib.load("models/label_encoder.pkl")
    
    return model, label_encoder

try:
    model, le = load_resources()
except FileNotFoundError:
    st.error("Erreur : Impossible de trouver les fichiers de modèles dans le dossier 'models/'. "
        "Assurez-vous que 'logistic_regression.pkl' et 'label_encoder.pkl' y sont bien présents.")


def load_analyse_page():
    st.markdown("""
        <style>
        /* ===== Carte blanche principale ===== */
        .st-key-white_bgc {
            background-color: white;
            border: 1px solid #E2E8F0;
            border-radius: 16px;
            padding: 24px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.02), 0 2px 4px -1px rgba(0, 0, 0, 0.02);
        }""",unsafe_allow_html=True)

    st.markdown('''
    # 🩺 Analyse de Symptômes

    Cette interface expérimentale utilise un modèle d'apprentissage automatique pour analyser vos symptômes et estimer les pathologies les plus probables, tout en vous proposant un plan d'accompagnement illustratif.

    **Comment procéder ?**
    1. Saisissez vos symptômes principaux dans le champ de recherche ci-dessous.
    2. Cliquez sur **"Lancer l'analyse"** pour afficher l'estimation et vos recommandations personnalisées.


    > ⚠️ **Avertissement de démonstration :**
    > Ce projet est un prototype étudiant à but exclusivement pédagogique et n'a reçu aucune validation clinique. Les résultats et conseils affichés sont des exemples générés automatiquement et **ne remplacent en aucun cas l'avis, le diagnostic ou le traitement d'un médecin.** En cas de problème de santé, consultez un professionnel. 
    ---
    ''')

    st.metric(label="Precision globale du modèle", value="89.85%")
    
    liste_symptomes = model.feature_names_in_.tolist()
    # symp = df.drop("diseases")
    symp = st.multiselect("Quels sont vos symptômes ?",
                options=liste_symptomes)

    input_dict = {
    symptome: [1 if symptome in symp else 0] for symptome in liste_symptomes
    }

    input_df = pd.DataFrame(input_dict)
    descriptionDF = pd.read_csv("./data/descriptionfr.csv",  index_col="Disease")
    medicamentsDF = pd.read_csv("./data/medications.csv",  index_col="Disease")
    dietsDF = pd.read_csv("./data/diets.csv",  index_col="Disease")
    precautionsDF = pd.read_csv("./data/precautions.csv",  index_col="Disease")

    if st.button("Lancer l'analyse"):
        if len(symp) == 0:
            st.warning("Veuillez sélectionner au moins un symptôme.")
        else:
            # 1. Prédiction du numéro de la maladie
            prediction_num = model.predict(input_df)[0]
            
            # 2. Calcul des probabilités pour les 100 maladies possibles
            probabilites = model.predict_proba(input_df)[0]
            
            # 3. Extraction de la probabilité la plus élevée (celle de la maladie prédite)
            fiabilite_score = max(probabilites) * 100
            
            # 4. Décodage et traduction
            maladie_anglais = le.inverse_transform([prediction_num])[0]
            maladie_francais = MALADIES_TRADUCTION.get(maladie_anglais, maladie_anglais)

            description = descriptionDF.loc[maladie_francais.capitalize(), "Description"]
            medicaments = medicamentsDF.loc[maladie_anglais.capitalize(), "Medication"]
            diets = dietsDF.loc[maladie_francais.capitalize(), "Diet"]

            precaution1 = precautionsDF.loc[maladie_francais.capitalize(), "Precaution_1"]
            precaution2 = precautionsDF.loc[maladie_francais.capitalize(), "Precaution_2"]
            precaution3 = precautionsDF.loc[maladie_francais.capitalize(), "Precaution_3"]
            precaution4 = precautionsDF.loc[maladie_francais.capitalize(), "Precaution_4"]
            precautions = [precaution1, precaution2, precaution3, precaution4]
            with st.container(key="white_bgc"):
                col1, col2 = st.columns([2, 1], vertical_alignment="top")
                with col2 : 
                    st.metric(
                        label="Indice de confiance du diagnostic", 
                        value=f"{fiabilite_score:.1f}%",
                        help="Ce pourcentage représente la certitude du modèle mathématique face aux symptômes déclarés."
                    )
        
                with col1:
                    st.markdown(f"### {maladie_francais.capitalize()}") 
        
                st.markdown("***")
                # ===== Description =====
                st.markdown(
                    """
                    #### Description
                    """,
                    unsafe_allow_html=True
                )
                st.markdown(
                    f"""
                    {description}
                    """
                )
        
                st.write("")
        
                # ===== Médicaments recommandés / Alimentation & Diète =====
                col_med, col_diet = st.columns(2, vertical_alignment="top")
        
                with col_med:
                    st.markdown(
                        """
                        #### Alimentation & Diète
                        """,
                    )
                    medicaments = [med.strip(" '\"") for med in medicaments.strip("[]").split(",")]
                    for med in medicaments:
                        st.markdown(
                            f"""
                            <div class="med-card">
                                <div class="med-card-title">{med}</div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                    st.markdown(
                        """
                        #### Precautions
                        """,
                    )
                    for prec in precautions :
                        st.markdown(f"""
                            <div>
                                <div >{prec}</div>
                            </div>
                        """, unsafe_allow_html=True)
        
                with col_diet:
                    st.markdown("""#### Alimentation & Diète
                    """)
        
                    
                    diets = [diet.strip(" '\"") for diet in diets.strip("[]").split(",")]

                    items_html = "".join(
                        f'<div class="diet-item">{text}</div>'
                        for text in diets
                    )
                    st.markdown(f'<div class="diet-box">{items_html}</div>', unsafe_allow_html=True)
            

            

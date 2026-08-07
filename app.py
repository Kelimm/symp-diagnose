import streamlit as st
from streamlit_option_menu import option_menu
import time 
import pandas as pd
import joblib
from dictionnaire import *
from src.analyse import load_analyse_page
from src.liste_maladie import load_liste_page
from src.visu import load_visu_page

MALADIES_TRADUCTION = MALADIES_TRADUCTION
MALADIES_CLUSTER = MALADIES_CLUSTER



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

st.set_page_config(layout="wide", page_title="Accueil")

with st.sidebar:
    selected = option_menu(
        menu_title="Diagnostic Santé",
        options=["Analyse", "Répertoire des pathologies", "Visualisation"],
        icons=["bag-plus", "file-earmark-text", "bar-chart-line"],
        menu_icon="none", # Masquer l'icône à côté du titre principal
        default_index=0, # Option sélectionnée par défaut
        styles={
            "container": {
                "padding": "0px", 
                "background-color": "transparent"
            },
            "title": {
                "color": "#2C5282", # Couleur bleu foncé pour le titre principal
                "font-size": "22px", 
                "font-weight": "bold",
                "padding": "10px 0px"
            },
            "icon": {
                "color": "#2D3748", # Couleur des icônes non sélectionnées
                "font-size": "18px"
            }, 
            "nav-link": {
                "font-size": "16px", 
                "text-align": "left", 
                "margin": "8px 0px", 
                "color": "#2D3748", # Couleur du texte non sélectionné
                "font-weight": "500",
                "border-radius": "25px", # Arrondir les bords comme sur l'image
                "padding": "12px 20px"
            },
            "nav-link-selected": {
                "background-color": "#C6F6D5", # Vert clair de l'onglet actif
                "color": "#22543D", # Vert foncé pour le texte actif
                "font-weight": "bold",
                "border-radius": "25px" # Conserver l'arrondi pour la sélection
            }
        }
    )


if selected == "Analyse" :
    load_analyse_page()

elif selected == "Répertoire des pathologies":
    load_liste_page()

elif selected == "Visualisation" :
    load_visu_page()
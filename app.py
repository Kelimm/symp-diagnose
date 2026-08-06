import streamlit as st
from streamlit_option_menu import option_menu
import time 
import pandas as pd
import joblib

MALADIES_TRADUCTION = {
    'actinic keratosis': 'kératose actinique',
    'acute bronchiolitis': 'bronchiolite aiguë',
    'acute bronchitis': 'bronchite aiguë',
    'acute bronchospasm': 'bronchospasme aigu',
    'acute kidney injury': 'insuffisance rénale aiguë',
    'acute pancreatitis': 'pancréatite aiguë',
    'acute sinusitis': 'sinusite aiguë',
    'allergy': 'allergie',
    'angina': 'angine de poitrine',
    'anxiety': 'anxiété',
    'appendicitis': 'appendicite',
    'arthritis of the hip': 'arthrose de la hanche',
    'asthma': 'asthme',
    'benign prostatic hyperplasia (bph)': 'hypertrophie bénigne de la prostate',
    'brachial neuritis': 'névrite brachiale',
    'bursitis': 'bursite',
    'carpal tunnel syndrome': 'syndrome du canal carpien',
    'cholecystitis': 'cholécystite',
    'chronic back pain': 'lombalgie chronique',
    'chronic constipation': 'constipation chronique',
    'chronic obstructive pulmonary disease (copd)': 'bronchopneumopathie chronique obstructive (BPCO)',
    'common cold': 'rhume',
    'complex regional pain syndrome': 'syndrome douloureux régional complexe',
    'concussion': 'commotion cérébrale',
    'conjunctivitis': 'conjonctivite',
    'conjunctivitis due to allergy': 'conjonctivite allergique',
    'contact dermatitis': 'eczéma de contact',
    'cornea infection': 'infection de la cornée',
    'croup': 'croup (laryngo-trachéo-bronchite)',
    'cystitis': 'cystite',
    'degenerative disc disease': 'discopathie dégénérative',
    'dental caries': 'carie dentaire',
    'depression': 'dépression',
    'developmental disability': 'trouble du développement',
    'diaper rash': 'érythème fessier du nourrisson',
    'diverticulitis': 'diverticulite',
    'drug reaction': 'réaction indésirable à un médicament',
    'ear drum damage': 'perforation du tympan',
    'eczema': 'eczéma',
    'esophagitis': 'œsophagite',
    'eustachian tube dysfunction (ear disorder)': "dysfonctionnement de la trompe d'Eustache",
    'fungal infection of the hair': 'teigne du cuir chevelu',
    'gallstone': 'calcul biliaire',
    'gastrointestinal hemorrhage': 'hémorragie gastro-intestinale',
    'gout': 'goutte',
    'gum disease': 'gingivite (maladie des gencives)',
    'heart attack': 'infarctus du myocarde (crise cardiaque)',
    'heart failure': 'insuffisance cardiaque',
    'hemorrhoids': 'hémorroïdes',
    'herniated disk': 'hernie discale',
    'hiatal hernia': 'hernie hiatale',
    'hyperemesis gravidarum': 'hyperémèse gravidique',
    'hypertensive heart disease': 'cardiopathie hypertensive',
    'hypoglycemia': 'hypoglycémie',
    'idiopathic excessive menstruation': 'règles anormalement abondantes',
    'idiopathic irregular menstrual cycle': 'cycles menstruels irréguliers',
    'idiopathic painful menstruation': 'règles douloureuses',
    'infectious gastroenteritis': 'gastro-entérite infectieuse',
    'injury to the arm': 'blessure au bras',
    'injury to the leg': 'blessure à la jambe',
    'injury to the trunk': 'blessure au torse',
    'liver disease': 'maladie du foie',
    'macular degeneration': 'dégénérescence maculaire (DMLA)',
    'marijuana abuse': 'abus de cannabis',
    'multiple sclerosis': 'sclérose en plaques',
    'noninfectious gastroenteritis': 'gastro-entérite non infectieuse',
    'nose disorder': 'affection nasale',
    'obstructive sleep apnea (osa)': 'apnée obstructive du sommeil',
    "otitis externa (swimmer's ear)": "otite externe (oreille du nageur)",
    'otitis media': 'otite moyenne',
    'pain after an operation': 'douleur postopératoire',
    'panic disorder': 'trouble panique',
    'pelvic inflammatory disease': 'maladie inflammatoire pelvienne',
    'peripheral nerve disorder': 'neuropathie périphérique',
    'personality disorder': 'trouble de la personnalité',
    'personality disorder': 'trouble de la personnalité',
    'pneumonia': 'pneumonie',
    'problem during pregnancy': 'complication pendant la grossesse',
    'psoriasis': 'psoriasis',
    'pyogenic skin infection': 'pyodermite (infection purulente de la peau)',
    'rectal disorder': 'affection rectale',
    'schizophrenia': 'schizophrénie',
    'seasonal allergies (hay fever)': 'rhume des foins (rhinite allergique)',
    'sebaceous cyst': 'kyste sébacé',
    'sepsis': 'septicémie (sepsis)',
    'sickle cell crisis': 'crise drépanocytaire',
    'sinus bradycardia': 'bradycardie sinusale',
    'skin pigmentation disorder': 'trouble de la pigmentation de la peau',
    'skin polyp': 'polype cutané',
    'spinal stenosis': 'sténose spinale',
    'spondylosis': 'spondylarthrose',
    'spontaneous abortion': 'fausse couche spontanée',
    'sprain or strain': 'entorse ou foulure',
    'strep throat': 'angine à streptocoque',
    'stye': 'orgelet',
    'temporary or benign blood in urine': 'présence temporaire de sang dans les urines',
    'threatened pregnancy': 'menace de fausse couche',
    'urinary tract infection': 'infection urinaire',
    'vaginal cyst': 'kyste vaginal',
    'vaginitis': 'vaginite',
    'vulvodynia': 'vulvodynie'
}

@st.cache_resource
def load_resources():
    # Chargement du modèle de Régression Logistique
    model = joblib.load("models/logistic_regression.pkl")
    
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
        options=["Symptômes", "Rapport", "Conseils", "Profil"],
        icons=["bag-plus", "file-earmark-text", "shield-plus", "person"],
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


if selected == "Symptômes":
    st.markdown('''
## 🩺 Analyse de Symptômes

Cette interface expérimentale utilise un modèle d'apprentissage automatique pour analyser vos symptômes et estimer les pathologies les plus probables, tout en vous proposant un plan d'accompagnement illustratif.

**Comment procéder ?**
1. Saisissez vos symptômes principaux dans le champ de recherche ci-dessous.
2. Cliquez sur **"Lancer l'analyse"** pour afficher l'estimation et vos recommandations personnalisées.

---

> ⚠️ **Avertissement de démonstration :**
> Ce projet est un prototype étudiant à but exclusivement pédagogique et n'a reçu aucune validation clinique. Les résultats et conseils affichés sont des exemples générés automatiquement et **ne remplacent en aucun cas l'avis, le diagnostic ou le traitement d'un médecin.** En cas de problème de santé, consultez un professionnel.
''')
    col1, col2 = st.columns(2)

    st.metric(label="Precision globale du modèle", value="89.85%")

    df = pd.read_csv("./data/Diseases_and_Symptoms_dataset.csv")

    liste_symptomes = model.feature_names_in_.tolist()
    # symp = df.drop("diseases")
    symp = st.multiselect("Quels sont vos symptômes ?",
                   options=liste_symptomes)

    input_dict = {
        symptome: [1 if symptome in symp else 0] for symptome in liste_symptomes
    }

    input_df = pd.DataFrame(input_dict)

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
            
            # 5. Affichage des résultats
            st.success(f"### Pathologie suspectée : **{maladie_francais.capitalize()}**")
            
            # Affichage de la fiabilité sous forme de métrique (comme sur votre maquette)
            st.metric(
                label="Indice de confiance du diagnostic", 
                value=f"{fiabilite_score:.1f}%",
                help="Ce pourcentage représente la certitude du modèle mathématique face aux symptômes déclarés."
            )
    # À insérer tout en bas de votre fichier app.py (en dehors de tout bloc conditionnel)


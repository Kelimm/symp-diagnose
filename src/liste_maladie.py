import streamlit as st
import pandas as pd




svg_path = "./svg/information.svg"

import streamlit as st

def load_liste_page():
    st.markdown(
    """
    <style>
    /* ===== Carte blanche principale ===== */
    .st-key-white_bgc {
        background-color: white;
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.02), 0 2px 4px -1px rgba(0, 0, 0, 0.02);
    }

    /* ===== Badge "Endocrinologie" ===== */
    .fiche-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background-color: #EFF6FF;
        color: #2563EB;
        font-size: 14px;
        font-weight: 500;
        padding: 6px 14px;
        border-radius: 999px;
        margin-bottom: 12px;
    }
    .fiche-badge img {
        width: 16px;
        height: 16px;
    }

    /* ===== Titre pathologie ===== */
    .fiche-title {
        font-size: 32px;
        font-weight: 800;
        margin-top: 4px;
        margin-bottom: 16px;
    }

    /* ===== Séparateur sous le header de la fiche ===== */
    .fiche-divider {
        border: none;
        border-top: 1px solid #E2E8F0;
        margin: 16px 0 24px 0;
    }

    /* ===== Sous-titres de section (Description, Médicaments...) ===== */
    .fiche-section-title {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 18px;
        font-weight: 700;
        margin-bottom: 12px;
        margin-top: 8px;
    }
    .fiche-section-title img {
        width: 20px;
        height: 20px;
    }

    /* ===== Barres de recherche (filtre haut + recherche fiche) ===== */
    .st-key-filter_box input,
    .st-key-search_box input {
        border-radius: 10px !important;
        border: 1px solid #E2E8F0 !important;
        color: #64748B !important;
        padding-left: 40px !important;
        background-image: url("[INSERER PATH LOUPE - encoder en base64 ou data URI]");
        background-repeat: no-repeat;
        background-position: 14px center;
        background-size: 18px 18px;
    }

    /* ===== Cartes médicaments ===== */
    .med-card {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 12px;
    }
    .med-card-title {
        font-weight: 700;
        font-size: 15px;
        margin-bottom: 4px;
    }
    .med-card-desc {
        font-size: 14px;
        color: #64748B;
        line-height: 1.4;
    }

    /* ===== Bloc Alimentation & Diète ===== */
    .diet-box {
        background-color: #F0FDF4;
        border: 1px solid #BBF7D0;
        border-radius: 12px;
        padding: 16px;
    }
    .diet-item {
        display: flex;
        align-items: flex-start;
        gap: 10px;
        margin-bottom: 16px;
        font-size: 14px;
        line-height: 1.4;
    }
    .diet-item:last-child {
        margin-bottom: 0;
    }
    .diet-item img {
        width: 18px;
        height: 18px;
        margin-top: 2px;
        flex-shrink: 0;
    }
    </style>
    """,
    unsafe_allow_html=True
    )

    # ===== Header : logo + titre + filtre =====
    col_title, col_filter = st.columns([ 4, 2], vertical_alignment="center")

    with col_title:
        st.markdown("## 📚 Répertoire des pathologies PAS ENCORE FAIT")
    with col_filter:
        with st.container(key="filter_box"):
            st.text_input(
                "Filtre",
                placeholder="Filtrer la liste...",
                label_visibility="collapsed"
            )

    st.write("")

    # ===== Carte de la fiche pathologie =====
    with st.container(key="white_bgc"):
        col1, col2 = st.columns([2, 1], vertical_alignment="top")

        with col1:
            st.markdown(
                f"""
                <div class="fiche-badge">
                    <img src="./svg/information.svg">
                    Endocrinologie
                </div>
                
                """,
                unsafe_allow_html=True
            )
            st.markdown("### Diabète de type 2")

        with col2:
            with st.container(key="search_box"):
                st.text_input(
                    "Recherche fiche",
                    placeholder="Rechercher dans la fiche...",
                    label_visibility="collapsed"
                )

        st.markdown('<hr class="fiche-divider">', unsafe_allow_html=True)

        # ===== Description =====
        st.markdown(
            """
            <div class="fiche-section-title">
                <img src="./svg/book-open-svgrepo-com.svg"> Description
            </div>
            """,
            unsafe_allow_html=True
        )
        st.markdown(
            """
            Le diabète de type 2 est une maladie chronique caractérisée par une glycémie
            (taux de sucre dans le sang) trop élevée. Il survient généralement lorsque
            l'organisme devient résistant à l'insuline ou n'en produit pas suffisamment
            pour maintenir un taux de glucose normal. Cette condition est souvent
            associée au mode de vie, notamment à l'alimentation et au manque d'activité
            physique.
            """
        )

        st.write("")

        # ===== Médicaments recommandés / Alimentation & Diète =====
        col_med, col_diet = st.columns(2, vertical_alignment="top")

        with col_med:
            st.markdown(
                """
                <div class="fiche-section-title">
                    <img src="[./svg/drugs-svgrepo-com(1).svg"> Médicaments recommandés
                </div>
                """,
                unsafe_allow_html=True
            )

            medicaments = [
                ("Metformine", "Traitement de première intention. Améliore la sensibilité à l'insuline."),
                ("Inhibiteurs de la DPP-4", "Aident à augmenter le taux d'incrétines, stimulant la libération d'insuline."),
                ("Agonistes des récepteurs du GLP-1", "Ralentissent la digestion et réduisent l'appétit, souvent sous forme injectable."),
            ]
            for titre, desc in medicaments:
                st.markdown(
                    f"""
                    <div class="med-card">
                        <div class="med-card-title">{titre}</div>
                        <div class="med-card-desc">{desc}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        with col_diet:
            st.markdown(
                """
                <div class="fiche-section-title">Alimentation &amp; Diète</div>
                """,
                unsafe_allow_html=True
            )

            diet_items = [
                ("[INSERER PATH ICONE CHECK VERT]", "Privilégier les glucides complexes à faible indice glycémique (légumineuses, céréales complètes)."),
                ("[INSERER PATH ICONE CHECK VERT]", "Augmenter l'apport en fibres (légumes verts, fruits entiers) pour ralentir l'absorption des sucres."),
                ("[INSERER PATH ICONE ALERTE ORANGE]", "Limiter drastiquement les sucres ajoutés, les boissons sucrées et les produits ultra-transformés."),
                ("[INSERER PATH ICONE CHECK VERT]", "Maintenir des horaires de repas réguliers pour stabiliser la glycémie."),
            ]

            items_html = "".join(
                f'<div class="diet-item"><img src="{icon}">{text}</div>'
                for icon, text in diet_items
            )
            st.markdown(f'<div class="diet-box">{items_html}</div>', unsafe_allow_html=True)



# 🩺 Symptom-to-Disease Predictor

Application web interactive permettant d'estimer une pathologie à partir d'une sélection de symptômes.

## 💡 Ce que fait l'application
Développée avec **Streamlit**, l'application offre une interface épurée en français où l'utilisateur peut renseigner ses symptômes. Le système analyse la saisie, prédit la maladie la plus probable parmi 100 pathologies, calcule un indice de confiance dynamique et affiche une description détaillée de la maladie associée.

## 🤖 Le Modèle
Le cœur prédictif repose sur un algorithme de **Régression Logistique** issu de *scikit-learn* :
- **Jeu de données :** SympScan (~96 000 observations).
- **Variables d'entrée :** 131 symptômes binaires (présence / absence).
- **Variable cible :** 100 classes de maladies.
- **Performance :** Une exactitude (*Accuracy*) d'environ **89,85 %** sur l'ensemble de test.
- L'application repose sur une **Régression Logistique**. À partir d'un vecteur de 131 symptômes binaires (0 ou 1), le modèle calcule une somme pondérée des caractéristiques. Les scores bruts obtenus pour les 100 classes de maladies sont ensuite convertis en probabilités via la fonction **Softmax**, permettant d'identifier la pathologie la plus probable et d'afficher son indice de confiance. Le modèle atteint une exactitude de **89,85 %** sur l'ensemble de test.

Ce projet est un projet personel étudiant.

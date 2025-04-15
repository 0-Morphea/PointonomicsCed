import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Configuration de la page Streamlit
st.set_page_config(page_title="Points Autonomics - Simulation Streamlit", layout="wide")

# --- Introduction ---
st.title("Simulation du Système Points Autonomics")
st.markdown("""
Cette application Streamlit permet de tester et valider le mécanisme de distribution de Bamboo Points.
Utilisez la sidebar pour configurer les paramètres de simulation et observez les résultats en temps réel.
""")

# --- Sidebar : Configuration de Simulation ---
st.sidebar.header("Paramètres de Simulation")

# Paramètres généraux
nb_users = st.sidebar.number_input("Nombre d'utilisateurs simulés", min_value=100, max_value=5000, value=1000, step=100)
nb_weeks = st.sidebar.slider("Nombre de semaines de simulation", min_value=2, max_value=12, value=4)
weekly_cap = st.sidebar.number_input("Plafond hebdomadaire de points", min_value=50, max_value=1000, value=200)

# Configuration des quêtes
st.sidebar.subheader("Configuration des Quêtes")
# Exemple de quêtes par défaut
default_quests = [
    {"name": "Connexion quotidienne", "points": 1, "probability": 0.9},
    {"name": "Connexion Wallet", "points": 10, "probability": 0.7},
    {"name": "Connexion CEX", "points": 100, "probability": 0.2},
    {"name": "Participation Réseaux Sociaux", "points": 50, "probability": 0.3},
]

# Possibilité d'éditer manuellement le nombre de quêtes (pour simplification, on utilise la liste par défaut)
quests_df = pd.DataFrame(default_quests)
st.sidebar.dataframe(quests_df)

# --- Moteur de Simulation ---
st.header("Résultats de la Simulation")

@st.cache(suppress_st_warning=True)
def simulate_points(quests, nb_users, weeks, weekly_cap):
    simulation = []
    # Pour chaque utilisateur simulé
    for user in range(nb_users):
        total_points = 0
        # Simulation semaine par semaine
        for week in range(weeks):
            week_points = 0
            # Pour chaque quête configurée
            for quest in quests:
                if np.random.rand() < quest['probability']:
                    week_points += quest['points']
            week_points = min(week_points, weekly_cap)
            total_points += week_points
        simulation.append(total_points)
    return np.array(simulation)

points_data = simulate_points(default_quests, nb_users, nb_weeks, weekly_cap)
mean_points = np.mean(points_data)
std_points = np.std(points_data)

st.markdown(f"**Points moyens par utilisateur sur {nb_weeks} semaines :** {mean_points:.2f} ± {std_points:.2f}")

# --- Visualisation ---
st.subheader("Distribution des Bamboo Points")
fig, ax = plt.subplots(figsize=(10, 5))
ax.hist(points_data, bins=30, color="skyblue", edgecolor="black")
ax.set_title("Répartition des Bamboo Points accumulés")
ax.set_xlabel("Points totaux")
ax.set_ylabel("Nombre d'utilisateurs")
st.pyplot(fig)

# --- Indicateurs Clés (KPI) ---
st.subheader("Indicateurs Clés")
kpi_data = {
    "DAU (simulé)": np.random.randint(500, 1500),
    "WAU (simulé)": np.random.randint(2000, 5000),
    "Taux de Rétention (7 jours, simulé)": f"{np.random.randint(30,60)}%",
    "Taux de Rétention (30 jours, simulé)": f"{np.random.randint(20,40)}%",
    "Quêtes complétées / Utilisateur": round(mean_points / 20, 2),  # Exemple de calcul
}
kpi_df = pd.DataFrame(kpi_data, index=["Valeur"])
st.dataframe(kpi_df)

# --- Section Feedback et Axes d'Amélioration ---
st.header("Axes d'Amélioration et Prochaines Étapes")
st.markdown("""
- **Test de Paramètres :** Expérimentez différentes valeurs pour le nombre d’utilisateurs, le nombre de semaines, et le plafond hebdomadaire.
- **Ajout de Quêtes :** Possibilité d’ajouter, modifier ou supprimer des quêtes pour tester l’impact sur la distribution.
- **Scénarios Multiples :** Simuler différents scénarios d’engagement (optimiste vs pessimiste).
- **Export des Données :** Option pour exporter les résultats sous forme de CSV pour analyse externe.
""")

st.markdown("---")
st.markdown("Cette application Streamlit sert de prototype pour le système Points Autonomics et permet une itération rapide afin de valider et affiner les mécaniques proposées.")


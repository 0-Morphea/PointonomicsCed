import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Pointonomics - Démo Bamboo Points", layout="wide")

# --- Introduction ---
st.title("Dashboard Interactif - Pointonomics & CityLabs")
st.markdown("""
Ce dashboard présente la simulation et l'implémentation du système de Bamboo Points.  
Il illustre la conversion des anciens Cede Points, la configuration des quêtes, et le suivi des indicateurs clés influençant l'engagement et la rétention des utilisateurs.
""")

# --- Configuration des Quêtes via la Sidebar ---
st.sidebar.header("Configuration des Quêtes")
default_quests = [
    {"name": "Connexion quotidienne", "points": 1, "probability": 0.9},
    {"name": "Connexion Wallet", "points": 10, "probability": 0.7},
    {"name": "Connexion CEX", "points": 100, "probability": 0.2},
    {"name": "Participation Réseaux Sociaux", "points": 50, "probability": 0.3},
]

# Nombre d'utilisateurs et nombre de semaines pour la simulation
nb_users = st.sidebar.number_input("Nombre d'utilisateurs simulés", min_value=100, max_value=5000, value=1000, step=100)
nb_weeks = st.sidebar.slider("Nombre de semaines", min_value=2, max_value=12, value=4)

# Affichage de la configuration des quêtes
quests_df = pd.DataFrame(default_quests)
st.subheader("Quêtes Configurées")
st.dataframe(quests_df)

# --- Simulation de Distribution des Bamboo Points ---
st.header("Simulation de Distribution des Bamboo Points")

def simulate_points(quests, nb_users=1000, weeks=4):
    simulation = []
    for user in range(nb_users):
        total_points = 0
        for week in range(weeks):
            week_points = 0
            for quest in quests:
                if np.random.rand() < quest['probability']:
                    week_points += quest['points']
            # Application d'un plafond hebdomadaire de 200 points
            week_points = min(week_points, 200)
            total_points += week_points
        simulation.append(total_points)
    return np.array(simulation)

points_data = simulate_points(default_quests, nb_users=nb_users, weeks=nb_weeks)
mean_points = np.mean(points_data)
std_points = np.std(points_data)

st.write(f"**Points moyens par utilisateur sur {nb_weeks} semaines :** {mean_points:.2f} ± {std_points:.2f}")

# Visualisation de la répartition des points
fig, ax = plt.subplots(figsize=(10, 5))
ax.hist(points_data, bins=30, color="skyblue", edgecolor="black")
ax.set_title("Répartition des Bamboo Points accumulés")
ax.set_xlabel("Points totaux accumulés")
ax.set_ylabel("Nombre d'utilisateurs")
st.pyplot(fig)

# --- Suivi des Indicateurs Clés (KPI) pour CityLabs ---
st.header("Indicateurs Clés d'Engagement & Rétention")
kpi_data = {
    "DAU": np.random.randint(500, 1500),
    "WAU": np.random.randint(2000, 5000),
    "Taux de Rétention (7 jours)": f"{np.random.randint(30, 60)}%",
    "Taux de Rétention (30 jours)": f"{np.random.randint(20, 40)}%",
    "Quêtes Complétées / Utilisateur": round(np.mean(points_data) / 20, 2),
    "Utilisation du Shop (%)": f"{np.random.randint(10, 30)}%",
}

kpi_df = pd.DataFrame(kpi_data, index=["Valeur"])
st.dataframe(kpi_df)

# --- Présentation des Prochaines Étapes Stratégiques ---
st.header("Prochaines Étapes et Voie d'Amélioration")
st.markdown("""
- **Validation des ratios de conversion :** Finaliser la méthode de conversion des anciens Cede Points en Bamboo Points en collaboration avec l’équipe "Silly Points".
- **Simulation Économique Avancée :** Déployer des simulations Monte Carlo pour affiner la distribution des Bamboo Points et éviter une inflation excessive.
- **Déploiement Pilote & Tests Utilisateurs :** Mettre


import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Configuration de la page
st.set_page_config(page_title="Simulation Points Autonomics", layout="wide")

# --- Introduction ---
st.title("Simulation du Système Points Autonomics")
st.markdown("""
Cette application permet de simuler et tester les différentes mécaniques de distribution des Bamboo Points.
Les données sont générées aléatoirement afin de valider le modèle et d'observer l'impact des paramètres configurables.
""")

# --- Sidebar : Configuration de Simulation ---
st.sidebar.header("Paramètres de Simulation")

# Nombre d'utilisateurs simulés (données aléatoires)
nb_users = st.sidebar.number_input("Nombre d'utilisateurs simulés", min_value=100, max_value=5000, value=1000, step=100)

# Nombre de semaines de simulation
nb_weeks = st.sidebar.slider("Nombre de semaines de simulation", min_value=2, max_value=12, value=4)

# Plafond hebdomadaire de points
weekly_cap = st.sidebar.number_input("Plafond hebdomadaire de points", min_value=50, max_value=1000, value=200)

# Configuration des quêtes (exemple de données par défaut)
st.sidebar.subheader("Quêtes")
# Vous pouvez modifier ces valeurs pour tester d'autres configurations
default_quests = [
    {"name": "Connexion quotidienne", "points": 1, "probability": 0.9},
    {"name": "Connexion Wallet", "points": 10, "probability": 0.7},
    {"name": "Connexion CEX", "points": 100, "probability": 0.2},
    {"name": "Participation Réseaux Sociaux", "points": 50, "probability": 0.3},
]

# Option pour générer des quêtes aléatoires (facultatif)
if st.sidebar.checkbox("Générer des quêtes aléatoires"):
    nb_quests = st.sidebar.number_input("Nombre de quêtes", min_value=2, max_value=10, value=4)
    default_quests = []
    for i in range(int(nb_quests)):
        quest = {
            "name": f"Quête {i+1}",
            "points": np.random.randint(1, 101),       # Points aléatoires entre 1 et 100
            "probability": round(np.random.uniform(0.1, 0.9), 2)  # Probabilité entre 0.1 et 0.9
        }
        default_quests.append(quest)

quests_df = pd.DataFrame(default_quests)
st.sidebar.dataframe(quests_df)

# --- Moteur de Simulation ---
st.header("Résultats de la Simulation")

@st.cache(suppress_st_warning=True)
def simulate_points(quests, nb_users, weeks, weekly_cap):
    simulation = []
    # Simulation pour chaque utilisateur
    for user in range(nb_users):
        total_points = 0
        # Simulation semaine par semaine
        for week in range(weeks):
            week_points = 0
            for quest in quests:
                # Génération d'une valeur aléatoire et comparaison avec la probabilité
                if np.random.rand() < quest['probability']:
                    week_points += quest['points']
            # Application du plafond hebdomadaire
            week_points = min(week_points, weekly_cap)
            total_points += week_points
        simulation.append(total_points)
    return np.array(simulation)

# Exécution de la simulation
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

# --- Indicateurs Clés ---
st.subheader("Indicateurs Clés")
kpi_data = {
    "Nombre d'utilisateurs simulés": nb_users,
    "Nombre de semaines simulées": nb_weeks,
    "Plafond hebdomadaire": weekly_cap,
    "Points moyens par utilisateur": round(mean_points, 2),
    "Écart-type des points": round(std_points, 2),
    "Nombre total de quêtes configurées": len(default_quests),
}
kpi_df = pd.DataFrame(kpi_data, index=["Valeur"])
st.dataframe(kpi_df)

# --- Feedback et Axes d'Amélioration ---
st.header("Axes d'Amélioration et Prochaines Étapes")
st.markdown("""
- **Testez différentes configurations de quêtes et paramètres** pour observer l'impact sur la distribution.
- **Expérimentez avec des scénarios multiples** en modifiant les probabilités et les montants des quêtes.
- **Analysez l'effet du plafond hebdomadaire** sur la distribution globale des points.
- **Utilisez ces résultats pour affiner vos hypothèses** et établir des règles de récompense équilibrées.
""")

st.markdown("---")
st.markdown("Cette simulation vous aide à tester et itérer sur les mécaniques du système Points Autonomics afin de mieux comprendre leur impact et de préparer leur intégration opérationnelle.")

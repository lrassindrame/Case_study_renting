import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.neighbors import KNeighborsClassifier
import matplotlib.pyplot as pltcd
import numpy as np
import pm4py
import matplotlib.pyplot as plt

# Charger l'event log depuis un fichier XES
file_path = "./datasets/renting_log_high.xes"  # Chemin vers votre fichier XES
dataframe = pm4py.read_xes(file_path)

# Prévisualisation des données
# print(dataframe.head())

# Sélection des colonnes pertinentes pour l'analyse
dataframe = dataframe[['case:concept:name', 'concept:name', 'time:timestamp', 'resource']]

# Extraction des statistiques des traces pour créer des profils utilisateurs
profiles = []
for case_id, group in dataframe.groupby("case:concept:name"):
    profile = {
        "case_id": case_id,
        "num_activities": group["concept:name"].nunique(),
        "unique_resources": group["resource"].nunique(),
        "trace_duration": (group["time:timestamp"].max() - group["time:timestamp"].min()).total_seconds()
    }
    profiles.append(profile)

# Transformation en dataframe
profiles_df = pd.DataFrame(profiles)

# Préparation des données pour le clustering
X = profiles_df.drop(columns=["case_id"])
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# ---
# Application de KMeans pour créer les clusters
n_clusters = 2  # Nombre de clusters
kmeans = KMeans(n_clusters=n_clusters, random_state=42)
clusters = kmeans.fit_predict(X_scaled)

# Ajout des clusters aux données
profiles_df["cluster"] = clusters

# Visualisation des clusters avec PCA
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

plt.figure(figsize=(8, 6))
for cluster in range(n_clusters):
    cluster_points = X_pca[clusters == cluster]
    plt.scatter(cluster_points[:, 0], cluster_points[:, 1], label=f"Cluster {cluster}")
plt.title("Visualisation des clusters (PCA)")
plt.xlabel("PC1")
plt.ylabel("PC2")
plt.legend()
plt.show()

# ---
# Préparation du modèle de prédiction (K-Nearest Neighbors)
knn = KNeighborsClassifier(n_neighbors=n_clusters)
knn.fit(X_scaled, clusters)

# Exemple d'une nouvelle trace
new_trace = {
    "num_activities": 25,  # Nombre d'activités uniques
    "unique_resources": 8,  # Nombre de ressources uniques
    "trace_duration": 3600 * 45  # Durée de la trace en secondes
}

# Transformation de la nouvelle trace
new_trace_df = pd.DataFrame([new_trace])
new_trace_scaled = scaler.transform(new_trace_df)

# Prédiction de la classe
predicted_cluster = knn.predict(new_trace_scaled)
print(f"La nouvelle trace appartient au cluster {predicted_cluster[0]}")

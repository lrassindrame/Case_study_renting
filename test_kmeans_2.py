import pandas as pd
import pm4py
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

# === Charger les données depuis un fichier XES === #
file_path = "./datasets/renting_log_high.xes"  # Chemin vers votre fichier XES
dataframe = pm4py.read_xes(file_path)

# === Prévisualisation des données === #
print(dataframe.columns.tolist())

# === Préparation des données pour le clustering === #
# Extraction des informations pertinentes de la trace
trace_profiles = []

for case_id, group in dataframe.groupby("case:concept:name"):
    # print(f"group : {group}")
    profile = {
        "case_id": case_id,
        "num_activities": group["concept:name"].nunique(),
        "unique_resources": group["resource"].nunique(),
        "trace_duration": (group["time:timestamp"].max() - group["time:timestamp"].min()).total_seconds(),
        "german_speaking": group["case:german speaking"].iloc[0],
        "yearsOfEducation": group["case:yearsOfEducation"].iloc[0],
        "age": group["case:age"].iloc[0],
        "gender": group["case:gender"].iloc[0],
        "citizen": group["case:citizen"].iloc[0],
        "protected": group["case:protected"].iloc[0],
        "married": group["case:married"].iloc[0],
    }
    trace_profiles.append(profile)

# Création d'un DataFrame pour les profils
profiles_df = pd.DataFrame(trace_profiles)

# Normalisation des données
X = profiles_df.drop(columns=["case_id"])
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# === Clustering avec KMeans === #
sse = []
k_range = range(1, 11)

# Calcul du SSE pour différents nombres de clusters
for k in k_range:
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(X_scaled)
    sse.append(kmeans.inertia_)  # Sum of Squared Errors (SSE)

# Affichage de l'évolution du SSE (méthode du coude)
plt.figure(figsize=(8, 6))
plt.plot(k_range, sse, marker='o')
plt.title("Méthode du coude pour déterminer le nombre optimal de clusters")
plt.xlabel("Nombre de clusters (k)")
plt.ylabel("SSE (Sum of Squared Errors)")
plt.show()

# Choix du nombre de clusters
optimal_k = 2  # Basé sur l'inspection visuelle du graphe du coude
kmeans = KMeans(n_clusters=optimal_k, random_state=42)
clusters = kmeans.fit_predict(X_scaled)

# Ajout des clusters aux données
profiles_df["cluster"] = clusters

# === Visualisation des clusters avec PCA === #
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

plt.figure(figsize=(8, 6))
for cluster in range(optimal_k):
    cluster_points = X_pca[clusters == cluster]
    plt.scatter(cluster_points[:, 0], cluster_points[:, 1], label=f"Cluster {cluster}")
plt.title("Visualisation des clusters avec PCA")
plt.xlabel("PC1")
plt.ylabel("PC2")
plt.legend()
plt.show()

# === Résumé des clusters === #
print("Résumé des clusters générés :")
numeric_columns = profiles_df.select_dtypes(include=[float, int]).columns
print(profiles_df.groupby("cluster")[numeric_columns].mean())

# === Prédiction de la classe d'une nouvelle trace === #
new_trace = {
    "num_activities": 0,  # Valeur par défaut, à ajuster si nécessaire
    "unique_resources": 0,  # Valeur par défaut, à ajuster si nécessaire
    "trace_duration": 60,  # Valeur par défaut, à ajuster si nécessaire
    "german_speaking": 0,  # 1 pour True, 0 pour False
    "yearsOfEducation": 0,
    "age": 20,  # Valeur par défaut, à ajuster si nécessaire
    "gender": 0,  # Valeur par défaut, à ajuster si nécessaire
    "citizen": 0,  # Valeur par défaut, à ajuster si nécessaire
    "protected": 0,  # Valeur par défaut, à ajuster si nécessaire
    "married": 0  # 1 pour True, 0 pour False
}

# Conversion en DataFrame
new_trace_df = pd.DataFrame([new_trace])

# Normalisation des données de la nouvelle trace
new_trace_scaled = scaler.transform(new_trace_df)

# Prédiction du cluster
predicted_cluster = kmeans.predict(new_trace_scaled)
print(f"La nouvelle trace est prédite pour appartenir au cluster : {predicted_cluster[0]}")
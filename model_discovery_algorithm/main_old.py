import pm4py
import pandas as pd

def log2trace(xeslog, case_id='@@case_index', activity='activity',time='time'):
    trace_log = xeslog.groupby(case_id).apply(lambda x: x.sort_values(time))
    trace_log = trace_log.reset_index(drop=True)
    trace_log['activity_sequence'] = trace_log.groupby(case_id)[activity].transform(lambda x: ','.join(x))
    return trace_log[[case_id, 'activity_sequence']].drop_duplicates()
    

# Fonction pour vérifier si une activité appartient à un cluster
def is_in_cluster(activity, clusters):
    for cluster_nodes in clusters.values():
        if activity in cluster_nodes:
            return True
    return False

# Fonction pour obtenir le nom du cluster auquel appartient une activité
def get_cluster_name(activity, clusters):
    for cluster_name, cluster_nodes in clusters.items():
        if activity in cluster_nodes:
            return cluster_name
    return None

# Fonction pour obtenir le nœud auquel une activité est mappée dans le modèle
def get_mapped_node(activity, clusters):
    if is_in_cluster(activity, clusters):
        return get_cluster_name(activity, clusters)
    return activity

# Fonction pour vérifier la conformité basée sur les transitions définies
def check_conformance(trace_log, transitions, clusters, case_id='@@case_index', activity_sequence='activity_sequence'):
    conformance_results = []
    total_events = 0
    total_deviations = 0

    for _, row in trace_log.iterrows():
        activities = row[activity_sequence].split(',')
        total_events += len(activities)

        # Initialisation
        deviations = 0
        nodes = []
        enabled = set()
        cluster = None
        deviation_types = {
            'unmappable_event': 0,
            'incorrect_initial_activity': 0,
            'invalid_transition': 0,
            'unexpected_cluster_change': 0
        }

        # Prétraitement : Nettoyage des événements non mappables et transformation de la séquence d'événements en une séquence de nœuds
        for activity in activities:
            n = get_mapped_node(activity, clusters)
            if n is None:
                deviations += 1  # Événement non mappable
                deviation_types['unmappable_event'] += 1
                print(f"Trace {row[case_id]}: Déviation - Événement non mappable: {activity}")
            else:
                nodes.append(n)

        # Vérifier que la première activité correspond à l'activité initiale
        if nodes and nodes[0] != 'Apply for Viewing Appointment':
            deviations += 1  # Si ce n'est pas l'activité initiale, c'est une déviation
            deviation_types['incorrect_initial_activity'] += 1
            print(f"Trace {row[case_id]}: Déviation - Première activité incorrecte: {nodes[0]} (attendu: Apply for Viewing Appointment)")

        # Vérification des transitions
        if nodes:
            n = nodes[0]
            if is_in_cluster(n, clusters):
                cluster = n
            enabled.update(transitions.get(n, {}).keys())

        for n in nodes[1:]:
            if n in enabled:
                enabled.update(transitions.get(n, {}).keys())
                if is_in_cluster(n, clusters):
                    cluster = n
                else:
                    cluster = None
            elif is_in_cluster(n, clusters):
                if n == cluster:
                    enabled.update(transitions.get(n, {}).keys())
                    cluster = n
                else:
                    deviations += 1
                    deviation_types['unexpected_cluster_change'] += 1
                    enabled.update(transitions.get(n, {}).keys())
                    cluster = n
                    print(f"Trace {row[case_id]}: Déviation - Changement inattendu de cluster: {cluster} (précédent: {cluster})")
            else:
                deviations += 1
                deviation_types['invalid_transition'] += 1
                enabled.update(transitions.get(n, {}).keys())
                cluster = None
                print(f"Trace {row[case_id]}: Déviation - Transition invalide: {n} après {nodes[nodes.index(n)-1]}")
                print(f"  Transitions attendues: {transitions.get(nodes[nodes.index(n)-1], {})}")

        # Enregistrer les résultats de conformité pour cette trace
        conformance_results.append({
            'trace': row[case_id],
            'deviations': deviations,
            'deviation_types': deviation_types
        })
        total_deviations += deviations

    return conformance_results, total_events, total_deviations


# Calculer la conformité C
def calculate_conformance(total_events, total_deviations):
    M_L = total_events
    d = total_deviations
    C = (M_L - d + 1) / (M_L + 1)
    return C

def calculate_detail(transitions, clusters):
    # Définir les nœuds primitifs et explicites avec leurs significances
    N = list(transitions.keys())

    # Les nœuds dans les clusters ne sont pas explicites
    cluster_nodes = set()
    for cluster_nodes_list in clusters.values():
        cluster_nodes.update(cluster_nodes_list)

    E = [node for node in N if node not in cluster_nodes]
    
    s = {node: sum(transitions[node].values()) for node in N}
    
    sum_s_E = sum(s[e] for e in E)
    sum_s_N = sum(s[n] for n in N)
    dt = sum_s_E / sum_s_N
    return dt

def evaluate_fuzzy_model(xes_filepath,model_transitions_significance,model_clusters):
    # Importer le fichier de log .xes
    log = pm4py.read_xes(xes_filepath)
    log = pm4py.format_dataframe(log)
    trace_log = log2trace(log)

    # Calculer la conformité
    conformance_results, total_events, total_deviations = check_conformance(trace_log, model_transitions_significance, model_clusters)

    # Afficher les résultats de conformité
    for result in conformance_results:
        print(f"Trace: {result['trace']}, Deviations: {result['deviations']}")
        print(f"  Types de déviations: {result['deviation_types']}")

    # Afficher les clusters
    print("\nClusters:")
    for cluster, nodes in model_clusters.items():
        print(f"{cluster}: {', '.join(nodes)}")

    C = calculate_conformance(total_events, total_deviations)
    print(f"\nConformité C: {C}")

    dt = calculate_detail(model_transitions_significance, model_clusters)
    print(f"Détail dt: {dt}")
    
# Définir manuellement les informations du modèle fuzzy avec significances et clusters
transitions_high_res = {
    'Apply for Viewing Appointment': {'Set Appointment': 0.423},
    'Set Appointment': {'View The Property': 0.357},
    'View The Property': {'Hand In The Paperwork': 0.296},
    'Hand In The Paperwork': {'Check Paperwork': 0.291},
    'Check Paperwork': {'Screen Prospective Tenant': 0.313},
    'Screen Prospective Tenant': {'Reject Prospective Tenant': 0.902, 'Extensive Screening': 0.188,'Sign Contract': 0.131},
    'Extensive Screening': {'Reject Prospective Tenant': 0.902, 'Sign Contract': 0.131},
    'Sign Contract': {'Move In': 0.112, 'Cluster_17': 0.063},
    'Move In': {'Pay Rent': 0.713, 'Miss Rent Payment': 0.045},
    'Miss Rent Payment': {'Miss Rent Payment': 0.045, 'Issue Warning': 0.041},
    'Issue Warning': {'Issue Warning': 0.041, 'Evict Tenant': 0.649, 'Accept Late Payment': 0.054},
    'Accept Late Payment': {'Accept Late Payment': 0.054, 'Pay Rent': 0.713, 'Miss Rent Payment': 0.045},
    'Pay Rent': {'Pay Rent': 0.713, 'Tenant Cancels Appartment': 0.741,'Miss Rent Payment': 0.045, 'Cluster_17': 0.063},
    'Cluster_17': {'Pay Rent': 0.713, 'Tenant Cancels Appartment': 0.741}  # Transition du cluster vers des activités
}

clusters_high_res = {
    'Cluster_17': ['Move In', 'Miss Rent Payment', 'Issue Warning', 'Accept Late Payment']
}

high_res_filepath = './datasets/renting_log_high.xes'
evaluate_fuzzy_model(high_res_filepath,transitions_high_res,clusters_high_res)


"""
# Importer le fichier de log .xes
log_high_res = pm4py.read_xes('./datasets/renting_log_high.xes')
log_high_res = pm4py.format_dataframe(log_high_res)
trace_log_high_res = log2trace(log_high_res)

# Calculer la conformité
conformance_results, total_events, total_deviations = check_conformance(trace_log_high_res, transitions_high_res, clusters_high_res)

# Afficher les résultats de conformité
for result in conformance_results:
    print(f"Trace: {result['trace']}, Deviations: {result['deviations']}")
    print(f"  Types de déviations: {result['deviation_types']}")

# Afficher les clusters
print("\nClusters:")
for cluster, nodes in clusters_high_res.items():
    print(f"{cluster}: {', '.join(nodes)}")

C = calculate_conformance(total_events, total_deviations)
print(f"\nConformité C: {C}")

dt = calculate_detail(transitions_high_res, clusters_high_res)
print(f"Détail dt: {dt}")
"""


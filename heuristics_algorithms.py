from utils.file import *
import pm4py
import pandas as pd
import os
from tabulate import tabulate  # Importer tabulate

def apply_heuristic_miner(input_file, output_img_path):
    data = pd.read_csv(input_file, sep=',')
    
    dataframe = pm4py.format_dataframe(data, case_id='@@case_index', activity_key='activity', timestamp_key='time')
    log = pm4py.convert_to_event_log(dataframe)
    net, im, fm = pm4py.discover_petri_net_heuristics(log)
    
    # Calcul des différentes métriques
    fitness_trb = pm4py.fitness_token_based_replay(log, net, im, fm)
    precision_foo = pm4py.precision_footprints(log, net, im, fm)
    precision_trb = pm4py.precision_token_based_replay(log, net, im, fm)
    generalization = pm4py.generalization_tbr(log, net, im, fm)
    simplicity = pm4py.simplicity_petri_net(net, im, fm)
    is_sound, soundness_dict = pm4py.check_soundness(net, im, fm)
    
    # Extraire des informations spécifiques pour une meilleure lisibilité (ex: fitness)
    fitness_summary = {
        "Fitness globale": fitness_trb['log_fitness'],  # Afficher la fitness globale
        "Précision des traces": fitness_trb['perc_fit_traces'],  # Afficher la précision des traces
        "Fitness moyenne des traces": fitness_trb['average_trace_fitness']  # Fitness moyenne des traces
    }
    
    # Préparer les résultats sous forme de liste de tuples pour tabulate
    results = [
        ("Fitness (Token-based Replay)", fitness_summary),
        ("Précision des Empreintes", precision_foo),
        ("Précision (Token-based Replay)", precision_trb),
        ("Généralisation", generalization),
        ("Simplicité du Réseau de Petri", simplicity),
        ("Réseau de Petri Sonore", "Oui" if is_sound else "Non"),
        ("Alignements de Précision", precision_alg if is_sound else "N/A")
    ]
    
    # Utilisation de tabulate pour afficher les résultats de manière propre
    print("="*50)
    print(f"Traitement du fichier : {input_file}")
    print("="*50)
    
    # Convertir le dictionnaire de fitness en string lisible pour tabulate
    formatted_results = []
    for metric, value in results:
        if isinstance(value, dict):
            value = "\n".join([f"{key}: {val}" for key, val in value.items()])  # Formater les sous-valeurs du dictionnaire
        formatted_results.append([metric, value])
    
    # Affichage avec tabulate
    print(tabulate(formatted_results, headers=["Métrique", "Valeur"], tablefmt="grid"))
    print("="*50)
    
    # Sauvegarde du graphique
    pm4py.save_vis_petri_net(net, im, fm, output_img_path)
    print(f"\nLe graphique du réseau de Petri a été sauvegardé sous: {output_img_path}")
    print("="*50)

def process_files_in_directory(input_directory, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    file_paths = get_file_paths(input_directory, extension=".csv")
    
    for input_file in file_paths:
        output_img_path = os.path.join(output_directory, f"{os.path.splitext(os.path.basename(input_file))[0]}_petri_net.png")
        
        print(f"\n### Début du traitement pour le fichier : {input_file} ###")
        apply_heuristic_miner(input_file, output_img_path)

input_directory = './datasets_csv'
output_directory = './heuristics_petri_net_images'

process_files_in_directory(input_directory, output_directory)

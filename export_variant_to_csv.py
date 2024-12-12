import pm4py
import pandas as pd
from pm4py.algo.filtering.log.variants import variants_filter

# Charger le fichier XES
file_path = "./datasets/renting_log_high.xes"  # Chemin vers votre fichier XES
file_name = file_path.split("\\")[-1].split(".")[0]
event_log = pm4py.read_xes(file_path)

# Obtenir les variantes avec la méthode adaptée à la version 2.7.10
variants = variants_filter.get_variants(event_log)

# Réduire les données en ne gardant qu'une seule trace par variante
reduced_traces = []
i = 0
for variant, traces in variants.items():
    # Prendre la première trace de chaque variante
    trace = traces[0]
    i += 1
    if i < 2:
        print(trace)
    trace_data = {
        "case_id": trace.attributes.get("concept:name", "unknown"),
        "variant": variant,
        "num_events": len(trace),
        "success": any(event["concept:name"] == "Sign Contract" for event in trace),  # Succès si "Sign contract" présent
    }
    # Ajouter les attributs associés à cette trace (e.g., âge, genre, etc.)
    for attr, value in trace.attributes.items():
        trace_data[attr] = value
    reduced_traces.append(trace_data)

# Convertir en DataFrame pour manipulation
df_reduced = pd.DataFrame(reduced_traces)

# Sauvegarder le DataFrame en CSV
output_csv = "./datasets/reduced_variants" + file_name + ".csv"
df_reduced.to_csv(output_csv, index=False)

print(f"Réduction terminée. Fichier exporté vers {output_csv}")

import os
import xml.etree.ElementTree as ET

def remove_keys(input_file, output_file, trace_keys_to_remove, event_keys_to_remove):
    tree = ET.parse(input_file)
    root = tree.getroot()

    namespace = {"xes": "http://www.xes-standard.org/"}
    ET.register_namespace("", "http://www.xes-standard.org/")

    for trace in root.findall(".//xes:trace", namespace):
        for key in trace_keys_to_remove:
            for element in trace.findall(f"xes:*[@key='{key}']", namespace):
                trace.remove(element)

    for event in root.findall(".//xes:event", namespace):
        for key in event_keys_to_remove:
            for element in event.findall(f"xes:*[@key='{key}']", namespace):
                event.remove(element)

    tree.write(output_file, encoding="utf-8", xml_declaration=True)
    print(f"Les propriétés {', '.join(trace_keys_to_remove + event_keys_to_remove)} ont été supprimées. Le fichier modifié est enregistré sous {output_file}.")

def process_directory(input_directory, output_directory, trace_keys_to_remove, event_keys_to_remove):
    """Traiter tous les fichiers XES dans un répertoire et sauvegarder les fichiers nettoyés."""
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    for filename in os.listdir(input_directory):
        if filename.endswith(".xes"):
            input_file_path = os.path.join(input_directory, filename)
            output_file_name = f"{os.path.splitext(filename)[0]}_clean.xes"
            output_file_path = os.path.join(output_directory, output_file_name)
            
            remove_keys(input_file_path, output_file_path, trace_keys_to_remove, event_keys_to_remove)

input_directory = "datasets"
output_directory = "datasets_clean"
trace_keys_to_remove = ["case"]
event_keys_to_remove = ["time", "activity", "resource"]

process_directory(input_directory, output_directory, trace_keys_to_remove, event_keys_to_remove)

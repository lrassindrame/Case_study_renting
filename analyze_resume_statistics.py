import os
import xml.etree.ElementTree as ET

def analyze_log(input_file):
    tree = ET.parse(input_file)
    root = tree.getroot()

    namespace = {"xes": "http://www.xes-standard.org/"}
    
    traces = root.findall(".//xes:trace", namespace)
    
    num_traces = len(traces)
    print(f"==============================================")
    print(f"Fichier: {os.path.basename(input_file)}")
    print(f"==============================================")
    print(f"Nombre total de traces : {num_traces}")
    
    event_counts = []

    for trace in traces:
        events = trace.findall("xes:event", namespace)
        num_events = len(events)
        event_counts.append(num_events)

    total_events = sum(event_counts)
    average_events = total_events / num_traces if num_traces > 0 else 0
    min_events = min(event_counts) if event_counts else 0
    max_events = max(event_counts) if event_counts else 0

    print(f"\nMoyenne du nombre d'événements par trace : {average_events:.2f}")
    print(f"Nombre minimum d'événements par trace : {min_events}")
    print(f"Nombre maximum d'événements par trace : {max_events}")

def do_process_with_all_into_directory(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".xes"):
            file_path = os.path.join(directory, filename)
            analyze_log(file_path)

input_directory = "datasets"
do_process_with_all_into_directory(input_directory)

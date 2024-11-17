import os
import xml.etree.ElementTree as ET
from collections import Counter

def analyze_duplicates(input_file):
    tree = ET.parse(input_file)
    root = tree.getroot()

    namespace = {"xes": "http://www.xes-standard.org/"}
    
    traces = root.findall(".//xes:trace", namespace)

    print(f"==============================================")
    print(f"Fichier: {os.path.basename(input_file)}")
    print(f"==============================================")
    
    trace_hashes = []
    duplicate_traces = 0
    for trace in traces:
        trace_hash = hash(str(trace))
        if trace_hash in trace_hashes:
            duplicate_traces += 1
        else:
            trace_hashes.append(trace_hash)
    
    print(f"\nNombre de doublons dans les traces : {duplicate_traces}")

    duplicate_events = 0
    event_hashes = []
    duplicate_keys = [] 
    
    for trace in traces:
        events = trace.findall("xes:event", namespace)
        for event in events:
            event_values = {}
            for string_elem in event.findall("xes:string", namespace):
                key = string_elem.get('key')
                value = string_elem.get('value')
                event_values[key] = value

            for date_elem in event.findall("xes:date", namespace):
                key = date_elem.get('key')
                value = date_elem.get('value')
                event_values[key] = value

            for key, value in event_values.items():
                if value in event_hashes:
                    duplicate_events += 1
                    duplicate_keys.append(key)
                else:
                    event_hashes.append(value)
    
    print(f"Nombre de doublons dans les événements : {duplicate_events}")
    if duplicate_keys:
        print("\nClés en doublon dans les événements :")
        for key in set(duplicate_keys):  
            print(f"- {key}")

def analyze_missing_properties(input_file):
    tree = ET.parse(input_file)
    root = tree.getroot()

    namespace = {"xes": "http://www.xes-standard.org/"}
    
    traces = root.findall(".//xes:trace", namespace)
    
    missing_properties = []
    for trace in traces:
        events = trace.findall("xes:event", namespace)
        for event in events:
            for key in ['activity', 'resource', 'time:timestamp']:
                property_elem = event.find(f"xes:string[@key='{key}']", namespace) if key != 'time:timestamp' else event.find(f"xes:date[@key='{key}']", namespace)
                if property_elem is None:
                    missing_properties.append(key)

    missing_count = Counter(missing_properties)

    if missing_count:
        print("\nPropriétés manquantes dans les événements :")
        for prop, count in missing_count.items():
            print(f"- {prop} : {count} fois")

def do_process_with_all_into_directory(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".xes"):
            file_path = os.path.join(directory, filename)
            analyze_duplicates(file_path)
            analyze_missing_properties(file_path)

input_directory = "datasets"
do_process_with_all_into_directory(input_directory)

import xml.etree.ElementTree as ET
import csv

def parse_file_xes(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    traces = []
    for trace in root.findall('.//{http://www.xes-standard.org/}trace'):
        trace_data = {}
        for elem in trace:
            if elem.tag.endswith('string'):
                trace_data[elem.attrib['key']] = elem.attrib['value']
            elif elem.tag.endswith('boolean'):
                trace_data[elem.attrib['key']] = elem.attrib['value']
            elif elem.tag.endswith('int'):
                trace_data[elem.attrib['key']] = elem.attrib['value']
            elif elem.tag.endswith('event'):
                event_data = {}
                for sub_elem in elem:
                    if sub_elem.tag.endswith('string'):
                        event_data[sub_elem.attrib['key']] = sub_elem.attrib['value']
                    elif sub_elem.tag.endswith('date'):
                        event_data[sub_elem.attrib['key']] = sub_elem.attrib['value']
                    elif sub_elem.tag.endswith('int'):
                        event_data[sub_elem.attrib['key']] = sub_elem.attrib['value']
                trace_data.setdefault('events', []).append(event_data)
        traces.append(trace_data)
    return traces

def write_file_csv(traces, output_file):
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Write header
        header = ['concept:name', 'german speaking', 'yearsOfEducation', 'age', 'gender', 'citizen', 'protected', 'married', '@@case_index', 'activity', 'resource', 'time', '@@index']
        writer.writerow(header)
        # Write data
        for trace in traces:
            for event in trace['events']:
                row = [
                    trace.get('concept:name', ''),
                    trace.get('german speaking', ''),
                    trace.get('yearsOfEducation', ''),
                    trace.get('age', ''),
                    trace.get('gender', ''),
                    trace.get('citizen', ''),
                    trace.get('protected', ''),
                    trace.get('married', ''),
                    trace.get('@@case_index', ''),
                    event.get('activity', ''),
                    event.get('resource', ''),
                    event.get('time', ''),
                    event.get('@@index', '')
                ]
                writer.writerow(row)

def convert_file_xes_to_csv(input_file, output_file):
    traces = parse_file_xes(input_file)
    write_file_csv(traces, output_file)

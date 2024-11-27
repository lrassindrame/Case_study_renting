import os
from utils.convert import convert_file_xes_to_csv

def convert_all_xes_files(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for filename in os.listdir(input_dir):
        if filename.endswith('.xes'):
            input_file = os.path.join(input_dir, filename)
            
            output_file = os.path.join(output_dir, f"{os.path.splitext(filename)[0]}.csv")
            
            print(f"Conversion du fichier : {input_file} vers {output_file}")
            convert_file_xes_to_csv(input_file, output_file)
            print(f"Fichier converti : {output_file}")

input_directory = './datasets'
output_directory = './datasets_csv'

convert_all_xes_files(input_directory, output_directory)

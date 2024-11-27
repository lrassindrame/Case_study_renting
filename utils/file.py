import os

def get_file_paths(input_directory, extension=".csv"):
    file_paths = []
    
    for filename in os.listdir(input_directory):
        if filename.endswith(extension):
            file_path = os.path.join(input_directory, filename)
            file_paths.append(file_path)
    
    return file_paths
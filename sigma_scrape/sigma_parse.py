import yaml
import csv
import glob
import os
import random

def get_random_files(directory_path, number_of_files=10):
    # Get the absolute path of the directory to ensure output is in absolute form
    abs_directory_path = os.path.abspath(directory_path)

    # List all files in the directory
    all_files = [os.path.join(abs_directory_path, f) for f in os.listdir(abs_directory_path) if
                 os.path.isfile(os.path.join(abs_directory_path, f))]

    # Select count random files (or all if there are fewer than count)
    random_files = random.sample(all_files, min(len(all_files), number_of_files))

    return random_files

###############fdfsafdsaffdsafdsafds

def yaml_directory_to_csv(directory_path):
    # Define the CSV headers, adjust based on your needs
    headers = set()
    all_data = []

    # Find all YAML files in the specified directory
    # yaml_files = glob.glob(os.path.join(directory_path, '*.yaml'))

    # for testing only
    yaml_files = get_random_files(directory_path)

    # Process each YAML file
    for yaml_file in yaml_files:
        with open(yaml_file, 'r', encoding='utf-8') as file:
            # Parse the YAML content
            data = yaml.safe_load(file)
            # Update headers dynamically based on all keys encountered
            headers.update(data.keys())
            all_data.append(data)

    return all_data
    # Write to CSV


# Example usage

for i in yaml_directory_to_csv('all_yaml'):
    print(i['detection'])



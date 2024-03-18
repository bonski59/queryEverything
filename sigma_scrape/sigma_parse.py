import yaml
import csv
import glob
import os
import random
from collections import OrderedDict

def get_random_files(directory_path, number_of_files=50):
    # Get the absolute path of the directory to ensure output is in absolute form
    abs_directory_path = os.path.abspath(directory_path)

    # List all files in the directory
    all_files = [os.path.join(abs_directory_path, f) for f in os.listdir(abs_directory_path) if
                 os.path.isfile(os.path.join(abs_directory_path, f))]

    # Select count random files (or all if there are fewer than count)
    random_files = random.sample(all_files, min(len(all_files), number_of_files))

    return random_files


def get_all_files(directory_path):
    # Get the absolute path of the directory to ensure output is in absolute form
    abs_directory_path = os.path.abspath(directory_path)

    # List all files in the directory
    all_files = [os.path.join(abs_directory_path, f) for f in os.listdir(abs_directory_path) if
                 os.path.isfile(os.path.join(abs_directory_path, f))]

    return all_files


def yaml_file_to_dict(yaml_file):
    # Define the CSV headers, adjust based on your needs

    with open(yaml_file, 'r', encoding='utf-8') as file:
        # Parse the YAML content

        data = list(yaml.safe_load_all(file))[0]

        # Update headers dynamically based on all keys encountered

        for i in ['category', 'product', 'service']:
            try:
                data.update({i: data['logsource'][i]})
            except KeyError:
                data.update({i: 'N/A'})

        data.update({'filepath': os.path.basename(yaml_file)})

        # Headers (keys) we want to keep
        desired_keys = {'id', 'title', 'description', 'references', 'tags', 'author', 'status', 'logsource', 'category',
                        'product', 'service', 'detection', 'falsepositives', 'level', 'category', 'product', 'service',
                        'filepath'}

        # Filtering the dictionary to only include desired keys
        filtered_dict = {k: data[k] for k in desired_keys if k in data}

        # fill empty values
        for i in desired_keys:
            try:
                filtered_dict[i]
            except KeyError:
                filtered_dict[i] = 'N/A'

        ordered_dict = OrderedDict((k, filtered_dict[k]) for k in list(desired_keys))

    return ordered_dict
    # Write to CSV


# Example usage

# csv fields needed -- 'title', 'description', 'references', 'tags', 'author', 'status', 'logsource', 'category', 'product', 'service', 'detection', 'falsepositives', 'level'
# 'category', 'product', 'service' need to be parsed from 'logsource'


def save_to_csv(data, filename="splunk_research_output.csv"):
    # print(data)
    keys = data.keys()
    file_exists = os.path.isfile(filename)
    with open(filename, 'a', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)

        if not file_exists:  # Only write the header if the file doesn't exist
            dict_writer.writeheader()

        dict_writer.writerow(data)
    print(f"{data.get('title')} retrieved and written")



if __name__ == "__main__":
    for i in get_all_files('all_yaml'):
        #save_to_csv(yaml_file_to_dict(i))
        save_to_csv(yaml_file_to_dict(i))

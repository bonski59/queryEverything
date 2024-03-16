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

            for i in ['category', 'product', 'service']:
                try:
                    data.update({i: data['logsource'][i]})
                except KeyError:
                    data.update({i: 'N/A'})

            data.update({'filepath': os.path.basename(yaml_file)})

            key = data.keys()

            headers.update(key)

            all_data.append(data)


            #print(all_data)



            #print(filtered_dict)

    return all_data
    # Write to CSV


# Example usage

# csv fields needed -- 'title', 'description', 'references', 'tags', 'author', 'status', 'logsource', 'category', 'product', 'service', 'detection', 'falsepositives', 'level'
# 'category', 'product', 'service' need to be parsed from 'logsource'


def save_to_csv(data, filename="splunk_research_output.csv"):
    print(data)
    keys = data.keys()
    file_exists = os.path.isfile(filename)
    with open(filename, 'a', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)

        if not file_exists:  # Only write the header if the file doesn't exist
            dict_writer.writeheader()

        dict_writer.writerow(data)
    print(f"{data.get('title')} retrieved and written")



result = yaml_directory_to_csv('all_yaml')


for i in result:
    print(type(i))



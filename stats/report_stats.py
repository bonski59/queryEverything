import pandas as pd
import ast

def read_make_df(csv):
    # Reading the CSV file into a DataFrame
    return pd.read_csv(csv)

def aggregate_tags(raw_df, tag_column, file_name):
    # Use ast.literal_eval to convert string to list and combine all tags into a single list
    all_tags = [ast.literal_eval(tag_string) for tag_string in raw_df[tag_column].tolist()]
    all_tags_flat = sum(all_tags, [])

    # Remove duplicates by converting the list to a set, then back to a list
    unique_tags = list(set(all_tags_flat))
    with open(file_name, 'w') as file:
        for tag in unique_tags:
            file.write(tag + '\n')

    return unique_tags


# aggregate_tags(read_make_df('splunk_mission_queries.csv'), 'mitre_attack_codes', 'splunk_covered_tcodes.txt') # 83 unique tcodes
# aggregate_tags(read_make_df('elastic_mission_queries.csv'), 'mitre_technique', 'elastic_covered_tcodes.txt') # 66 unique tcodes



def compile_unique_tcodes(file1, file2):
    # Step 1: Read genres from each text file
    with open(file1, 'r') as file:
        tcodes1 = file.read().splitlines()

    with open(file2, 'r') as file:
        tcodes2 = file.read().splitlines()

    # Step 2: Find unique genres
    # Method 1: Unique genres that are only in file 1 or file 2, but not in both
    unique_tcodes = set(tcodes1) ^ set(tcodes2)  # Symmetric difference

    # OR

    # Method 2: Unique genres combining both files but removing duplicates
    # unique_tcodes = set(tcodes1).union(set(tcodes2)) - set(tcodes1).intersection(set(tcodes2))

    # Convert the set to a sorted list (optional, if you want the output to be sorted)
    unique_tcodes = sorted(list(unique_tcodes))

    # Step 3: Write unique genres to a new text file
    with open('ouput/unique_tcodes.txt', 'w') as output_file:
        for genre in unique_tcodes:
            output_file.write(genre + '\n')


csv_brf = '../brf/brf_data.csv'
def write_list(file_name, read_codes, column):
    brf_codes = [code for code in pd.read_csv(read_codes)[column]]
    with open(file_name, 'w') as file:
        for tag in brf_codes:
            file.write(tag + '\n')


def sort_unique_txt(file):
    with open(file, 'r') as f:
        tcodes = f.read().splitlines()

    unique_tcodes = set(sorted(list(tcodes)))

    with open(file, 'w') as output_file:
        for code in unique_tcodes:
            output_file.write(code + '\n')

# sort_unique_txt('All_Tcodes_final.txt')

# write_list('brf_tcode_aggregate.txt', csv_brf, 'Technique')

# compile_unique_tcodes('unique_tcodes.txt', 'brf_tcode_aggregate.txt')
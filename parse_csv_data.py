import pandas as pd
import ast
# Replace 'your_file_path.csv' with the path to your actual CSV file
csv_splunk = '/home/assessor/PycharmProjects/queryEverything/queryEverything/splunk_scrape/splunk_research_output.csv'

csv_elastic = '/home/assessor/PycharmProjects/queryEverything/queryEverything/elastic_scrape/elastic_research_output.csv'

txt_tcodes = "/home/assessor/PycharmProjects/queryEverything/queryEverything/All_Tcodes_final.txt"

notmatch_tags = "/home/assessor/PycharmProjects/queryEverything/queryEverything/notmatch_tags.txt"

# elastic headers ---- url,title,mitre_tactic_name,mitre_tactic,mitre_technique_name,mitre_technique,description,type,elastic_query,rule_indices,references,tags
# splunk headers ---- url,title,mitre_attack_codes,description,type,last_update,splunk_query,required_macros,required_fields,false_positives,associated_analytics,analytic_stories,references,tags,category

def read_make_df(csv):
    # Reading the CSV file into a DataFrame
    return pd.read_csv(csv)


def read_req_items(text_file):
    with open(text_file, "r") as file:
        read = set(file.read().splitlines())
    return read


def matches_text_file(row, text_file):
    try:
        row_data = ast.literal_eval(row)  # Safely evaluate the string as a Python literal (list)
        return any(line in text_file for line in row_data)  # Check if any string matches
    except ValueError:
        return False  # In case of evaluation error, assume no match

def notmatch_text_file(row, text_file):
    try:
        row_data = ast.literal_eval(row)  # Safely evaluate the string as a Python literal (list)
        return not any(line in text_file for line in row_data)  # Check if any string matches
    except ValueError:
        return False  # In case of evaluation error, assume no match



def filter_df(frame, read_items, filter_column, out_or_in):
    if out_or_in == "in":
        return frame[frame[filter_column].apply(lambda x: matches_text_file(x, read_items))]
    if out_or_in == "out":
        return frame[frame[filter_column].apply(lambda x: notmatch_text_file(x, read_items))]
    else:
        return "Wrong Syntax"

# print(filter_df(read_make_df(csv_elastic), read_req_items(txt_tcodes), 'mitre_technique'))





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

# aggregate_tags(read_make_df(csv_elastic), 'tags', 'elastic_tags_aggregate.txt')
# aggregate_tags(read_make_df(csv_splunk), 'tags', 'splunk_tags_aggregate.txt')


def filter_elastic():

    filter_by_tcode = filter_df(read_make_df(csv_elastic), read_req_items(txt_tcodes), 'mitre_technique', "in")

    filter_out_tags = filter_df(filter_by_tcode, read_req_items(notmatch_tags), 'tags', "out")

    return filter_out_tags

#elastic_filtered = filter_elastic()
#elastic_filtered.to_csv('elastic_mission_queries.csv', index=False)

def filter_splunk():

    filter_by_tcode = filter_df(read_make_df(csv_splunk), read_req_items(txt_tcodes), 'mitre_attack_codes', "in")

    filter_out_tags = filter_df(filter_by_tcode, read_req_items(notmatch_tags), 'tags', "out")

    return filter_out_tags


def filter_titles(df):
    with open(notmatch_tags, 'r') as notmatch:
        words_to_exclude = notmatch.read().splitlines()

    # Convert the words to exclude to lowercase for case-insensitive comparison
    words_to_exclude = [word.lower() for word in words_to_exclude]

    # Filter function to check if title contains any exclude words
    def title_contains_excluded_words(title, exclude_words):
        return any(exclude_word in title.lower() for exclude_word in exclude_words)

    # Apply filter function to DataFrame
    filtered_df = df[~df['title'].apply(title_contains_excluded_words, args=(words_to_exclude,))]

    return filtered_df


df = filter_titles(filter_splunk())
#print(df[df['title'].str.contains(r'\blinux\b', case=False, regex=True)])
df[df['type'] == '[\'Hunting\']'].to_csv('splunk_mission_queries.csv', index=False)
# splunk_filtered = filter_splunk()
# splunk_filtered.to_csv('splunk_mission_data-14MAR24.csv', index=False)







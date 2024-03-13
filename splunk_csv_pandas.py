import pandas as pd
import ast
# Replace 'your_file_path.csv' with the path to your actual CSV file
csv_file_path = 'splunk_research_output.csv'

# Reading the CSV file into a DataFrame
df = pd.read_csv(csv_file_path)

print(df)

with open('All_Tcodes_final.txt', "r") as file:
    tcodes = set(file.read().splitlines())

def matches_tcode(row, tcodes_set):
    try:
        row_tcodes = ast.literal_eval(row)  # Safely evaluate the string as a Python literal (list)
        return any(tcode in tcodes_set for tcode in row_tcodes)  # Check if any TCode matches
    except ValueError:
        return False  # In case of evaluation error, assume no match


filtered_df = df[df['mitre_attack_codes'].apply(lambda x: matches_tcode(x, tcodes))]

print(filtered_df['title'])
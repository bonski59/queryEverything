import pandas as pd

"""df = pd.read_csv('sigma_research_output.csv')

#print(df['tags'])

with open('tags.txt', 'w') as f:
    for title in df['title']:
        f.write(str(title))"""


def create_unique_word_bank(input_file_path, output_file_path):
    # Read words from the input file
    with open(input_file_path, 'r') as file:
        words = file.readlines()

    # Remove newline characters and duplicates
    # Strip removes leading/trailing whitespace including newlines, set removes duplicates
    unique_words = set(word.strip() for word in words)

    # Write the unique words to the output file
    with open(output_file_path, 'w') as file:
        for word in sorted(unique_words):
            file.write(word + '\n')

    print(f'Unique word bank has been created at {output_file_path}.')


# Example usage

create_unique_word_bank('tags.txt', 'unique_tags')

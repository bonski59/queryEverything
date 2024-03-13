# Path to your text file
file_path = 'detections_repo_links.txt'

# Read the file and remove duplicates
with open(file_path, 'r') as file:
    unique_lines = set(file.readlines())

# Optionally, you might want to sort the unique lines for better readability or for any other purpose
sorted_unique_lines = sorted(unique_lines)

# Write the unique lines back to a file (or another file if you wish)
output_file_path = 'detections_repo_links.txt'
with open(output_file_path, 'w') as output_file:
    output_file.writelines(sorted_unique_lines)
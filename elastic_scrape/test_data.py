import random


def read_random_lines(filename, num_lines=10):
    lines = []
    with open(filename, 'r') as file:
        # Read all lines in the file to get the total count
        all_lines = file.readlines()

    # Get the total number of lines in the file
    total_lines = len(all_lines)

    # Ensure the file has at least as many lines as we want to read
    if total_lines < num_lines:
        print(f"File only has {total_lines} lines, which is less than {num_lines}. Returning all lines.")
        return all_lines

    # Generate a list of num_lines random unique line numbers
    random_line_numbers = random.sample(range(total_lines), num_lines)

    # Extract the corresponding lines
    for line_number in random_line_numbers:
        lines.append(all_lines[line_number].strip())

    return lines


#print(read_random_lines('detections_repo_links.txt'))
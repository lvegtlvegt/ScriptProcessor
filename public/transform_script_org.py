import re

# Function to transform dialogue
def transform_dialogue(dialogue):
    # Remove all apostrophes
    dialogue = dialogue.replace("'", "")
    # Use regex to replace each word with its first letter, preserving punctuation
    return re.sub(r"(\b\w)\w*", r"\1", dialogue)

# Function to process the script
def process_script(input_file, output_file):
    with open(input_file, 'r') as file:
        lines = file.readlines()

    transformed_lines = []
    for line in lines:
        # Check if the line is a dialogue line
        if re.match(r'^([A-Z]+\s?[A-Z]*)\.', line):
            # Split the line into character name and dialogue
            character, dialogue = line.split('.', 1)
            # Transform the dialogue
            transformed_dialogue = transform_dialogue(dialogue)
            # Append the transformed line
            transformed_lines.append(f'{character}.{transformed_dialogue}')
        else:
            # Append non-dialogue lines unchanged
            transformed_lines.append(line)

    with open(output_file, 'w') as file:
        file.writelines(transformed_lines)

# Define input and output files
input_file = 'Little women script cloze.txt'
output_file = 'Little women script transformed.txt'

# Process the script
process_script(input_file, output_file)

import re

def transform_dialogue(text):
    # First pass: collect all character names
    character_names = set()
    for line in text.split('\n'):
        if match := re.match(r'^([A-Z][A-Z\s\.]+)\.', line):
            name = match.group(1).strip()
            character_names.add(name)
            # Also add without periods
            character_names.add(name.replace('.', ''))

    # Function to process a single word while preserving capitalization
    def process_word(word, is_first_word=False):
        # Skip if the word is empty or just punctuation
        if not word or not any(c.isalpha() for c in word):
            return word

        # DEBUG CODE
        if is_first_word and (word.startswith('ACT')):
            print ("I FOUMND THE WORD")

        # Preserve 'Scene' if it's the first word
        if is_first_word and (word.startswith('Scene') or word.startswith('ACT')):
            return word
            
        # Preserve character names
        if word in character_names:
            return word
            
        # Find the first letter and preserve its case
        first_letter = next((c for c in word if c.isalpha()), '')
        if not first_letter:
            return word
            
        # Preserve any leading or trailing punctuation
        prefix = ''
        suffix = ''
        
        while word and not word[0].isalpha():
            prefix += word[0]
            word = word[1:]
            
        while word and not word[-1].isalpha():
            suffix = word[-1] + suffix
            word = word[:-1]
            
        return prefix + first_letter + suffix

    # Split the text into lines
    lines = text.split('\n')
    transformed_lines = []
    
    for line in lines:
        # Skip empty lines
        if not line.strip():
            transformed_lines.append(line)
            continue
            
        # Check if line starts with a character name or scene heading
        match = re.match(r'^([A-Z][A-Z\s\.]+\.|\[.*\]|Scene\s+\d+)', line)
        if match:
            # If it's a character name or scene heading, preserve it
            name_part = match.group(0)
            rest_of_line = line[len(name_part):]
            
            # Only transform the dialogue part
            if rest_of_line:
                words = rest_of_line.split()
                transformed_words = [process_word(word) for word in words]
                transformed_lines.append(name_part + ' ' + ' '.join(transformed_words))
            else:
                transformed_lines.append(line)
        else:
            # For continuation lines of dialogue
            words = line.split()
            transformed_words = [process_word(word) for word in words]
            transformed_lines.append(' '.join(transformed_words))
    
    return '\n'.join(transformed_lines)

def process_script_file(input_path, output_path):
    try:
        # Read input file
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Transform the content
        transformed_content = transform_dialogue(content)
        
        # Write to output file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(transformed_content)
            
        print(f"Successfully processed script from {input_path} to {output_path}")
        
    except Exception as e:
        print(f"Error processing script: {str(e)}")

if __name__ == "__main__":
    import sys
    
    #if len(sys.argv) != 3:
    #    print("Usage: python transform_script.py input_script.txt output_script.txt")
    #    sys.exit(1)
        
    #input_file = sys.argv[1]
    #input_file = 'Little women script cloze.txt'
    input_file = 'ACT.txt'
    #output_file = sys.argv[2]
    output_file = 'Little women script transformed cloze.txt'
    process_script_file(input_file, output_file)

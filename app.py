from difflib import SequenceMatcher
from docx import Document
import csv

def load_file_text(file_name):
    if file_name.lower().endswith(".txt"):
        with open(file_name, "r", encoding="utf8") as file:
            return file.readlines()
    elif file_name.lower().endswith(".docx"):
        document = Document(file_name)
        return [paragraph.text for paragraph in document.paragraphs]
        
    print("Unsupported file type. Please use a .txt or .docx file for now")
    return None

# Cleans the data before storage
def clean_term(term):
    #removes extra spaces
    term = term.strip()

    #removes leading articles
    lower_term = term.lower()

    if lower_term.startswith("a "):
        term = term[2:] 
    elif lower_term.startswith("an "):
        term = term[3:] 
    elif lower_term.startswith("the "):
        term = term[4:]
    return term.strip( )


def normalize_term(term):
    return term.strip().lower()

  
# Validates data before storage
def is_valid_card(term, definition):
    # Remove extra spaces before checking
    term = term.strip()
    definition = definition.strip()

    # Skips empty terms or definitions
    if not term or not definition:
        return False
    
    # Skips terms & definitions that are too short to be useful
    if len(term) < 2:
        return False
    
    if len(definition) < 2:
        return False
    
    # Skips weak or invalid terms
    invalid_terms = {"a", "an", "the", "what", "this", "is"}

    if term.lower() in invalid_terms:
        return False
    
    return True

def is_question_line(line):
    return line.strip().endswith("?")

def add_qa_card(question, answer):
    card = {
        "front": question.strip(),
        "back": clean_definition(answer)
    }
    cards.append(card)

def generate_question(term, style="define"):
    if style == "define":
        return f'Define the term "{term}".'
    
    elif style == "meaning":
        return f'What does "{term}" mean?'
    
    elif style == "concept":
        return f'Explain the concept of "{term}".'
    
    elif style == "describe":
        return f'Describe "{term}".'
    
    else:
        return f'Define the term "{term}".'
    
def generate_flashcards(file_name):
    global cards
    global seen_terms
    global duplicate_cards
    global skipped_duplicates

    cards.clear()
    seen_terms.clear()
    duplicate_cards.clear()
    skipped_duplicates = 0
    skipped_lines = []

    lines = load_file_text(file_name)

    if lines is None:
        return None
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # Skip empty lines
        if not line:
            i += 1
            continue

        # Q&A Parsing
        if is_question_line(line):
            j = i + 1

            # Skip blank lines between question and answer
            while j < len(lines) and not lines[j].strip():
                j += 1

            if j < len(lines):
                next_line = lines[j].strip()

                # Avoid pairing question with another question
                if not is_question_line(next_line):
                    add_qa_card(line, next_line)

                    # Skip both question and answer
                    i = j + 1 
                    continue 

        term, definition = parse_line(line)

        if not term or not definition:
            skipped_lines.append({
                "line": line,
                "reason": get_skip_reason(line)
            })
            i += 1
            continue

        add_card(term, definition)

        i += 1

    return {
        "cards": cards,
        "duplicates_skipped": skipped_duplicates,
        "important_duplicates": duplicate_cards,
        "skipped_lines": skipped_lines
    }

def parse_pattern_line(line, separator):
    term, definition = line.split(separator, 1)

    term = clean_term(term)
    definition = definition.strip()

    confidence = get_parse_confidence(term, definition)

    if confidence < 2:
        return None, None
    
    return term, definition

def parse_colon_line(line):
    term, definition = line.split(":", 1)

    if " is " in term:
        term, partial_definition = term.split(" is ", 1)
        definition = partial_definition + " " + definition
        definition = " ".join(definition.split())
    
    term = clean_term(term)
    definition = definition.strip()

    # Confidence check
    confidence = get_parse_confidence(term, definition)

    if confidence < 2:
        return None, None
    
    return term, definition

def parse_line(line):
    if ":" in line:
        return parse_colon_line(line)
    
    patterns = [
        " is ",
        " has ",
        " consists of ",
        " provides ",
        " determines ",
        " translates ",
        " stores ",
        " manages ",
        " uses ",
        " forwards ",
        " connects ",
        " refers to ",
        " represents ",
        " assumes ",
        " distributes ",
        " acts as ",
        " handles ",
        " runs ",
        " uniquely identifies ",
        " improves ",
        " repeats ",
        " attempts ",
        " adds ",
        " packages ",
        " involves ",
        " identifies ",
        " are inspired by ",
        " measures ",
        " occurs when ",
        " store ",
        " stores ",
        " use ",
    ]

    for pattern in patterns:
        if pattern in line: 
            return parse_pattern_line(line, pattern)
    
    return None, None

def add_card(term, definition):
    global skipped_duplicates

    if is_valid_card(term,definition):

        definition = clean_definition(definition)

        card = {
            "front": generate_question(term, question_style),
            "back": definition
        }

        term_key = normalize_term(term)

        if term_key not in seen_terms:
            seen_terms[term_key] = definition.lower()
            cards.append(card)
        else:
            if seen_terms[term_key] == definition.lower():
                skipped_duplicates += 1

            elif definitions_are_similar(seen_terms[term_key], definition):
                skipped_duplicates += 1
            else:
                duplicate_cards.append({
                    "term": term,
                    "original_definition": seen_terms[term_key],
                    "new_definition": definition
                })

def clean_definition(definition):
    
    # Removes repeated spaces
    definition = " ".join(definition.split())

    # Capitalizes first letter
    definition = definition[0].upper() + definition[1:]

    # Adds ending punctuation if missing
    if not definition.endswith((".", "!", "?")):
        definition += "."
    
    return definition

def get_parse_confidence(term, definition):
    score = 0 

    # Good signals
    if len(term.split()) <= 6:
        score += 1

    if len(definition) > len(term):
        score += 1

    # Bad Signals
    if "'" in term or '"' in term:
        score -= 1

    if term.endswith("."):
        score -= 1

    return score

def get_skip_reason(line):
    if line.endswith(":"):
        return "Empty definition"
    
    if line.startswith(":"):
        return "Missing term"
    
    if line.endswith("?"):
        return "Question format detected without answer"
    
    if len(line.split()) <= 4:
        return "Missing definition"
    
    return "Unsupported format"


def definitions_are_similar(def1, def2, threshold=0.8):
    similarity = SequenceMatcher(None, def1.lower(), def2.lower()).ratio()
    
    return similarity >= threshold

def save_flashcards_to_csv(cards, output_file="flashcards.csv"):
    with open(output_file, "w", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["front", "back"])
        writer.writeheader()
        writer.writerows(cards)

# List to store flashcards
cards = [] 

# Tracks terms already added
seen_terms = {}

# Stores possible important duplicates for review
duplicate_cards = []

# Counter for duplicates that were skipped
skipped_duplicates = 0 

# Controls how flashcard questions are worded
question_style = "define"

if __name__ == "__main__":

    # Loop forever until a valid file is provided
    while True:
        # Prompt user for file name and remove extra spaces
        file_name = input("Enter the file name and type (ex: notes.txt): ").strip()

        try:
            # Attempt to open the file
            results = generate_flashcards(file_name)

            if results is None:
                continue

            cards = results["cards"]

            print("\nFile loaded successfully!\n")
            break  # Exit loop once file is successfully processed

        except FileNotFoundError:
            # If file doesn't exist, prompt user again
            print("File not found. Try again.\n")

    # Prints flashcards from stored list
    print("\nAll Flashcards:\n")

    for card in cards:
        print(f"Front: {card['front']}")
        print(f"Back: {card['back']}\n")

    # Save flashcards to a CSV file
    save_flashcards_to_csv(cards)

    print("Flashcards saved to flashcards.csv")

    print(f"\nDuplicates skipped: {skipped_duplicates}")
    print(f"\nPossible important duplicates found: {len(duplicate_cards)}")
    print(f"\nSkipped lines: {len(results['skipped_lines'])}")

    for skipped in results["skipped_lines"]:
        print(f"Skipped: {skipped['line']}")
        print(f"Reason: {skipped['reason']}")

    for duplicate in duplicate_cards:
        print(f"\nTerm: {duplicate['term']}")
        print(f"Original definition: {duplicate['original_definition']}")
        print(f"New definition: {duplicate['new_definition']}")
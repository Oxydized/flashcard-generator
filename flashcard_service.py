from file_loader import load_file_text
from cleaner import normalize_term, clean_definition, is_valid_card
from parser import is_question_line, parse_line, get_skip_reason
from duplicate_checker import definitions_are_similar

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
    

def add_qa_card(question, answer):
    card = {
        "front": question.strip(),
        "back": clean_definition(answer)
    }
    cards.append(card)


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
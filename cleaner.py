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

def clean_definition(definition):
    
    # Removes repeated spaces
    definition = " ".join(definition.split())

    # Capitalizes first letter
    definition = definition[0].upper() + definition[1:]

    # Adds ending punctuation if missing
    if not definition.endswith((".", "!", "?")):
        definition += "."
    
    return definition

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
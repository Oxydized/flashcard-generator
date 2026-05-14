from cleaner import clean_term

def is_question_line(line):
    return line.strip().endswith("?")

def parse_pattern_line(line, separator):
    term, definition = line.split(separator, 1)
    definition = separator.strip() + " " + definition

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

def get_parse_confidence(term, definition):
    score = 0 

    # Good signals
    if len(term.split()) <= 6:
        score += 1

    if len(definition.split()) > len(term.split()):
        score += 1

    # Bad Signals
    if "'" in term or '"' in term:
        score -= 1

    if term.endswith("."):
        score -= 1

    if any(char.isdigit() for char in definition):
        score += 1

    if len(definition.split()) >= 2:
        score += 1

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
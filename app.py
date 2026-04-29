import csv

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

# List to store flashcards
cards = [] 

# Loop forever until a valid file is provided
while True:
    # Prompt user for file name and remove extra spaces
    file_name = input("Enter the file name (ex: notes.txt): ").strip()

    try:
        # Attempt to open the file
        with open(file_name, 'r', encoding='utf8') as file:
            print("\nFile loaded successfully!\n")

            # Loop through each line in the file
            for line in file:
                line = line.strip()  # Remove whitespace/newline

                # Check if the line contains a colon (Term: definition format)
                if ":" in line:
                    # Split into term and definition (only split on first colon)
                    term, definition = line.split(":", 1)

                    term = clean_term(term)
                    definition = definition.strip()

                    if is_valid_card(term,definition):    
                        # Create a dictionary for each card
                        card = {
                            "front": f"What is {term}?",
                            "back": definition.strip()
                        }
                        cards.append(card) # add flashcards to list

                elif " is " in line:
                    term, definition = line.split(" is ", 1)
                    
                    term = clean_term(term)
                    definition = definition.strip()
                    
                    if is_valid_card(term, definition):
                        card = {
                            "front": f"What is {term}?",
                            "back": definition.strip()
                        }
                        cards.append(card) # add flashcards to list

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
with open("flashcards.csv", "w", newline="") as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=["front", "back"])
    writer.writeheader()
    writer.writerows(cards)

print("Flashcards saved to flashcards.csv")
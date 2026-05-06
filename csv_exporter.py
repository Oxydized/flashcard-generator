import csv

def save_flashcards_to_csv(cards, output_file="flashcards.csv"):
    with open(output_file, "w", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["front", "back"])
        writer.writeheader()
        writer.writerows(cards)
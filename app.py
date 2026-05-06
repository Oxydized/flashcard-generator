from flashcard_service import generate_flashcards
from csv_exporter import save_flashcards_to_csv

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

    print(f"\nDuplicates skipped: {results['duplicates_skipped']}")
    print(f"\nPossible important duplicates found: {len(results['important_duplicates'])}")
    print(f"\nSkipped lines: {len(results['skipped_lines'])}")

    for skipped in results["skipped_lines"]:
        print(f"Skipped: {skipped['line']}")
        print(f"Reason: {skipped['reason']}")

    for duplicate in results["important_duplicates"]:
        print(f"\nTerm: {duplicate['term']}")
        print(f"Original definition: {duplicate['original_definition']}")
        print(f"New definition: {duplicate['new_definition']}")
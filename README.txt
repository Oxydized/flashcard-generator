This project started as a way to practice backend parsing and gradually evolved into a full interactive study application.

# Flashcard Generator

An interactive flashcard generation and study application built with Python and Streamlit.

This project allows users to upload `.txt` or `.docx` notes and automatically generate study flashcards through rule-based parsing and validation.

---

# Features

## Flashcard Generation

- Upload `.txt` and `.docx` files
- Automatically parse notes into flashcards
- Supports multiple input formats
- Cleans and validates generated cards
- Detects duplicate and fuzzy duplicate flashcards
- Exports flashcards as downloadable CSV files

---

## Study Interface

- Interactive Streamlit web interface
- One-card-at-a-time study mode
- Previous / Next card navigation
- Show / Hide answer toggle
- Shuffle flashcards during study mode
- Reset flashcards back to original generated order
- Flashcard counter display
- Styled flashcard UI
- Optional flashcard table view

---

## Parser Transparency

- Tracks skipped/unparsed lines
- Displays skipped lines inside expandable UI section
- Displays skipped lines with reason classifications
- Helps users identify unsupported formatting
- Improves parser debugging and transparency
- Shows duplicate skip counts

---

# Supported Input Formats

The parser currently supports:

```text
Term: definition
```

```text
Term has definition
Term consists of definition
Term provides definition
Term determines definition
Term translates definition
Term stores definition
```

Example:

```text
Firewall: A device or software that filters network traffic based on security rules.
```

And:

```text
Term is definition
```

Example:

```text
A subnet is a smaller network created by dividing a larger network.
```

---

# Technologies Used

- Python
- Streamlit
- Pandas
- python-docx
- difflib

---

# Project Structure

```text
flashcard-generator/
├── app.py
├── streamlit_app.py
├── requirements.txt
├── README.md
└── sample_notes.txt
```

---

# How to Install

Clone the repository:

```bash
git clone <repository-url>
```

Navigate into the project folder:

```bash
cd flashcard-generator
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

---

# How to Run

Start the Streamlit application:

```bash
python -m streamlit run streamlit_app.py
```

The application will automatically open in your browser.

---

# Example Input

```text
Firewall: A device or software that filters network traffic based on security rules.

A subnet is a smaller network created by dividing a larger network.

Encryption: The process of converting data into a secure format.
```

---

# Current Capabilities

## Backend

- Modular parser architecture
- Reusable flashcard generation functions
- Reusable pattern-based parser helper
- Expanded sentence pattern support
- Skipped-line reason classification
- Input validation
- Duplicate detection
- Fuzzy duplicate comparison
- CSV export support
- Skipped-line tracking

---

## Frontend

- Interactive Streamlit UI
- Shuffle and reset study controls
- Duplicate skip count display
- Skipped-line reason display
- Session state management
- Flashcard navigation
- Responsive layout using Streamlit columns
- Styled HTML/CSS flashcards
- CSV downloads
- Expandable skipped-line viewer

---

# Future Improvements

## Parser Enhancements

- Question/answer pair parsing
- Multi-file upload support
- Parser precision tuning
- Better parser confidence scoring
- Improved natural-language parsing

---

## Study Features

- Reverse flashcards
- Fill-in-the-blank flashcards
- Multiple-choice study mode
- Spaced repetition
- Saved study decks

---

## File Support

- PDF support
- OCR/image support
- Better DOCX formatting support

---

## UI Improvements

- Flashcard flip animations
- Dark/light theme support
- Progress tracking
- Study statistics

---

## AI Integration (Planned)

Future AI-assisted functionality may include:

- Automatic concept extraction
- Semantic flashcard generation
- Smarter duplicate detection
- Difficulty-based flashcards
- AI-generated quizzes
- Summarization of lecture notes into study decks

The current system intentionally uses deterministic rule-based parsing first to establish strong backend architecture and parser transparency before introducing AI-assisted enhancements.

---

# Purpose of This Project

This project was built to strengthen skills in:

- Python backend development
- Frontend UI development with Streamlit
- State management
- File processing
- Parser design
- Software architecture
- Debugging and validation systems
- Git/GitHub workflow
- Building user-focused study tools

---

# Author

William Warren
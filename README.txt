# Flashcard Generator

A modular flashcard generation application built with Python, Streamlit, and FastAPI.

This project allows users to upload `.txt`, `.docx`, or `.pdf` notes and automatically generate study flashcards using rule-based parsing, validation, duplicate detection, skipped-line reporting, and question-answer extraction.

The project originally started as a backend parsing exercise and gradually evolved into a reusable document-processing engine with both a Streamlit frontend and a FastAPI backend API.

---

## Key Technologies

Python • FastAPI • Streamlit • File Processing • REST APIs • Parser Design

---

# Features

## Flashcard Generation

- Upload `.txt`, `.docx`, and `.pdf` files
- Automatically parse notes into flashcards
- Supports multiple input formats
- Cleans and validates generated cards
- Detects duplicate and fuzzy duplicate flashcards
- Tracks skipped or unsupported lines with reason classifications
- Supports question-and-answer pair parsing
- Exports generated flashcards as CSV files

---

## Streamlit Study Interface

- Interactive browser-based study mode
- One-card-at-a-time flashcard review
- Previous / Next card navigation
- Show / Hide answer toggle
- Shuffle flashcards
- Reset cards back to original generated order
- Flashcard counter display
- Optional generated flashcard table view
- CSV download support
- Expandable skipped-line viewer

---

## FastAPI Backend

- API endpoint for file uploads
- Accepts `.txt`, `.docx`, and `.pdf` files
- Validates supported file types
- Processes uploaded files through a reusable flashcard generation engine
- Returns structured JSON responses
- Includes duplicate counts, skipped lines, and generated cards
- Uses temporary file handling for uploads
- Includes error handling for unsupported file types

---

# Supported File Types

```text
.txt
.docx
.pdf
```

---

# Supported Input Formats

The parser currently supports formats such as:

- Term: definition
- Term is definition
- Term has definition
- Term consists of definition
- Term provides definition
- Term determines definition
- Term translates definition
- Term stores definition
- Term manages definition
- Term uses definition
- Term forwards definition
- Term connects definition

Example: Firewall: A device or software that filters network traffic based on security rules.
Example: A subnet is a smaller network created by dividing a larger network.

---

# Question and Answer Support

The application also supports basic question-and-answer formatting:

Example: 

What port does HTTPS use?
Port 443 is commonly used for HTTPS traffic.

The parser automatically pairs supported questions with the next valid answer line.

---

# Technologies Used

- Python
- Streamlit
- FastAPI
- Pandas
- python-docx
- pypdf
- python-multipart
- Uvicorn
- difflib

---

# Project Structure

```text
flashcard-generator/
├── app.py
├── main.py
├── streamlit_app.py
├── flashcard_service.py
├── file_loader.py
├── parser.py
├── cleaner.py
├── duplicate_checker.py
├── csv_exporter.py
├── requirements.txt
├── README.md
└── sample notes files
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

Create and activate a virtual environment:

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

---

# How to Run the Streamlit App

Start the Streamlit application:

```bash
python -m streamlit run streamlit_app.py
```

The Streamlit app will automatically open in your browser.

## Users can:

- upload study notes
- generate flashcards
- review flashcards interactively
- shuffle and reset cards
- download generated CSV files

---

# How to Run the FastAPI Backend

- Start the FastAPI development server:

```bash
python -m uvicorn main:app --reload
```

Open the interactive API documentation:
http://127.0.0.1:8000/docs

---

# API Endpoint
POST /generate-flashcards

Accepts an uploaded .txt, .docx, or .pdf file and returns generated flashcards as JSON.

Example Response: 

{
  "success": true,
  "filename": "notes.txt",
  "total_cards": 10,
  "duplicates_skipped": 2,
  "important_duplicates": [],
  "skipped_lines": [],
  "cards": [
    {
      "front": "Define the term \"Firewall\".",
      "back": "A security device that filters network traffic."
    }
  ]
}

Unsupported file types return a structured API error response.

---

# Current Capabilities

## Backend 

- Modular parser architecture
- Reusable flashcard generation engine
- TXT, DOCX, and PDF file loading
- Pattern-based parsing
- Question-and-answer parsing
- Parser confidence scoring
- Input cleaning and validation
- Duplicate detection
- Fuzzy duplicate comparison
- Skipped-line reason classification
- Stateless backend refactor for safer API usage
- FastAPI upload endpoint
- API file validation and error handling
- Temporary file processing pipeline


## Frontend

- Interactive Streamlit UI
- File upload interface
- Flashcard study mode
- Shuffle and reset controls
- Duplicate skip count display
- Skipped-line reason display
- Session state management
- Flashcard navigation
- Styled HTML/CSS flashcards
- CSV downloads
- Expandable skipped-line viewer

---

# Future Improvements

## Parser Enhancements  

- Multi-file upload support
- Improved natural-language parsing
- Better parser confidence scoring
- More advanced Q&A pairing
- Better handling of messy classroom notes

## Study Features

- Reverse flashcards
- Fill-in-the-blank flashcards
- Multiple-choice study mode
- Spaced repetition
- Saved study decks
- Study statistics

## API Improvements

- Pydantic response models
- More detailed error responses
- Automated API testing
- Authentication support
- Frontend integration with React or Angular
- Optional database support for saved decks

## File Support

- OCR/image-based PDF support
- Better DOCX formatting support
- Support for multiple uploaded files

---

# AI Integration Planned

Future AI-assisted functionality may include:

- Automatic concept extraction
- Semantic flashcard generation
- Smarter duplicate detection
- Difficulty-based flashcards
- AI-generated quizzes
- Summarization of lecture notes into study decks

The current system intentionally uses deterministic rule-based parsing first 
to establish strong backend architecture and parser transparency before introducing AI-assisted enhancements.

---

# Purpose of This Project

This project was built to strengthen skills in:

- Python backend development
- API development with FastAPI
- Frontend UI development with Streamlit
- File processing
- Parser design
- State management
- Software architecture
- Debugging and validation systems
- Git/GitHub workflow
- Building user-focused study tools

--- 

# Author

William Warren
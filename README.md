# Flashcard Generator

A full-stack flashcard study platform built with FastAPI and Angular that converts unstructured notes into interactive study decks.

The application supports `.txt`, `.docx`, and `.pdf` uploads, processes notes through a modular parsing pipeline, and provides a modern study experience featuring deck previews, keyboard shortcuts, progress tracking, review workflows, and dark/light mode support.

The project originally began as a backend parsing exercise and evolved into a multi-page study application focused on educational UX, frontend architecture, and scalable backend processing.

---

## Key Technologies

Python • FastAPI • Angular • File Processing • REST APIs • Parser Design • TypeScript • HTML/CSS

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

## Screenshots

## Upload Page (Light Mode)

![Upload Page](https://github.com/Oxydized/flashcard-generator/blob/793846469a222c24baf724c0528eddc04e12fee2/Upload%20-%20Light%20Mode.png)

## Study Session (Light Mode)

![Study Session-Light](https://github.com/Oxydized/flashcard-generator/blob/793846469a222c24baf724c0528eddc04e12fee2/Study%20Session%20-%20Light%20Mode.png)

## Study Session (Dark Mode)

![Study Session-Dark](https://github.com/Oxydized/flashcard-generator/blob/793846469a222c24baf724c0528eddc04e12fee2/Study%20Session%20-%20Dark%20Mode.png)

---

## Angular Frontend Features
 
- Upload page
- Deck preview page
- Interactive study mode
- Keyboard shortcuts
- Knew It / Review workflow
- Dark/light themes
- Multi-page SPA routing
- Shared service-based state management

---

## Streamlit Study Interface (Legacy)

The original frontend prototype was built with Streamlit to rapidly validate:
- flashcard generation workflows
- parser behavior
- study interaction concepts

The project later evolved into a full Angular single-page application frontend.

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
- TypeScript
- HTML/CSS
- Angular
- Streamlit
- FastAPI
- Pandas
- python-docx
- pypdf
- python-multipart
- Uvicorn
- difflib

---

# Project Backend Structure

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

# Project Frontend Structure

```text
flashcard-frontend/
├── src/
│   ├── app/
│   │   ├── pages/
│   │   │   ├── upload/
│   │   │   ├── deck/
│   │   │   └── study/
│   │   ├── services/
│   │   └── app.routes.ts
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
- Persistent saved decks
- Dockerization
- AWS deployment
- Kubernetes orchestration
- Mobile responsiveness
- Spaced repetition
- AI-assisted study recommendations
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
- Frontend UI development with Angular and Streamlit
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
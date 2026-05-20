from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware
import tempfile
import os

from flashcard_service import generate_flashcards

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ALLOWED_EXTENSIONS = [".txt", ".docx", ".pdf"]


class Flashcard(BaseModel):
    term: Optional[str] = None
    front: str
    back: str


class ImportantDuplicate(BaseModel):
    term: str
    original_definition: str
    new_definition: str


class SkippedLine(BaseModel):
    line: str
    reason: str


class FlashcardResponse(BaseModel):
    success: bool
    filename: str
    total_cards: int
    duplicates_skipped: int
    important_duplicates: List[ImportantDuplicate]
    skipped_lines: List[SkippedLine]
    cards: List[Flashcard]


@app.get("/")
def root():
    return {"message": "Flashcard API running"}


@app.post("/generate-flashcards", response_model=FlashcardResponse)
async def generate_flashcards_from_file(files: List[UploadFile] = File(...)):
    all_cards = []
    all_important_duplicates = []
    all_skipped_lines = []
    total_duplicates_skipped = 0
    filenames = []

    for file in files:
        file_extension = os.path.splitext(file.filename)[1]

        if file_extension.lower() not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type: {file.filename}. Please upload a .txt, .docx, or .pdf file."
            )

        filenames.append(file.filename)

        with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_file:
            contents = await file.read()
            temp_file.write(contents)
            temp_file_path = temp_file.name

        try:
            results = generate_flashcards(temp_file_path)

            if results is None:
                raise HTTPException(
                    status_code=400,
                    detail=f"The file could not be processed: {file.filename}"
                )

            all_cards.extend(results["cards"])
            total_duplicates_skipped += results["duplicates_skipped"]
            all_important_duplicates.extend(results["important_duplicates"])
            all_skipped_lines.extend(results["skipped_lines"])

        finally:
            os.remove(temp_file_path)

    return {
        "success": True,
        "filename": ", ".join(filenames),
        "total_cards": len(all_cards),
        "duplicates_skipped": total_duplicates_skipped,
        "important_duplicates": all_important_duplicates,
        "skipped_lines": all_skipped_lines,
        "cards": all_cards
    }
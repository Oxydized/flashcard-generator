from fastapi import FastAPI, UploadFile, File, HTTPException
import tempfile
import os

from flashcard_service import generate_flashcards

app = FastAPI()
ALLOWED_EXTENSIONS = [".txt", ".docx", ".pdf"]

@app.get("/")
def root():
    return {"message": "Flashcard API running"}

@app.post("/generate-flashcards")
async def generate_flashcards_from_file(file: UploadFile = File(...)):
    # Get uploaded file extension, such as .txt, .docx, or .pdf
    file_extension = os.path.splitext(file.filename)[1]
    if file_extension.lower() not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type. Plase upload a .txt, .docx or .pdf file."
        )

    # Save uploaded file temporarily so existing backend can process it
    with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_file:
        contents = await file.read()
        temp_file.write(contents)
        temp_file_path = temp_file.name

    try:
        # Send temp file path into your existing flashcard generator
        results = generate_flashcards(temp_file_path)
        if results is None:
            raise HTTPException(
                status_code=400,
                detail="The file could not be processed."
            )
        
        return {
            "success": True,
            "filename": file.filename,
            "total_cards": len(results["cards"]),
            "duplicates_skipped": results["duplicates_skipped"],
            "important_duplicates": results["important_duplicates"],
            "skipped_lines": results["skipped_lines"],
            "cards": results["cards"]
        }

    finally:
        # Delete temp file after processing
        os.remove(temp_file_path)

     

from fastapi import FastAPI, UploadFile, File
import tempfile
import os

from flashcard_service import generate_flashcards

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Flashcard API running"}

@app.post("/generate-flashcards")
async def generate_flashcards_from_file(file: UploadFile = File(...)):
    # Get uploaded file extension, such as .txt, .docx, or .pdf
    file_extension = os.path.splitext(file.filename)[1]

    # Save uploaded file temporarily so existing backend can process it
    with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_file:
        contents = await file.read()
        temp_file.write(contents)
        temp_file_path = temp_file.name

    try:
        # Send temp file path into your existing flashcard generator
        results = generate_flashcards(temp_file_path)
        return results

    finally:
        # Delete temp file after processing
        os.remove(temp_file_path)

     

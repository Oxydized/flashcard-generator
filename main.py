from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class FlashcardRequest(BaseModel):
    text: str

@app.get("/")
def root():
    return {"message": "Flashcard API running"}

@app.post("/generate_flashcards")
def generate_flashcards_from_text(request: FlashcardRequest):
    return {
        "received_text": request.text
    }
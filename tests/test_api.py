from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Flashcard API running"
    }


def test_upload_txt_file():
    response = client.post(
        "/generate-flashcards",
        files={
            "file": (
                "notes.txt",
                b"Firewall: A security device"
            )
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True
    assert data["filename"] == "notes.txt"
    assert data["total_cards"] == 1
    assert data["duplicates_skipped"] == 0
    assert data["cards"][0]["front"] == 'Define the term "Firewall".'
    assert data["cards"][0]["back"] == "A security device."


def test_upload_unsupported_file_type():
    response = client.post(
        "/generate-flashcards",
        files={
            "file": (
                "image.png",
                b"fake image content"
            )
        }
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Unsupported file type. Please upload a .txt, .docx, or .pdf file."
    }


def test_upload_txt_with_skipped_line():
    response = client.post(
        "/generate-flashcards",
        files={
            "file": (
                "notes.txt",
                b"Firewall: A security device\nCIA Triad"
            )
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total_cards"] == 1
    assert len(data["skipped_lines"]) == 1
    assert data["skipped_lines"][0]["line"] == "CIA Triad"
    assert data["skipped_lines"][0]["reason"] == "Missing definition"
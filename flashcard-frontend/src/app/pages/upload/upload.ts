import { ChangeDetectorRef, Component } from "@angular/core";
import { CommonModule } from "@angular/common";
import { HttpClient } from "@angular/common/http";
import { FlashcardService } from "../../services/flashcard";
import { Router } from "@angular/router";
import { StudySessionService } from "../../services/study-session";
import { Title } from '@angular/platform-browser';

const API_URL = "https://flashcard-generator-api.onrender.com";

@Component({
  selector: "app-upload",
  standalone: true,
  templateUrl: "./upload.html",
  styleUrl: "./upload.css",
  imports: [CommonModule],
})
export class Upload {
  selectedFiles: File[] = [];
  flashcards: any[] = [];
  totalCards = 0;
  isLoading = false;

  constructor(
    private http: HttpClient,
    private cdr: ChangeDetectorRef,
    private flashcardService: FlashcardService,
    private router: Router,
    private studySessionService: StudySessionService,
    private titleService: Title

  ) {
    this.titleService.setTitle("Flashcard Generator | Upload");
  }

  onFileSelected(event: any) {
    this.selectedFiles = Array.from(event.target.files);
  }

  generateFlashcards() {
    console.log("Generate clicked");

    if (this.selectedFiles.length === 0) {
      alert("Please select at least one file first.");
      return;
    }

    console.log("Selected files:", this.selectedFiles);

    this.isLoading = true;
    this.flashcards = [];
    this.totalCards = 0;

    const formData = new FormData();

    this.selectedFiles.forEach((file) => {
      formData.append("files", file);
    });

    this.http.post(
      `${API_URL}/generate-flashcards`,
      formData
    ).subscribe({
      next: (response: any) => {
        console.log("API response:", response);

        const cards = response.cards ?? [];
        const total = response.total_cards ?? 0;

        this.flashcardService.setFlashcards(
          cards,
          total,
          response.duplicates_skipped ?? 0,
          response.skipped_lines ?? [],
          response.important_duplicates ?? []
        );
        
        this.studySessionService.clearSession();

        this.router.navigate(["/deck", "generated"]);

        this.isLoading = false;
        this.cdr.detectChanges();
      },
      error: (error) => {
        console.error("Upload failed:", error);
        this.isLoading = false;
        this.cdr.detectChanges();
      },
      complete: () => {
        console.log("Request complete");
      }
    });
  }
}
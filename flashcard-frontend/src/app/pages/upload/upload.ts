import { ChangeDetectorRef, Component } from "@angular/core";
import { CommonModule } from "@angular/common";
import { HttpClient } from "@angular/common/http";
import { FlashcardService } from '../../services/flashcard';
import { Router } from '@angular/router';

@Component({
  selector: "app-upload",
  standalone: true,
  templateUrl: "./upload.html",
  styleUrl: "./upload.css",
  imports: [CommonModule],
})
export class Upload {
  selectedFile: File | null = null;
  flashcards: any[] = [];
  totalCards = 0;
  isLoading = false;

  constructor(
    private http: HttpClient,
    private cdr: ChangeDetectorRef,
    private flashcardService: FlashcardService,
    private router: Router
  ) {}

  onFileSelected(event: any) {
    this.selectedFile = event.target.files[0];
  }

  generateFlashcards() {
    console.log("Generate clicked");

    if (!this.selectedFile) {
      alert("Please select a file first.");
      return;
    }

    console.log("Selected file:", this.selectedFile);

    this.isLoading = true;
    this.flashcards = [];
    this.totalCards = 0;

    const formData = new FormData();
    formData.append("file", this.selectedFile);

    this.http.post(
      "http://127.0.0.1:8000/generate-flashcards",
      formData
    ).subscribe({
      next: (response: any) => {
        console.log("API response:", response);
        
        const cards = response.cards ?? [];
        const total = response.total_cards ?? 0;

        // this.flashcards = response.cards ?? [];
        // this.totalCards = response.total_cards ?? 0;

        this.flashcardService.setFlashcards(cards, total)
        this.router.navigate(['/deck', 'generated'])

        this.isLoading = false;
        this.cdr.detectChanges();
      },
      error: (error) => {
        console.error("Upload failed:", error);
        this.isLoading = false;
        this.cdr.detectChanges();
      },
      complete: () => {
        console.log("Request complete"
        )
      }
    });
  }
}
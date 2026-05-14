import { ChangeDetectorRef, Component } from "@angular/core";
import { HttpClient } from "@angular/common/http";
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-root',
  standalone: true,
  templateUrl: './app.html',
  styleUrl: './app.css',
  imports: [CommonModule],
})

export class App {
  selectedFile: File | null = null;

  flashcards: any[] = [];
  totalCards = 0;
  isLoading = false;

  constructor(
    private http: HttpClient,
    private cdr: ChangeDetectorRef
  ) {}

  onFileSelected(event: any) {
    this.selectedFile = event.target.files[0];
  }

  generateFlashcards() {
    if (!this.selectedFile) {
      alert('Please select a file first.');
      return;
    }

    this.isLoading = true;
    this.flashcards = [];
    this.totalCards = 0;

    const formData = new FormData();
    formData.append('file', this.selectedFile);

    this.http.post(
      'http://127.0.0.1:8000/generate-flashcards',
      formData
    ).subscribe({
      next: (response: any) => {

        this.flashcards = response.cards ?? [];
        this.totalCards = response.total_cards ?? 0;
        this.isLoading = false;

        this.cdr.detectChanges();
      },
      error: (error) => {
        console.error('Upload failed:', error);
        this.isLoading = false;
        this.cdr.detectChanges();
      }
    });
  }
}
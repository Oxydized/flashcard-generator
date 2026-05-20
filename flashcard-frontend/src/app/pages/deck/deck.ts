import { Component } from "@angular/core";
import { CommonModule } from "@angular/common";
import { FlashcardService } from "../../services/flashcard";
import { Router } from "@angular/router";
import { Title } from '@angular/platform-browser';

@Component({
  selector: "app-deck",
  standalone: true,
  templateUrl: "./deck.html",
  styleUrl: "./deck.css",
  imports: [CommonModule],
})


export class Deck {
  flashcards: any[] = [];
  totalCards = 0;
  duplicatesSkipped = 0;
  skippedLines: any[] = [];
  importantDuplicates: any[] = [];
  showSkippedDetails = false;

  constructor(
    private flashcardService: FlashcardService,
    private router: Router,
    private titleService: Title
  ) {
    this.titleService.setTitle('Flashcard Generator | Deck Preview');
    this.duplicatesSkipped = this.flashcardService.getDuplicatesSkipped();
    this.skippedLines = this.flashcardService.getSkippedLines();
    this.importantDuplicates = this.flashcardService.getImportantDuplicates();
    this.flashcards = this.flashcardService.getFlashcards();
    this.totalCards = this.flashcardService.getTotalCards();
  }
  startStudy() {
  this.router.navigate(['/study', 'generated']);
  }
  previewLimit = 4;
  showAllCards = false;

  get visibleCards() {
    return this.showAllCards ? this.flashcards : this.flashcards.slice(0, this.previewLimit);
  }

  toggleShowAllCards() {
    this.showAllCards = !this.showAllCards;
  }

  toggleSkippedDetails() {
    this.showSkippedDetails = !this.showSkippedDetails;
  }

  returnToUpload() {
    this.router.navigate(["/upload"]);
  }
}


import { Component } from "@angular/core";
import { CommonModule } from "@angular/common";
import { FlashcardService } from "../../services/flashcard";
import { Router } from "@angular/router";

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

  constructor(
    private flashcardService: FlashcardService,
    private router: Router
  ) {
    this.flashcards = this.flashcardService.getFlashcards();
    this.totalCards = this.flashcardService.getTotalCards();
  }
  startStudy() {
  this.router.navigate(['/study', 'generated']);
  }
  previewLimit = 5;
  showAllCards = false;

  get visibleCards() {
    return this.showAllCards ? this.flashcards : this.flashcards.slice(0, this.previewLimit);
  }

  toggleShowAllCards() {
    this.showAllCards = !this.showAllCards;
  }
}


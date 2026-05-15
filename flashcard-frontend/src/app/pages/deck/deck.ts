import { Component } from "@angular/core";
import { CommonModule } from "@angular/common";
import { FlashcardService } from "../../services/flashcard";

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

  constructor(private flashcardService: FlashcardService) {
    this.flashcards = this.flashcardService.getFlashcards();
    this.totalCards = this.flashcardService.getTotalCards();
  }
}
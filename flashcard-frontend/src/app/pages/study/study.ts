import { Component } from "@angular/core";
import { CommonModule } from "@angular/common";
import { FlashcardService } from "../../services/flashcard";

@Component({
  selector: "app-study",
  standalone: true,
  templateUrl: "./study.html",
  styleUrl: "./study.css",
  imports: [CommonModule],
})
export class Study {
  flashcards: any[] = [];
  currentIndex = 0;
  showAnswer = false;

  constructor(private flashcardService: FlashcardService) {
    this.flashcards = this.flashcardService.getFlashcards();
  }

  get currentCard() {
    return this.flashcards[this.currentIndex];
  }

  toggleAnswer() {
    this.showAnswer = !this.showAnswer;
  }

  nextCard() {
    if (this.currentIndex < this.flashcards.length - 1) {
      this.currentIndex++;
      this.showAnswer = false;
    }
  }

  previousCard() {
    if (this.currentIndex > 0) {
      this.currentIndex--;
      this.showAnswer = false;
    }
  }
}
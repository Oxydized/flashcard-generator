import { Component, HostListener } from "@angular/core";
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
  knownCards: number[] = [];
  reviewCards: number[] = [];

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

  getQuestionPrefix(): string {
    if (!this.currentCard?.term) {
      return this.currentCard?.front || '';
    }

    return this.currentCard.front.split(
      `"${this.currentCard.term}"`
    )[0];
  }

  getQuestionSuffix(): string {
    if (!this.currentCard?.term) {
      return '';
    }

    return this.currentCard.front.split(
      `"${this.currentCard.term}"`
    )[1];
  }

    @HostListener('window:keydown', ['$event'])
      handleKeyboardEvent(event: KeyboardEvent) {

    // Prevent spacebar from scrolling page
    if (event.code === 'Space') {
      event.preventDefault();
    }

    // Show / Hide Answer
    if (event.code === 'Space') {
      this.toggleAnswer();
    }

    // Next Card
    if (event.code === 'ArrowRight') {
      this.nextCard();
    }

    // Previous Card
    if (event.code === 'ArrowLeft') {
      this.previousCard();
    }

    // Prevent arrow from scrolling page
    if (event.code === 'ArrowUp') {
      event.preventDefault();
    }

    // Mark Known
    if (event.code === 'ArrowUp') {
      this.markKnown();
    }

    // Prevent arrow from scrolling page
    if (event.code === 'ArrowDown') {
      event.preventDefault();
    }

    // Review Again
    if (event.code === 'ArrowDown') {
      this.markReviewAgain();
    }
  }
    markKnown() {

    if (!this.knownCards.includes(this.currentIndex)) {
      this.knownCards.push(this.currentIndex);
    }

    // Remove from review list if previously marked
    this.reviewCards = this.reviewCards.filter(
      index => index !== this.currentIndex
    );

    this.nextCard();
  }

  markReviewAgain() {

    if (!this.reviewCards.includes(this.currentIndex)) {
      this.reviewCards.push(this.currentIndex);
    }

    // Remove from known list if previously marked
    this.knownCards = this.knownCards.filter(
      index => index !== this.currentIndex
    );

    this.nextCard();
  }
}
import { Component, HostListener } from "@angular/core";
import { CommonModule } from "@angular/common";
import { FlashcardService } from "../../services/flashcard";
import { StudySessionService } from '../../services/study-session';
import { Router } from "@angular/router";
import { Title } from '@angular/platform-browser';

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
  sessionComplete = false;
  isWeakReviewMode = false;
  originalFlashcards: any[] = [];
    

  constructor(
    private flashcardService: FlashcardService,
    private studySessionService: StudySessionService,
    private router: Router,
    private titleService: Title

  ) {
    this.titleService.setTitle('Flashcard Generator | Study Session');

    const savedSession = this.studySessionService.loadSession();

    if (savedSession) {
    this.flashcards = savedSession.flashcards ?? [];
    this.originalFlashcards = savedSession.originalFlashcards ?? [];
    this.currentIndex = savedSession.currentIndex ?? 0;
    this.showAnswer = savedSession.showAnswer ?? false;
    this.sessionComplete = savedSession.sessionComplete ?? false;
    this.knownCards = savedSession.knownCards ?? [];
    this.reviewCards = savedSession.reviewCards ?? [];
    this.isWeakReviewMode = savedSession.isWeakReviewMode ?? false;

    this.titleService.setTitle(
    this.sessionComplete
      ? 'Flashcard Generator | Session Results'
      : 'Flashcard Generator | Study Session'
    );
    } else {
    this.flashcards = this.flashcardService.getFlashcards();
    this.originalFlashcards = [...this.flashcards];
    }
  } 

  get currentCard() {
    return this.flashcards[this.currentIndex];
  }

  toggleAnswer() {
    this.showAnswer = !this.showAnswer;
    this.saveSessionState();
  }

  nextCard() {
    if (this.currentIndex < this.flashcards.length - 1) {
      this.currentIndex++;
      this.showAnswer = false;
      this.saveSessionState();
    }
  }

  previousCard() {
    if (this.currentIndex > 0) {
      this.currentIndex--;
      this.showAnswer = false;
      this.saveSessionState();
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

    this.advanceAfterRating();
  }

  markReviewAgain() {
 
    if (!this.reviewCards.includes(this.currentIndex)) {
      this.reviewCards.push(this.currentIndex);
    }

    // Remove from known list if previously marked
    this.knownCards = this.knownCards.filter(
      index => index !== this.currentIndex
    );

    this.advanceAfterRating();
  }

  advanceAfterRating() {
    if (this.currentIndex < this.flashcards.length - 1) {
      this.nextCard();
    } else {
      this.sessionComplete = true;
      this.showAnswer = false;

      this.titleService.setTitle(
        'Flashcard Generator | Session Results'
      );
    }

    this.saveSessionState();
  }

  get reviewedCount(): number {
    return this.knownCards.length + this.reviewCards.length;
  }

  get completionPercent(): number {
    if (this.flashcards.length === 0) {
      return 0;
    }

    return Math.round((this.reviewedCount / this.flashcards.length) * 100);
  }

  restartSession() {
    this.currentIndex = 0;
    this.showAnswer = false;
    this.sessionComplete = false;
    this.knownCards = [];
    this.reviewCards = [];
    this.titleService.setTitle(
      this.isWeakReviewMode
        ? 'Flashcard Generator | Focused Review'
        : 'Flashcard Generator | Study Session'
    );

    this.saveSessionState();
  }

  get unratedCount(): number {
    return this.flashcards.length - this.reviewedCount;
  }

  get masteryPercent(): number {
    if (this.reviewedCount == 0) {
      return 0;
    }

    return Math.round((this.knownCards.length / this.reviewedCount) * 100);
  }

  get knownPercent(): number {
    if (this.flashcards.length == 0) {
      return 0;
    }
    return Math.round((this.knownCards.length / this.flashcards.length) * 100);
  }

  get reviewPercent(): number {
    if (this.flashcards.length == 0) {
      return 0;
    }
    return Math.round((this.reviewCards.length / this.flashcards.length) * 100);
  }

  get completionMessage(): string {
    if (this.reviewedCount === 0) {
      return `Session completed. ${this.getRatedMessage()}<br> 
      Rate cards during your next pass to get mastery insights.`;
    }

    const ratedPercent = this.reviewedCount / this.flashcards.length;

    if (ratedPercent < 0.25) {
      return `Session completed. ${this.getRatedMessage()}<br>
      Rate more cards next time for an accurate mastery summary.`;
    }

    if (this.masteryPercent >= 80) {
      return `${this.getRatedMessage()}<br>
      Great job - you marked most cards as understood.`
    }

    if (this.reviewCards.length > this.knownCards.length) {
      return `${this.getRatedMessage()}<br>
      You flagged several cards for review. Consider another pass.`
    }

    return `${this.getRatedMessage()}<br>
    Nice work - keep building consistency through repitition.`
  }

  getRatedMessage(): string {
    const total = this.flashcards.length;
    const rated = this.reviewedCount;

    if (rated === 0) {
      return `No cards were rated during this session.`;
    }

    if (rated === 1) {
      return `Only 1 out of ${total} cards was rated during this session.`;
    }

    return `${rated} out of ${total} cards were rated during this session.`;
  }

  getCardStatus(index: number): string[] {
    const classes = [];

    if (this.knownCards.includes(index)) {
      classes.push('known');
    }

    if (this.reviewCards.includes(index)) {
      classes.push('review');
    }

    if (index === this.currentIndex && !this.sessionComplete) {
      classes.push('current');
    }

    if (classes.length === 0) {
      classes.push('unrated');
    }

    return classes;
  }

  reviewWeakCards() {
    const sourceDeck = this.isWeakReviewMode
      ? this.flashcards
      : this.originalFlashcards;

    const reviewableCards = sourceDeck.filter((card, index) => {
      const wasMarkedReview = this.reviewCards.includes(index);
      const wasMarkedKnown = this.knownCards.includes(index);

      return wasMarkedReview || !wasMarkedKnown;
    });

    if (reviewableCards.length === 0) {
      return;
    }

    this.flashcards = reviewableCards;

    this.currentIndex = 0;
    this.showAnswer = false;
    this.sessionComplete = false;
    this.titleService.setTitle('Flashcard Generator | Focused Review');

    this.knownCards = [];
    this.reviewCards = [];

    this.isWeakReviewMode = true;

    this.saveSessionState();
  }

  studyFullDeck() {
    this.flashcards = [...this.originalFlashcards];

    this.currentIndex = 0;
    this.showAnswer = false;
    this.sessionComplete = false;

    this.knownCards = [];
    this.reviewCards = [];

    this.isWeakReviewMode = false;

    this.titleService.setTitle('Flashcard Generator | Study Session');

    this.saveSessionState();
  }
  
  finishSession() {
    this.sessionComplete = true;
    this.showAnswer = false;
    this.titleService.setTitle(
    'Flashcard Generator | Session Results'
    );

    this.saveSessionState();
  }

  returnToDeck() {
    this.router.navigate(["/deck", "generated"]);
  }

  get reviewableCount(): number {
    return this.flashcards.length - this.knownCards.length;
  }

  saveSessionState() {
    this.studySessionService.saveSession({
    flashcards: this.flashcards,
    originalFlashcards: this.originalFlashcards,
    currentIndex: this.currentIndex,
    showAnswer: this.showAnswer,
    sessionComplete: this.sessionComplete,
    knownCards: this.knownCards,
    reviewCards: this.reviewCards,
    isWeakReviewMode: this.isWeakReviewMode
  });
}
}
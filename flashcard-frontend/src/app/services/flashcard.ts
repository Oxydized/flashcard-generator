import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class FlashcardService {
  flashcards: any[] = [];
  totalCards = 0;

  setFlashcards(cards: any[], total: number) {
    this.flashcards = cards;
    this.totalCards = total;
  }

  getFlashcards() {
    return this.flashcards;
  }

  getTotalCards() {
    return this.totalCards;
  }

  clearFlashcards() {
    this.flashcards = [];
    this.totalCards = 0;
  }
}
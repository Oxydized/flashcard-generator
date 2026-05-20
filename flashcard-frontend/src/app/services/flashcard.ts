import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class FlashcardService {
  private storageKey = 'flashcardDeck';

  flashcards: any[] = [];
  totalCards = 0;

  constructor() {
    this.loadFromStorage();
  }

  setFlashcards(cards: any[], total: number) {
    this.flashcards = cards;
    this.totalCards = total;

    this.saveToStorage();
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

    localStorage.removeItem(this.storageKey);
  }

  private saveToStorage() {
    const deckData = {
      flashcards: this.flashcards,
      totalCards: this.totalCards,
      savedAt: new Date().toISOString()
    };

    localStorage.setItem(this.storageKey, JSON.stringify(deckData));
  }

  private loadFromStorage() {
    const savedDeck = localStorage.getItem(this.storageKey);

    if(!savedDeck) {
      return;
    }

    try {
      const deckData = JSON.parse(savedDeck);

      this.flashcards = deckData.flashcards ?? [];
      this.totalCards = deckData.totalCards ?? this.flashcards.length;
    } catch (error) {
      console.error('Failed to load saved deck:', error);
      localStorage.removeItem(this.storageKey);
    }
  }
}
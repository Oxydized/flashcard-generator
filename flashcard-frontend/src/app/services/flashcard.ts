import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class FlashcardService {
  private storageKey = 'flashcardDeck';

  duplicatesSkipped = 0;
  skippedLines: any[] = [];
  importantDuplicates: any[] = [];
  
  flashcards: any[] = [];
  totalCards = 0;

  constructor() {
    this.loadFromStorage();
  }

  setFlashcards(
    cards: any[],
    total: number,
    duplicatesSkipped = 0,
    skippedLines: any[] = [],
    importantDuplicates: any[] = []
  ) {
    this.flashcards = cards;
    this.totalCards = total;
    this.duplicatesSkipped = duplicatesSkipped;
    this.skippedLines = skippedLines;
    this.importantDuplicates = importantDuplicates;

    this.saveToStorage();
  }

  getFlashcards() {
    return this.flashcards;
  }

  getTotalCards() {
    return this.totalCards;
  }

  getDuplicatesSkipped() {
    return this.duplicatesSkipped;
  }

  getSkippedLines() {
    return this.skippedLines;
  }

  getImportantDuplicates() {
    return this.importantDuplicates;
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
      duplicatesSkipped: this.duplicatesSkipped,
      skippedLines: this.skippedLines,
      importantDuplicates: this.importantDuplicates,
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

      this.duplicatesSkipped = deckData.duplicatesSkipped ?? 0;
      this.skippedLines = deckData.skippedLines ?? [];
      this.importantDuplicates = deckData.importantDuplicates ?? [];

    } catch (error) {
      console.error('Failed to load saved deck:', error);
      localStorage.removeItem(this.storageKey);
    }
  }
}
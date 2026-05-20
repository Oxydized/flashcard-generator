import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class StudySessionService {
  private storageKey = 'studySession';

  saveSession(session: any) {
    localStorage.setItem(this.storageKey, JSON.stringify(session));
  }

  loadSession() {
    const savedSession = localStorage.getItem(this.storageKey);

    if (!savedSession) {
      return null;
    }

    try {
      return JSON.parse(savedSession);
    } catch (error) {
      console.error('Failed to load study session:', error);
      localStorage.removeItem(this.storageKey);
      return null;
    }
  }

  clearSession() {
    localStorage.removeItem(this.storageKey);
  }
}
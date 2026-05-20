import { Component } from "@angular/core";
import { RouterOutlet } from "@angular/router";

@Component({
  selector: "app-root",
  standalone: true,
  templateUrl: "./app.html",
  styleUrl: "./app.css",
  imports: [RouterOutlet],
})
export class App {
  private themeStorageKey = 'themePreference';

  isDarkMode = false;

  constructor() {
    const savedTheme = localStorage.getItem(this.themeStorageKey);

    this.isDarkMode = savedTheme === 'dark';
  }

  toggleDarkMode() {
    this.isDarkMode = !this.isDarkMode;

    localStorage.setItem(
      this.themeStorageKey,
      this.isDarkMode ? 'dark' : 'light'
    );
  }
}
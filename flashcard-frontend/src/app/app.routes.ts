import { Routes } from '@angular/router';

import { Upload } from './pages/upload/upload';
import { Deck } from './pages/deck/deck';
import { Study} from './pages/study/study';

export const routes: Routes = [
    { path: '', redirectTo: 'upload', pathMatch: 'full' },

    { path: 'upload', component: Upload },

    { path: 'deck/:id', component: Deck },

    { path: 'study/:id', component: Study },
];

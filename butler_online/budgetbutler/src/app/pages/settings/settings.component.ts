import {Component} from '@angular/core';
import { PartnernameComponent } from './partnername/partnername.component';

@Component({
    selector: 'app-settings',
    templateUrl: './settings.component.html',
    styleUrls: ['./settings.component.css'],
    standalone: true,
    imports: [PartnernameComponent]
})
export class SettingsComponent {

}

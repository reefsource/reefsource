import {Component} from "@angular/core";
import {MdDialog} from "@angular/material";
import {LoginComponent} from "./components/login/login.component";

@Component({
  selector: 'app-root',
  template: `

    <h1>Reefsource</h1>
    <nav>
      <a routerLink="/how-it-works">How it Works</a>
      <a routerLink="/mission">Mission</a>
      <a routerLink="/about">About</a>
      <a routerLink="/contact">Contact</a>
      <a routerLink="/map">Map</a>
      <a (click)="login()">Login</a>
    </nav>

    <router-outlet></router-outlet>
  `,
  styles: [``]
})
export class AppComponent {
  constructor(private dialog: MdDialog) {

  }

  login() {
    let dialogRef = this.dialog.open(LoginComponent, {
      height: '400px',
      width: '600px',
    });

    dialogRef.afterClosed().subscribe(result => {
      console.log(`Dialog result: ${result}`); // Pizza!
    });
  }
}

import {Component} from "@angular/core";
import {MdDialog} from "@angular/material";
import {LoginComponent} from "./components/login/login.component";
import {Observable} from "rxjs/Observable";
import {Store} from "@ngrx/store";
import * as fromRoot from "app/reducers";
import * as userAction from "app/actions/user";
import {User} from "app/models/user";

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

      <a *ngIf="!(user$ | async)" (click)="login()">Login</a>
      <span *ngIf="(user$ | async)">{{(user$ | async)?.email }} <a (click)="logout()">logout</a></span>
    </nav>

    <router-outlet></router-outlet>
  `,
  styles: [``]
})

export class AppComponent {
  public user$: Observable<User>;

  constructor(private dialog: MdDialog, private store: Store<fromRoot.State>,) {
    this.user$ = store.select(fromRoot.getUserState);
  }

  ngOnInit() {
    this.store.dispatch(new userAction.LoadUserAction());
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

  logout() {
    this.store.dispatch(new userAction.Logout())
  }
}
import {Component, OnInit} from '@angular/core';
import {MdDialog} from '@angular/material';
import {LoginComponent} from './components/login/login.component';
import {Observable} from 'rxjs/Observable';
import {Store} from '@ngrx/store';
import * as fromRoot from 'app/reducers';
import * as userAction from 'app/actions/user';
import {User} from 'app/models/user';

@Component({
  selector: 'app-root',
  template: `
    <div class="container header-nav">
      <div class="row vertical-align">
        <h1 class="col-sm-2 text-center">REEFSOURCE</h1>
        <nav class="col-sm-8">
          <a routerLink="/how-it-works">How it Works</a>
          <a routerLink="/mission">Mission</a>
          <a routerLink="/map">Map</a>
          <a routerLink="/about">About</a>
          <a routerLink="/contact">Contact</a>
            
          <a *ngIf="!(user$ | async)" (click)="login()">Login</a>
      
          <a *ngIf="(user$ | async)" routerLink="/albums"> My Albums</a>
          <span *ngIf="(user$ | async)">{{(user$ | async)?.email }} <a (click)="logout()">logout</a></span>
        </nav>
      </div>
    </div>

    <router-outlet></router-outlet>
    
    
    <footer>
      <div class="container">
        <div class="row">
          <div class="col-sm-4">
            <h4>REEFSOURCE</h4>
            <p>A crowdsourcing environmental project funded by Brown Institute for Media Innovation.</p>
          </div>
          <div class="col-sm-2"></div>
          <div class="col-sm-3 text-right">
            <h6>CONTACT US</h6>
            <p>Address: </p>
            <p>Phone: </p>
            <p>Email: </p>
            <p></p>
          </div>
          <div class="col-sm-3 text-right">
            <h6>SOCIAL MEDIA</h6>
            <label>Medium</label>
            <label>Twitter</label>
          </div>
        </div>
      </div>

      <div class="container copyright">
        <p class="text-center"> Copyright © REEFSOUCE 2017. All right reserved. </p>
      </div>
    </footer>
    
  `,
  styles: [`
    h1, h2, h3, h4, h5, a, nav, div {
      font-family: Avenir;
    }
    h4, h6 {
      color: #aed0e8;
    }
    p, label {
      margin: 0 0 0 0;
    }
    h1 {
      margin-top: auto;
      margin-bottom: auto;
      font-size: calc(14px + 0.7vw);
    }
    .copyright {
      width: 100vw;
      margin-top: 3%;
      padding-top: 1%;
      padding-bottom: 1%;
      font-size: 0.9em;
      background-color: black;
    }
    h1, a, nav {
      color: #384163 !important;
    }
    .vertical-align {
      display: flex;
      align-items: center;
      top: 50%;
      position: absolute;
      transform: translateY(-50%);
      width: 100vw;
    }
    footer {
      padding-top: 3%;
      background-color: #384163;
      color: beige;
    }
    a {
      font-size: calc(14px + 0.5vw);
      font-variant-caps: all-petite-caps;
      margin-left: 0.5vw;
      margin-right: 0.5vw;
    }
    .header-nav {
      height: 10vh;
      position: relative;
    }
  `]
})

export class AppComponent implements OnInit {
  public user$: Observable<User>;

  constructor(private dialog: MdDialog, private store: Store<fromRoot.State>,) {
    this.user$ = store.select(fromRoot.getUserState);
  }

  ngOnInit() {
    this.store.dispatch(new userAction.LoadUserAction());
  }

  login() {
    const dialogRef = this.dialog.open(LoginComponent, {
      height: '50%',
      width: '50%',
    });

    dialogRef.afterClosed().subscribe(result => {
      console.log(`Dialog result: ${result}`);
    });
  }

  logout() {
    this.store.dispatch(new userAction.Logout());
  }
}

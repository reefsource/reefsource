import {Component, OnInit} from '@angular/core';
import {LoginComponent} from '../login/login.component';
import {MdDialog} from '@angular/material';
import * as fromRoot from 'app/reducers';
import * as userAction from 'app/actions/user';
import {Observable} from 'rxjs/Observable';
import {Store} from '@ngrx/store';
import {User} from '../../models/user';

@Component({
  selector: 'header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css']
})
export class HeaderComponent implements OnInit {
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

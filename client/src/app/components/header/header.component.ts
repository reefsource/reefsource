import {Component, OnInit} from '@angular/core';
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
    window.location.href = '/oauth2/login/google-oauth2/';
  }

  logout() {
    this.store.dispatch(new userAction.Logout());
  }
}

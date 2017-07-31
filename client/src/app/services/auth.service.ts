import {Injectable} from '@angular/core';
import {Store} from '@ngrx/store';
import * as fromRoot from 'app/reducers';
import * as userAction from 'app/actions/user';
import {Router} from '@angular/router';
import {User} from '../models/user';
import * as Raven from 'raven-js';

@Injectable()
export class AuthService {
  isLoggedIn() {
    return localStorage.getItem('isLoggedIn') === 'true';
  }

  constructor(private store: Store<fromRoot.State>, public router: Router) {
    let user$ = store.select(fromRoot.getUserState);

    this.store.dispatch(new userAction.LoadUserAction());

    user$
      .subscribe((user: User) => {
        if (typeof user !== 'undefined') {
          localStorage.setItem('isLoggedIn', (!!user).toString());
        }
        Raven.setUserContext(!!user ? {
          id: user.id,
          username: user.username,
          email: user.email
        } : null);
      })
  }

  // store the URL so we can redirect after logging in
  redirectUrl: string;

  login_google_OAuth() {
    let redirectUrl = '/oauth2/login/google-oauth2/';
    if (this.redirectUrl) {
      redirectUrl += `?next=${this.redirectUrl}`
    }
    window.location.href = redirectUrl;
  }

  logout(): void {
    this.store.dispatch(new userAction.Logout());
    this.router.navigate(['/how-it-works']);
  }
}

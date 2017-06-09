import {Injectable} from '@angular/core';
import {Observable} from 'rxjs/Observable';
import {Store} from '@ngrx/store';
import * as fromRoot from 'app/reducers';
import * as userAction from 'app/actions/user';
import {Router} from '@angular/router';
import {User} from '../models/user';
import * as Raven from 'raven-js';

@Injectable()
export class AuthService {
  isLoggedIn: boolean = false;

  constructor(private store: Store<fromRoot.State>, public router: Router) {
    let user$ = store.select(fromRoot.getUserState);

    user$
      .subscribe((user: User) => {
        this.isLoggedIn = !!user;

        Raven.setUserContext(this.isLoggedIn ? {
          id: user.id,
          username: user.username,
          email: user.email
        } : null);

        // if (!this.isLoggedIn) {
        //   router.navigate(['/']);
        // }
      })
  }

  // store the URL so we can redirect after logging in
  redirectUrl: string;

  login(): Observable<boolean> {
    return Observable.of(true).do(val => this.isLoggedIn = true);
  }

  login_google_OAuth() {
    let redirectUrl = '/oauth2/login/google-oauth2/';
    if (this.redirectUrl) {
      redirectUrl += `?next=${this.redirectUrl}`
    }
    window.location.href = redirectUrl;
  }

  logout(): void {
    this.store.dispatch(new userAction.Logout());
  }
}

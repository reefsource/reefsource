import 'rxjs/add/operator/mergeMap';
import 'rxjs/add/operator/map';
import 'rxjs/add/operator/catch';
import {of} from 'rxjs/observable/of';

import {Injectable} from '@angular/core';
import {Actions, Effect} from '@ngrx/effects';
import {Action} from '@ngrx/store';
import {Observable} from 'rxjs/Observable';

import {UserService} from '../services/user.service';
import * as userActions from '../actions/user';

@Injectable()
export class UserEffects {
  constructor(private actions$: Actions,
              private userService: UserService) {
  }

  @Effect()
  loadUser$: Observable<Action> = this.actions$.ofType(userActions.LOAD_USER)
    .mergeMap(payload => this.userService.getProfile()
      .map(user => new userActions.LoadUserSuccessAction(user))
      .catch(() => of(new userActions.LoggedOut()))
    );

  @Effect()
  logout$: Observable<Action> = this.actions$.ofType(userActions.LOGOUT)
    .mergeMap(payload => this.userService.logout()
      .map(user => new userActions.LogoutSuccess(null))
    );

  @Effect()
  loggedOut$: Observable<Action> = this.actions$.ofType(userActions.LOGGEDOUT)
    .map(user => new userActions.LogoutSuccess(null));
}

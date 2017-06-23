import 'rxjs/add/operator/switchMap';
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
  loadUser$: Observable<Action> = this.actions$
    .ofType(userActions.LOAD_USER)
    .switchMap(() => this.userService.getProfile())
    .map(user => new userActions.LoadUserSuccessAction(user));

  @Effect()
  logout$: Observable<Action> = this.actions$
    .ofType(userActions.LOGOUT)
    .switchMap(() => this.userService.logout())
    .map(user => new userActions.LogoutSucess(null));

  @Effect()
  loggedOut$: Observable<Action> = this.actions$
    .ofType(userActions.LOGGEDOUT)
    .map(user => new userActions.LogoutSucess(null));
}

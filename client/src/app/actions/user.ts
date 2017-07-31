import {Action} from '@ngrx/store';
import {User} from '../models/user';

export const LOAD_USER = '[User] Load User';
export const LOAD_USER_SUCCESS = '[User] Load User Success';
export const LOGOUT = '[User] Logout';
export const LOGGEDOUT = '[User] LOGGED OUT';
export const LOGOUT_SUCCESS = '[User] Logout Succes';

export class LoadUserAction implements Action {
  readonly type = LOAD_USER;

  constructor() {
  }
}

export class LoadUserSuccessAction implements Action {
  readonly type = LOAD_USER_SUCCESS;

  constructor(public payload: User) {
  }
}

export class Logout implements Action {
  readonly type = LOGOUT;
}

export class LoggedOut implements Action {
  readonly type = LOGGEDOUT;
}

export class LogoutSuccess implements Action {
  readonly type = LOGOUT_SUCCESS;

  constructor(public payload: User) {
  }
}

export type Actions
  = LoadUserAction
  | LoadUserSuccessAction
  | Logout
  | LogoutSuccess;

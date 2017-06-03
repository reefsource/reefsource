import {Action} from '@ngrx/store';
import {PaginatedResult, Result} from '../models/result';

export const LOAD_RESULTS_ACTION = '[Action] Load Results';
export const LOAD_RESULTS_ACTION_SUCCESS = '[Action] Load Results Success';

export class LoadResultsAction implements Action {
  readonly type = LOAD_RESULTS_ACTION;

  constructor() {
  }
}

export class LoadResultsSuccessAction implements Action {
  readonly type = LOAD_RESULTS_ACTION_SUCCESS;

  constructor(public payload: PaginatedResult) {
  }
}

export type Actions
  = LoadResultsAction
  | LoadResultsSuccessAction;

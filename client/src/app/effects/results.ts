import 'rxjs/add/operator/switchMap';
import {Injectable} from '@angular/core';
import {Actions, Effect} from '@ngrx/effects';
import {Action} from '@ngrx/store';
import {Observable} from 'rxjs/Observable';

import * as resultActions from '../actions/result';
import {ResultService} from '../services/result.service';

@Injectable()
export class ResultEffects {
  constructor(private actions$: Actions,
              private resultService: ResultService) {
  }

  @Effect()
  loadResults$: Observable<Action> = this.actions$
    .ofType(resultActions.LOAD_RESULTS_ACTION)
    .switchMap(() => this.resultService.getResults())
    .map(response => new resultActions.LoadResultsSuccessAction(response));
}

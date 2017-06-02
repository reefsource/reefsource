import * as resultActions from '../actions/result';
import {Result} from '../models/result';

export type  State = Result[];

const initialState: State = null;

export function reducer(state = initialState, action: resultActions.Actions): State {
  switch (action.type) {
    case resultActions.LOAD_RESULTS_ACTION: {
      return initialState;
    }

    case resultActions.LOAD_RESULTS_ACTION_SUCCESS: {
      return action.payload;
    }

    default: {
      return state;
    }
  }
}

import * as albumActions from '../actions/album';
import {Album} from '../models/album';

export type  State = Album;

const initialState: State = null;

export function reducer(state = initialState, action: albumActions.Actions): State {
  switch (action.type) {
    case albumActions.LOAD_ALBUM_ACTION: {
      return initialState;
    }

    case albumActions.LOAD_ALBUM_ACTION_SUCCESS: {
      return action.payload;
    }


    default: {
      return state;
    }
  }
}

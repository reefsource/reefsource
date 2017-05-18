import { User } from '../models/user';
import * as user from '../actions/user';

export type  State = User;

const initialState: State = null;

export function reducer(state = initialState, action: user.Actions): State {
  switch (action.type) {
    case user.LOAD_USER: {
      return initialState;
    }


    case user.LOAD_USER_SUCCESS:
    case user.LOGOUT_SUCCESS: {
      return action.payload;
    }


    default: {
      return state;
    }
  }
}

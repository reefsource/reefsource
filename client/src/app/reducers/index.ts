import { ActionReducerMap } from '@ngrx/store';

import * as fromUser from './user';
import * as fromAlbums from './albums';
import * as fromAlbum from './album';

export interface State {
  user?: fromUser.State;
  albums?: fromAlbums.State;
  album?: fromAlbum.State;
}

export const reducers: ActionReducerMap<State> = {
  user: fromUser.reducer,
  albums: fromAlbums.reducer,
  album: fromAlbum.reducer,
};

export const getUserState = (state: State) => state.user;
export const getAlbumsState = (state: State) => state.albums;
export const getAlbumState = (state: State) => state.album;

import {Action} from "@ngrx/store";
import {Album} from "../models/album";

export const LOAD_ALBUMS_ACTION = '[Action] Load Actions';
export const LOAD_ALBUMS_ACTION_SUCCESS = '[Action] Load Actions Success';
export const LOAD_ALBUM_ACTION = '[Action] Load Action';
export const LOAD_ALBUM_ACTION_SUCCESS = '[Action] Load Action Success';

export class LoadAlbumsAction implements Action {
  readonly type = LOAD_ALBUMS_ACTION;

  constructor() {
  }
}

export class LoadAlbumsSuccessAction implements Action {
  readonly type = LOAD_ALBUMS_ACTION_SUCCESS;

  constructor(public payload: Album[]) {
  }
}

export class LoadAlbumAction implements Action {
  readonly type = LOAD_ALBUM_ACTION;

  constructor(public payload: number) {

  }
}

export class LoadAlbumSuccessAction implements Action {
  readonly type = LOAD_ALBUM_ACTION_SUCCESS;

  constructor(public payload: Album) {
  }
}


export type Actions
  = LoadAlbumsAction
  | LoadAlbumsSuccessAction
  | LoadAlbumAction
  | LoadAlbumSuccessAction;

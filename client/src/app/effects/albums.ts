import "rxjs/add/operator/switchMap";
import {Injectable} from "@angular/core";
import {Actions, Effect} from "@ngrx/effects";
import {Action} from "@ngrx/store";
import {Observable} from "rxjs/Observable";

import * as albumActions from "../actions/album";
import {AlbumService} from "../services/album.service";

@Injectable()
export class AlbumEffects {
  constructor(private actions$: Actions,
              private albumService: AlbumService) {
  }

  @Effect()
  loadAlbums$: Observable<Action> = this.actions$
    .ofType(albumActions.LOAD_ALBUMS_ACTION)
    .switchMap(() => this.albumService.getAlbums())
    .map(albums => new albumActions.LoadAlbumsSuccessAction(albums));

  @Effect()
  loadAlbum$: Observable<Action> = this.actions$
    .ofType(albumActions.LOAD_ALBUM_ACTION)
    .map(action => +JSON.stringify(action.payload))
    .switchMap((albumId) => this.albumService.getAlbum(albumId))
    .map(album => new albumActions.LoadAlbumSuccessAction(album));

}

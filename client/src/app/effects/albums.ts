import 'rxjs/add/operator/mergeMap';
import 'rxjs/add/operator/map';
import 'rxjs/add/operator/catch';

import {Injectable} from '@angular/core';
import {Actions, Effect} from '@ngrx/effects';
import {Action} from '@ngrx/store';
import {Observable} from 'rxjs/Observable';

import * as albumActions from '../actions/album';
import * as userActions from '../actions/user';
import {LoadAlbumAction} from '../actions/album';
import {AlbumService} from '../services/album.service';
import {of} from 'rxjs/observable/of';

@Injectable()
export class AlbumEffects {
  constructor(private actions$: Actions,
              private albumService: AlbumService) {
  }

  @Effect()
  loadAlbums$: Observable<Action> = this.actions$.ofType(albumActions.LOAD_ALBUMS_ACTION)
    .mergeMap(payload => this.albumService.getAlbums()
      .map(albums => new albumActions.LoadAlbumsSuccessAction(albums))
      .catch(() => of(new userActions.LoggedOut()))
    );

  @Effect()
  loadAlbum$: Observable<Action> = this.actions$.ofType(albumActions.LOAD_ALBUM_ACTION)
    .map((action: LoadAlbumAction) => +JSON.stringify(action.payload))
    .mergeMap(albumId => this.albumService.getAlbum(albumId)
      .map(album => new albumActions.LoadAlbumSuccessAction(album))
      .catch(() => of(new userActions.LoggedOut()))
    );
}

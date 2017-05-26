import {Component, OnInit} from '@angular/core';
import {ActivatedRoute, Params} from '@angular/router';
import {Album} from 'app/models/album';
import {Store} from '@ngrx/store';
import 'rxjs/add/operator/switchMap';

import * as fromRoot from '../../reducers';
import * as albumActions from '../../actions/album';
import {AlbumService} from '../../services/album.service';

@Component({
  selector: 'app-album',
  templateUrl: './album.component.html',
  styleUrls: ['./album.component.css']
})
export class AlbumComponent implements OnInit {

  public album: Album;

  constructor(private albumService: AlbumService,
              private route: ActivatedRoute,
              private store: Store<fromRoot.State>) {

  }

  ngOnInit() {
    this.route.params
      .switchMap((params: Params) => {
        const albumId = +params['albumId'];

        this.store.dispatch(new albumActions.LoadAlbumAction(albumId));

        return this.store.select(fromRoot.getAlbumState)
      })
      .subscribe((album: Album) => this.album = album);
  }
}


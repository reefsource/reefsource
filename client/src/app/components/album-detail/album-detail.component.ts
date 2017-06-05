import {Component, OnInit} from '@angular/core';
import {ActivatedRoute, Params} from '@angular/router';
import {Album} from 'app/models/album';
import {Store} from '@ngrx/store';
import 'rxjs/add/operator/switchMap';

import * as fromRoot from '../../reducers';
import * as albumActions from '../../actions/album';
import {Observable} from 'rxjs/Observable';

@Component({
  selector: 'app-album-detail',
  templateUrl: './album-detail.component.html',
  styleUrls: ['./album-detail.component.css']
})
export class AlbumDetailComponent implements OnInit {

  public album$: Observable<Album>;

  constructor(private route: ActivatedRoute,
              private store: Store<fromRoot.State>) {

    this.album$ = store.select(fromRoot.getAlbumState);
  }

  ngOnInit() {
    this.route.params
      .subscribe((params: Params) => {
        const albumId = +params['albumId'];
        this.store.dispatch(new albumActions.LoadAlbumAction(albumId))
      });
  }
}

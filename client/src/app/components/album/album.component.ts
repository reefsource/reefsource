import {Component, OnInit} from "@angular/core";
import {ActivatedRoute} from "@angular/router";
import {Observable} from "rxjs/Observable";
import {Album} from "app/models/album";
import {Store} from "@ngrx/store";

import * as fromRoot from "../../reducers";
import * as albumActions from "../../actions/album";
import {AlbumService} from "../../services/album.service";

@Component({
  selector: 'app-album',
  templateUrl: './album.component.html',
  styleUrls: ['./album.component.css']
})
export class AlbumComponent implements OnInit {

  public album$: Observable<Album>;
  private albumId: number;

  constructor(private albumService: AlbumService,
              private route: ActivatedRoute,
              private store: Store<fromRoot.State>) {

    this.album$ = store.select(fromRoot.getAlbumState);
  }

  ngOnInit() {
    this.albumId = +this.route.params['value']['albumId'];

    this.store.dispatch(new albumActions.LoadAlbumAction(this.albumId));
  }

  fileChange($event) {
    this.albumService.uploadFile(this.albumId, $event.target.files);
  }
}


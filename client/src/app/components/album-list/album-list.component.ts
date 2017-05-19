import {Component, OnInit} from "@angular/core";
import {Observable} from "rxjs/Observable";
import {Album} from "../../models/album";
import {Store} from "@ngrx/store";
import * as fromRoot from "../../reducers";
import * as albumActions from "../../actions/album";
import {Router} from "@angular/router";

@Component({
  selector: 'app-album-list',
  templateUrl: './album-list.component.html',
  styleUrls: ['./album-list.component.css']
})
export class AlbumListComponent implements OnInit {
  public albums$: Observable<Album[]>;

  constructor(private store: Store<fromRoot.State>, private router: Router) {
    this.albums$ = store.select(fromRoot.getAlbumsState);
  }

  ngOnInit() {
    this.store.dispatch(new albumActions.LoadAlbumsAction());
  }

}

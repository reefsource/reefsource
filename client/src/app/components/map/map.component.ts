import {Component, OnInit} from '@angular/core';
import {Observable} from 'rxjs/Observable';
import {PaginatedResult} from '../../models/result';
import * as fromRoot from '../../reducers';
import {Store} from '@ngrx/store';
import * as resultActions from '../../actions/result';

@Component({
  selector: 'app-map',
  templateUrl: './map.component.html',
  styleUrls: ['./map.component.css']
})
export class MapComponent implements OnInit {

  lat: number = 24.275;
  lng: number = 0.89;
  zoom: number = 2;

  public results$: Observable<PaginatedResult>;

  constructor(private store: Store<fromRoot.State>) {
    this.results$ = store.select(fromRoot.getResultsState);
  }

  ngOnInit() {
    this.store.dispatch(new resultActions.LoadResultsAction());
  }
}

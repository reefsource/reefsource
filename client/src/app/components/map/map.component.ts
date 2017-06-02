import {Component, OnInit} from '@angular/core';
import {Observable} from 'rxjs/Observable';
import {Result} from '../../models/result';
import * as fromRoot from '../../reducers';
import {Store} from '@ngrx/store';
import * as resultActions from '../../actions/result';

@Component({
  selector: 'app-map',
  templateUrl: './map.component.html',
  styleUrls: ['./map.component.css']
})
export class MapComponent implements OnInit {

  lat: number = 0;
  lng: number = 0;

  zoom: number = 12;
  public results$: Observable<Result[]>;
  public results: Result[] = [];

  constructor(private store: Store<fromRoot.State>) {
    this.results$ = store.select(fromRoot.getResultsState);
  }

  ngOnInit() {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(this.setPosition.bind(this));
    }

    this.store.dispatch(new resultActions.LoadResultsAction());
    this.results$.subscribe((results) => {
      this.results = results;
    })
  }

  setPosition(position) {
    this.lat = position.coords.latitude;
    this.lng = position.coords.longitude;
  }
}


import {Component, OnInit} from '@angular/core';
import {PaginatedResult, Result} from '../../models/result';
import {ResultService} from '../../services/result.service';

@Component({
  selector: 'app-map',
  templateUrl: './map.component.html',
  styleUrls: ['./map.component.css']
})
export class MapComponent implements OnInit {

  lat: number = 24.275;
  lng: number = 0.89;
  zoom: number = 2;

  public results: PaginatedResult<Result>;

  constructor(private resultService: ResultService) {

  }

  ngOnInit() {
    this.resultService.getResults()
      .subscribe((resonse) => {
        this.results = resonse;
      }, err => {
        // Log errors if any
        console.log(err);
      });
  }
}

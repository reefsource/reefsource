import 'rxjs/add/operator/map';
import 'rxjs/add/operator/catch';
import 'rxjs/add/operator/filter';

import {Injectable} from '@angular/core';
import {Http} from '@angular/http';
import {Observable} from 'rxjs/Observable';
import {BaseService} from './base.service';
import {PaginatedResult, Result} from '../models/result';
import {Album} from '../models/album';

@Injectable()
export class ResultService extends BaseService {

  constructor(private http: Http) {
    super();
  }

  getResults(): Observable<PaginatedResult<Result>> {
    return this.http.get('/api/v1/results/')
      .map(res => res.json())
      .map((res) => {

        let map = {};

        res.results = res.results.map((item) => {
          item.score = item.score.toFixed(2);

          let key = item.location.coordinates[0] + '' + item.location.coordinates[1];
          if (map[key]) {
            map[key].push(item.score);
          } else {
            map[key] = [item.score];
          }

          return item;
        });


        return res;
      })
      .catch(this.handleError);
  }

  getAlbumsResults(): Observable<PaginatedResult<Album>> {
    return this.http.get('/api/v1/results/albums/')
      .map(res => {
        let tmp = res.json();
        return tmp;
      })

      .map((res) => {

        res.results = res.results.filter((item) => item.weighted_result > 0);
        res.results = res.results.map((item) => {
          item.weighted_result = item.weighted_result.toFixed(2);
          return item;
        });

        return res;
      })
      .catch(this.handleError);
  }
}

import {Injectable} from '@angular/core';
import {Http} from '@angular/http';
import {Observable} from 'rxjs/Observable';
import {BaseService} from './base.service';
import {PaginatedResult, Result} from '../models/result';

@Injectable()
export class ResultService extends BaseService {

  constructor(private http: Http) {
    super();
  }

  getResults(): Observable<PaginatedResult<Result>> {
    return this.http.get('/api/v1/results/')
      .map(res => res.json())
      .map((res) => {
        res.results = res.results.map((item) => {
          item.score = '' + item.score.toFixed(2);
          return item;
        });
        return res;
      })
      .catch(this.handleError);
  }
}

import {Injectable} from '@angular/core';
import {Http} from '@angular/http';
import {Observable} from 'rxjs/Observable';
import {BaseService} from './base.service';
import {Result} from '../models/result';

@Injectable()
export class ResultService extends BaseService {

  constructor(private http: Http) {
    super();
  }

  getResults(): Observable<Result[]> {
    return this.http.get('/api/v1/results/?stage=stage_2')
      .map(res => res.json())
      .catch(this.handleError);
  }
}

import {Injectable} from '@angular/core';
import {Observable} from 'rxjs/Observable';
import {Headers, RequestOptions} from '@angular/http';
@Injectable()
export class BaseService {

  constructor() {
  }

  protected handleError(error: Response) {
    return Observable.throw(error.json() || 'Server error');
  }

  protected getOptions() {
    let headers = new Headers({'Content-Type': 'application/json'});
    return new RequestOptions({headers: headers});

  }
}

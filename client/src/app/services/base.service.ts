import { Injectable } from '@angular/core';
import {Observable} from "rxjs/Observable";

@Injectable()
export class BaseService {

  constructor() { }

  protected handleError(error: Response) {
    return Observable.throw(error.json() || 'Server error');
  }

}

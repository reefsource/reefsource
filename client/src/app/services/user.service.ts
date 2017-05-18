import { Injectable } from '@angular/core';
import { Http, Response } from '@angular/http';
import { Observable } from 'rxjs/Rx';

import { User } from '../models/user';

@Injectable()
export class UserService {

  constructor(
    private http: Http,
  ) { }

  getProfile(): Observable<User> {
    return this.http.get('/api/v1/users/profile/')
      .map(res => res.json())
      .catch(this.handleError);
  }

  logout(): Observable<User> {
    return this.http.post('/api/v1/users/logout/', {})
      .map(res => res.json())
      .catch(this.handleError);
  }

  private handleError(error: Response) {
    return Observable.throw(error.json().error || 'Server error');
  }
}

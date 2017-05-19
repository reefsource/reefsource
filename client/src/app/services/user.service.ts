import {Injectable} from "@angular/core";
import {Http} from "@angular/http";
import {Observable} from "rxjs/Rx";

import {User} from "../models/user";
import {BaseService} from "./base.service";

@Injectable()
export class UserService extends BaseService {

  constructor(private http: Http,) {
    super();
  }

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


}

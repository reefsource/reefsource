import {Component, OnInit} from '@angular/core';
import * as fromRoot from 'app/reducers';
import {Store} from '@ngrx/store';
import {Observable} from 'rxjs/Observable';
import {AuthService} from '../../services/auth.service';
import {User} from '../../models/user';

@Component({
  selector: 'app-how-it-works',
  templateUrl: './how-it-works.component.html',
  styleUrls: ['./how-it-works.component.css']
})
export class HowItWorksComponent implements OnInit {
  public user$: Observable<User>;

  constructor(private store: Store<fromRoot.State>, private authService: AuthService) {
    this.user$ = store.select(fromRoot.getUserState);
  }

  ngOnInit() {
  }

  login() {
     this.authService.login_google_OAuth();
  }
}

import {Component} from '@angular/core';
import {ActivatedRouteSnapshot, Resolve, RouterStateSnapshot} from '@angular/router';
import {Observable} from 'rxjs/Observable';
import {AuthService} from './services/auth.service';
import * as fromRoot from 'app/reducers';
import * as userAction from 'app/actions/user';
import {Store} from '@ngrx/store';
import {User} from './models/user';

@Component({
  selector: 'app-root',
  template: `
    <header></header>
    <div class="content">
        <router-outlet></router-outlet>
    </div>
    <footer></footer>
`,
  styles: [`
    :host {
      display: flex;
      flex-direction: column;
      min-height:100vh;
    }
    .content {
      flex-grow:1;
    }
  `]
})

export class AppComponent {
}

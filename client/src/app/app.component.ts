import {Component} from '@angular/core';
import {getHttpHeadersOrInit, HttpInterceptorService} from 'ng-http-interceptor/dist';

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
  constructor(httpInterceptor: HttpInterceptorService) {
    httpInterceptor.request().addInterceptor((data, method) => {
      const headers = getHttpHeadersOrInit(data, method);
      headers.set('X-Requested-With', 'XMLHttpRequest');
      return data;
    });
  }
}

import {Component} from '@angular/core';

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

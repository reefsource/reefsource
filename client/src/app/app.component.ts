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
    .content {
      min-height: 80vh
    }
  `]
})

export class AppComponent {

}

import {Pipe, PipeTransform} from '@angular/core';
import {environment} from '../../environments/environment';

@Pipe({
  name: 'static'
})
export class StaticPipe implements PipeTransform {

  transform(value: any, args?: any): any {

    if (environment.production) {
      return `${environment.static_path}/${value}`;
    } else {
      return `${value}`;
    }
  }
}

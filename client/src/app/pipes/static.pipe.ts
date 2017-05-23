import {Pipe, PipeTransform} from '@angular/core';

@Pipe({
  name: 'static'
})
export class StaticPipe implements PipeTransform {

  transform(value: any, args?: any): any {
    return `https://static.coralreefsource.org/${value}`;
  }

}

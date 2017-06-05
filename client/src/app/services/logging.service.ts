import {Injectable} from '@angular/core';

@Injectable()
export class LoggingService {

  constructor() {
  }

  log(message) {
    console.log(message);
  }

}

import {ErrorHandler, Injectable, Injector} from '@angular/core';
import {LocationStrategy, PathLocationStrategy} from '@angular/common';
import {LoggingService} from './logging.service';


@Injectable()
export class GlobalErrorHandlerService implements ErrorHandler {
  constructor(private injector: Injector) {
  }

  handleError(error) {
    const loggingService = this.injector.get(LoggingService);
    const location = this.injector.get(LocationStrategy);

    const message = error.message ? error.message : error.toString();

    loggingService.log({message});

    throw error;
  }
}

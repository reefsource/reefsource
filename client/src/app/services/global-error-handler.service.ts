import {ErrorHandler, Injectable, Injector} from '@angular/core';
import {LocationStrategy} from '@angular/common';
import {LoggingService} from './logging.service';
import * as Raven from 'raven-js';

@Injectable()
export class GlobalErrorHandlerService implements ErrorHandler {
  constructor(private injector: Injector) {
  }

  handleError(err) {
    const loggingService = this.injector.get(LoggingService);
    const location = this.injector.get(LocationStrategy);

    Raven.captureException(err.originalError || err);
  }
}

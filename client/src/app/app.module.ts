import 'hammerjs';

import {BrowserModule} from '@angular/platform-browser';
import {ErrorHandler, NgModule} from '@angular/core';
import {FormsModule} from '@angular/forms';
import {CookieXSRFStrategy, HttpModule, XSRFStrategy} from '@angular/http';
import {StoreModule} from '@ngrx/store';
import {EffectsModule} from '@ngrx/effects';
import {StoreDevtoolsModule} from '@ngrx/store-devtools';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import {AgmCoreModule} from '@agm/core';
import {MdButtonModule, MdDatepickerModule, MdDialogModule, MdInputModule, MdMenuModule, MdNativeDateModule, MdProgressBarModule, MdSlideToggleModule} from '@angular/material';

import {reducer} from './reducers';
import {AppRoutingModule} from './app-routing.module';

import {AppComponent} from './app.component';

import {HowItWorksComponent} from './components/how-it-works/how-it-works.component';
import {MapComponent} from './components/map/map.component';
import {AboutComponent} from './components/about/about.component';
import {ContactComponent} from './components/contact/contact.component';
import {MissionComponent} from './components/mission/mission.component';
import {AlbumListComponent} from './components/album-list/album-list.component';
import {AlbumNewComponent} from './components/album-new/album-new.component';
import {AlbumDetailComponent} from './components/album-detail/album-detail.component';
import {UploaderComponent} from './components/uploader/uploader.component';
import {HeaderComponent} from './components/header/header.component';
import {FooterComponent} from './components/footer/footer.component';
import {LoginComponent} from './components/login/login.component';

import {UserEffects} from './effects/user';
import {AlbumEffects} from './effects/albums';

import {UserService} from './services/user.service';
import {AlbumService} from './services/album.service';
import {AuthService} from './services/auth.service';

import {HttpInterceptorModule} from 'ng-http-interceptor';
import {FileUploadModule} from 'ng2-file-upload';
import {CookieModule} from 'ngx-cookie';
import {StaticPipe} from './pipes/static.pipe';

import {AuthGuard} from './guards/auth.guard';
import {environment} from '../environments/environment';
import {ResultService} from './services/result.service';
import {ResultEffects} from './effects/results';
import {LoggingService} from './services/logging.service';
import {GlobalErrorHandlerService} from './services/global-error-handler.service';

import {LoginRoutingModule} from './login-routing.module';
import * as Raven from 'raven-js';

Raven.config('https://83f43a32b29647df9aaba46355c4564e@sentry.io/166728').install();

export function xsrfFactory() {
  return new CookieXSRFStrategy('csrftoken', 'X-CSRFToken');
}

@NgModule({
  declarations: [
    AppComponent,
    HowItWorksComponent,
    MapComponent,
    AboutComponent,
    ContactComponent,
    MissionComponent,
    AlbumListComponent,
    AlbumNewComponent,
    AlbumDetailComponent,
    UploaderComponent,
    StaticPipe,
    FooterComponent,
    HeaderComponent,
    LoginComponent,
  ],
  imports: [
    BrowserModule,
    FormsModule,
    HttpModule,
    HttpInterceptorModule,
    FileUploadModule,
    AppRoutingModule,
    LoginRoutingModule,
    MdNativeDateModule, MdDialogModule, MdButtonModule, MdMenuModule, MdDatepickerModule, MdInputModule, MdProgressBarModule, MdSlideToggleModule,
    CookieModule.forRoot(),
    BrowserAnimationsModule,
    StoreModule.provideStore(reducer),
    StoreDevtoolsModule.instrumentOnlyWithExtension(),
    EffectsModule.run(UserEffects),
    EffectsModule.run(AlbumEffects),
    EffectsModule.run(ResultEffects),
    AgmCoreModule.forRoot({apiKey: environment.google_map_api_key}),
  ],

  providers: [
    UserService,
    AlbumService,
    ResultService,
    AuthService,
    AuthGuard,
    LoggingService,
    {provide: XSRFStrategy, useFactory: xsrfFactory},
    {provide: ErrorHandler, useClass: GlobalErrorHandlerService}
  ],
  entryComponents: [
    AlbumNewComponent
  ],
  bootstrap: [AppComponent]
})
export class AppModule {

}

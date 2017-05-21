import "hammerjs";

import {BrowserModule} from "@angular/platform-browser";
import {NgModule} from "@angular/core";
import {FormsModule} from "@angular/forms";
import {CookieXSRFStrategy, Http, HttpModule, XSRFStrategy} from "@angular/http";
import {StoreModule} from "@ngrx/store";
import {EffectsModule} from "@ngrx/effects";
import {StoreDevtoolsModule} from "@ngrx/store-devtools";
import {BrowserAnimationsModule} from "@angular/platform-browser/animations";

import {MdButtonModule, MdDialogModule} from "@angular/material";

import {reducer} from "./reducers";
import {AppRoutingModule} from "./app-routing.module";

import {AppComponent} from "./app.component";

import {HowItWorksComponent} from "./components/how-it-works/how-it-works.component";
import {MapComponent} from "./components/map/map.component";
import {AboutComponent} from "./components/about/about.component";
import {ContactComponent} from "./components/contact/contact.component";
import {LoginComponent} from "./components/login/login.component";
import {MissionComponent} from "./components/mission/mission.component";
import {AlbumListComponent} from "./components/album-list/album-list.component";
import {AlbumComponent} from "./components/album/album.component";
import {UploaderComponent} from "./components/uploader/uploader.component";

import {UserEffects} from "./effects/user";
import {AlbumEffects} from "./effects/albums";

import {UserService} from "./services/user.service";
import {AlbumService} from "./services/album.service";
import {getHttpHeadersOrInit, HttpInterceptorModule, HttpInterceptorService} from "ng-http-interceptor";
import {FileUploadModule} from "ng2-file-upload";
import {CookieService} from "angular2-cookie/services/cookies.service";

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
    LoginComponent,
    MissionComponent,
    AlbumListComponent,
    AlbumComponent,
    UploaderComponent,
  ],
  imports: [
    BrowserModule,
    FormsModule,
    HttpModule,
    HttpInterceptorModule,
    FileUploadModule,
    AppRoutingModule,
    MdDialogModule,
    MdButtonModule,
    BrowserAnimationsModule,
    StoreModule.provideStore(reducer),
    StoreDevtoolsModule.instrumentOnlyWithExtension(),
    EffectsModule.run(UserEffects),
    EffectsModule.run(AlbumEffects),
  ],

  providers: [
    UserService,
    AlbumService,
    CookieService,
    {provide: XSRFStrategy, useFactory: xsrfFactory}
  ],
  entryComponents: [
    LoginComponent
  ],
  bootstrap: [AppComponent]
})
export class AppModule {
  constructor(http: Http, httpInterceptor: HttpInterceptorService) {
    httpInterceptor.request().addInterceptor((data, method) => {
      const headers = getHttpHeadersOrInit(data, method);
      headers.set('X-Requested-With', 'XMLHttpRequest');
      return data;
    });
  }
}

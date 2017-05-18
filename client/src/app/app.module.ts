import "hammerjs";

import {BrowserModule} from "@angular/platform-browser";
import {NgModule} from "@angular/core";
import {FormsModule} from "@angular/forms";
import {HttpModule} from "@angular/http";
import {StoreModule} from "@ngrx/store";
import {EffectsModule} from "@ngrx/effects";
import {StoreDevtoolsModule} from "@ngrx/store-devtools";
import {MaterialModule} from "@angular/material";
import {BrowserAnimationsModule} from "@angular/platform-browser/animations";

import {reducer} from "./reducers";
import {AppRoutingModule} from "./app-routing.module";

import {AppComponent} from "./app.component";
import {UsersComponent} from "./components/users/users.component";

import {HowItWorksComponent} from "./components/how-it-works/how-it-works.component";
import {MapComponent} from "./components/map/map.component";
import {AboutComponent} from "./components/about/about.component";
import {ContactComponent} from "./components/contact/contact.component";
import {LoginComponent} from "./components/login/login.component";
import {MissionComponent} from "./components/mission/mission.component";

import {UserEffects} from "./effects/user";

import {UserService} from "./services/user.service";


@NgModule({
  declarations: [
    AppComponent,
    UsersComponent,
    HowItWorksComponent,
    MapComponent,
    AboutComponent,
    ContactComponent,
    LoginComponent,
    MissionComponent,
  ],
  imports: [
    BrowserModule,
    FormsModule,
    HttpModule,
    AppRoutingModule,
    MaterialModule,
    BrowserAnimationsModule,
    StoreModule.provideStore(reducer),
    StoreDevtoolsModule.instrumentOnlyWithExtension(),
    EffectsModule.run(UserEffects),
  ],
  providers: [
    UserService,
  ],
  entryComponents: [
    LoginComponent
  ],
  bootstrap: [AppComponent]
})
export class AppModule {
}

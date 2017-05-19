import {NgModule} from "@angular/core";
import {RouterModule, Routes} from "@angular/router";

import {HowItWorksComponent} from "./components/how-it-works/how-it-works.component";
import {AboutComponent} from "./components/about/about.component";
import {ContactComponent} from "./components/contact/contact.component";
import {MapComponent} from "./components/map/map.component";
import {MissionComponent} from "./components/mission/mission.component";
import {AlbumListComponent} from "app/components/album-list/album-list.component";
import {AlbumComponent} from "./components/album/album.component";

const routes: Routes = [
  {path: '', redirectTo: 'how-it-works', pathMatch: 'full'},
  {path: 'how-it-works', component: HowItWorksComponent,},
  {path: 'mission', component: MissionComponent,},
  {path: 'about', component: AboutComponent},
  {path: 'contact', component: ContactComponent},
  {path: 'map', component: MapComponent},
  {path: 'albums', component: AlbumListComponent},
  {path: 'album/:albumId', component: AlbumComponent},
];


@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {
}

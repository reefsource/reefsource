import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';

import {HowItWorksComponent} from './components/how-it-works/how-it-works.component';
import {AboutComponent} from './components/about/about.component';
import {ContactComponent} from './components/contact/contact.component';
import {MapComponent} from './components/map/map.component';
import {MissionComponent} from './components/mission/mission.component';
import {AlbumListComponent} from 'app/components/album-list/album-list.component';
import {AlbumComponent} from './components/album/album.component';
import {PageNotFoundComponent} from './components/page-not-found/page-not-found.component';

import {AuthGuard} from './guards/auth.guard';

const routes: Routes = [
  {path: '', redirectTo: 'how-it-works', pathMatch: 'full'},
  {path: 'how-it-works', component: HowItWorksComponent,},
  {path: 'mission', component: MissionComponent,},
  {path: 'map', component: MapComponent},
  {path: 'about', component: AboutComponent},
  {path: 'contact', component: ContactComponent},
  {path: 'albums', component: AlbumListComponent, canActivate: [AuthGuard],},
  {path: 'album/:albumId', component: AlbumComponent, canActivate: [AuthGuard]},
  {path: '**', component: PageNotFoundComponent}
];


@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {
}

import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LoginComponent } from './pages/auth/login/login.component';
import { AllebuchungenComponent } from './pages/allebuchungen/allebuchungen.component';
import { SettingsComponent } from './pages/settings/settings.component';
import { AllegemeinsamebuchungenComponent } from './pages/allegemeinsamebuchungen/allegemeinsamebuchungen.component';
import { AddschnelleinstiegComponent } from './pages/addschnelleinstieg/addschnelleinstieg.component';
import {
  ADD_SCHNELLEINSTIEG_ROUTE,
  ALLE_EINZELBUCHUNGEN_ROUTE,
  ALLE_GEMEINSAME_BUCHUNGEN_ROUTE,
  LOGIN_OFFLINE_ROUTE,
  LOGIN_ROUTE,
  LOGOUT_ROUTE,
  ROOT_ROUTE,
  SETTINGS_ROUTE
} from './app-routes';
import { AuthGuard } from './pages/auth/auth.guard';
import { LogoutComponent } from './pages/auth/logout/logout.component';
import { OfflineLoginComponent } from './pages/offline-login/offline-login.component';


const routes: Routes = [
  {path: LOGIN_ROUTE, component: LoginComponent},
  {path: LOGOUT_ROUTE, component: LogoutComponent},
  {path: LOGIN_OFFLINE_ROUTE, component: OfflineLoginComponent},

  {path: ADD_SCHNELLEINSTIEG_ROUTE, component: AddschnelleinstiegComponent, canActivate: [AuthGuard]},
  {path: ALLE_EINZELBUCHUNGEN_ROUTE, component: AllebuchungenComponent, canActivate: [AuthGuard]},
  {path: ALLE_GEMEINSAME_BUCHUNGEN_ROUTE, component: AllegemeinsamebuchungenComponent, canActivate: [AuthGuard]},
  {path: SETTINGS_ROUTE, component: SettingsComponent, canActivate: [AuthGuard]},
  {path: ROOT_ROUTE, component: AddschnelleinstiegComponent, canActivate: [AuthGuard]}
];

@NgModule({
  imports: [RouterModule.forRoot(routes, {})],
  exports: [RouterModule]
})
export class AppRoutingModule {
}

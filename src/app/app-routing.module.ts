import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { LoginComponent } from './login/login.component';
import { ContactUsComponent } from './contact-us/contact-us.component';
import { MembersComponent } from './members/members.component';
import { EventsComponent } from './events/events.component';
import { OurVisionComponent } from './our-vision/our-vision.component';
import { RegisterComponent } from './register/register.component';


const routes: Routes = [

  { path: '', component: HomeComponent  },
  { path: 'login', component: LoginComponent },
  { path: 'contactus', component: ContactUsComponent },
  { path: 'members',component: MembersComponent },
  { path: 'events', component: EventsComponent},
  { path: 'ourvision',component: OurVisionComponent },
  { path: 'home',component: HomeComponent },
  { path: 'register', component: RegisterComponent}

];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }

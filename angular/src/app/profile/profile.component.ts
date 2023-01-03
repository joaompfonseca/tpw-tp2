import {Component, OnInit} from '@angular/core';
import {Profile} from "../../interfaces/profile";
import {PilotService} from "../../services/pilot/pilot.service";
import {DomSanitizer} from "@angular/platform-browser";
import {ProfileService} from "../../services/profile/profile.service";
import {TeamService} from "../../services/team/team.service";
import {UserService} from "../../services/user/user.service";
import {Router} from "@angular/router";

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.css']
})
export class ProfileComponent implements OnInit {

  profile: Profile | undefined;
  editing = false;
  emptyFields = false;

  constructor(
    private profileService: ProfileService,
    private pilotService: PilotService,
    private teamService: TeamService,
    private userService: UserService,
    private router: Router,
    private sanitizer: DomSanitizer
  ) {
  }

  ngOnInit() {
    this.getProfile();
  }

  getProfile() {
    this.profileService.getProfile().subscribe(profile => {
      this.profile = profile;
      this.getProfileImage();
      this.getPilotImages();
      this.getTeamImages();
    });
  }

  getProfileImage() {
    this.profileService.getProfileImage().subscribe(image => {
      if (image.type == 'text/html')
        this.profile!.image = 'assets/images/profile-default.jpg';
      else
        this.profile!.image = this.sanitizer.bypassSecurityTrustUrl(URL.createObjectURL(image));
    });
  }

  getPilotImages() {
    for (let p of this.profile!.favourite_pilot) {
      this.pilotService.getPilotImage(p.id).subscribe(
        image => {
          if (image.type == 'text/html')
            p.image = 'assets/images/pilot-default.jpg';
          else
            p.image = this.sanitizer.bypassSecurityTrustUrl(URL.createObjectURL(image));
        });
    }
  }

  getTeamImages() {
    for (let t of this.profile!.favourite_team) {
      this.teamService.getTeamImage(t.id).subscribe(
        image => {
          if (image.type == 'text/html')
            t.image = 'assets/images/team-default.jpg';
          else
            t.image = this.sanitizer.bypassSecurityTrustUrl(URL.createObjectURL(image));
        });
    }
  }

  edit() {
    this.editing = true;
  }

  save() {
    this.emptyFields = (this.profile!.user.first_name == ''
      || this.profile!.user.last_name == ''
      || this.profile!.user.email == ''
      || this.profile!.biography == '');

    if (!this.emptyFields) {
      this.profileService.updateProfile(this.profile!).subscribe(() => {
        this.editing = false;
      });
    }
  }

  logout() {
    this.userService.logout().subscribe(() => {
      this.router.navigate(['/']).then(() => window.location.reload());
    });
  }
}

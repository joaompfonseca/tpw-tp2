import {Component, OnInit} from '@angular/core';
import {User} from "../../interfaces/user";
import {ActivatedRoute} from "@angular/router";
import {UserService} from "../../services/user/user.service";
import {DomSanitizer, SafeUrl} from "@angular/platform-browser";
import {ProfileService} from "../../services/profile/profile.service";

@Component({
  selector: 'app-loginpartial',
  templateUrl: './loginpartial.component.html',
  styleUrls: ['./loginpartial.component.css']
})
export class LoginpartialComponent implements OnInit {
  user: User | undefined;
  image: SafeUrl | undefined;

  constructor(
    private route: ActivatedRoute,
    private userService: UserService,
    private profileService: ProfileService,
    private sanitizer: DomSanitizer
  ) { }

  ngOnInit() {
    this.getUser();
  }

  getUser() {
    this.userService.getUser().subscribe(user => {
      this.user = user
      this.getProfileImage();
    });
  }

  getProfileImage() {
    this.profileService.getProfileImage().subscribe(image => {
      if (image.type == 'text/html')
        this.image = 'assets/images/profile-default.jpg';
      else
        this.image = this.sanitizer.bypassSecurityTrustUrl(URL.createObjectURL(image));
    });
  }
}

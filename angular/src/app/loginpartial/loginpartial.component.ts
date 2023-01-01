import {Component, OnInit} from '@angular/core';
import {User} from "../../interfaces/user";
import {ActivatedRoute} from "@angular/router";
import {UserService} from "../../services/user/user.service";
import {DomSanitizer} from "@angular/platform-browser";

@Component({
  selector: 'app-loginpartial',
  templateUrl: './loginpartial.component.html',
  styleUrls: ['./loginpartial.component.css']
})
export class LoginpartialComponent implements OnInit {
  user: User | undefined;

  constructor(
    private route: ActivatedRoute,
    private userService: UserService,
    private sanitizer: DomSanitizer
  ) { }

  ngOnInit() {
    this.getUser();
  }

  getUser() {
    this.userService.getUser().subscribe(user => {
      this.user = user
      this.getUserImage();
    });
  }

  getUserImage() {
    this.userService.getUserImage().subscribe(image => {
      this.user!.image = this.sanitizer.bypassSecurityTrustUrl(URL.createObjectURL(image));
    });
  }
}

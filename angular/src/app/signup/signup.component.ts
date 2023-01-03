import { Component } from '@angular/core';
import {Router} from "@angular/router";
import {UserService} from "../../services/user/user.service";

@Component({
  selector: 'app-signup',
  templateUrl: './signup.component.html',
  styleUrls: ['./signup.component.css']
})
export class SignupComponent {

  username: string = '';
  email: string = '';
  password1: string = '';
  password2: string = '';
  emptyFields: boolean = false;
  diffPasswords: boolean = false;
  errors: boolean = false;

  constructor(
    private router: Router,
    private userService: UserService
  ) {
  }

  signup() {
    this.emptyFields = (this.username == '' || this.password1 == '' || this.password2 == '');
    this.diffPasswords = (this.password1 != this.password2);
    this.errors = false;

    if (!this.emptyFields && !this.diffPasswords) {
      this.userService.signup(this.username, this.email, this.password1).subscribe(
        () => this.router.navigate(['/profile']).then(() => window.location.reload()),
        () => this.errors = true
      );
    }
  }
}

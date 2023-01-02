import {Component} from '@angular/core';
import {UserService} from "../../services/user/user.service";
import {Router} from "@angular/router";

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {

  username: string = '';
  password: string = '';
  emptyFields: boolean = false;
  errors: boolean = false;

  constructor(
    private router: Router,
    private userService: UserService
  ) {
  }

  login() {
    this.emptyFields = (this.username == '' || this.password == '');
    this.errors = false;

    if (!this.emptyFields) {
      this.userService.login(this.username, this.password).subscribe(
        () => this.router.navigate(['/']).then(() => window.location.reload()),
        () => this.errors = true
      );
    }
  }
}

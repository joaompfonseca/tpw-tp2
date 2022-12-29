import {Component, OnInit} from '@angular/core';
import {User} from "../../interfaces/user";
import {Car} from "../../interfaces/car";

@Component({
  selector: 'app-car',
  templateUrl: './car.component.html',
  styleUrls: ['./car.component.css']
})
export class CarComponent implements OnInit {

  header: string;
  user: User;
  car: Car;

  constructor() {
    this.header = 'Car Details';
    this.user = {
      is_authenticated: true,
      is_superuser: true,
    };
    this.car = {
      id: 1,
      model: 'F40',
      engine: 'V8',
      weight: 1200,
      pilot: {
        id: 1,
        name: 'Lewis Hamilton',
        team: {
          id: 1,
          name: 'Mercedes',
        }
      }
    }
  }

  ngOnInit() {
  }

  getCar() {
  }
}

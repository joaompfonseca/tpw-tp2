import {Component, OnInit} from '@angular/core';
import {User} from "../../interfaces/user";
import {Car} from "../../interfaces/car";
import {CarService} from "../../services/car/car.service";
import {ActivatedRoute} from "@angular/router";

@Component({
  selector: 'app-car',
  templateUrl: './car.component.html',
  styleUrls: ['./car.component.css']
})
export class CarComponent implements OnInit {

  header: string;
  carId: number;
  user: User;
  car: Car;

  constructor(private route: ActivatedRoute,  private carService: CarService) {
    this.header = '';
    this.carId = 0;
    this.user = {
      is_authenticated: false,
      is_superuser: false,
    };
    this.car = {
      id: 0,
      model: '',
      engine: '',
      weight: 0,
      pilot: {
        id: 0,
        name: '',
        team: {
          id: 0,
          name: '',
        }
      }
    }
  }

  ngOnInit() {
    this.route.paramMap.subscribe(paramMap => {
      let id = paramMap.get('id');
      if (id !== null) {
        this.carId = +id;
      }
      this.getCar();
    })
  }

  getCar() {
    this.carService.getCar(this.carId).subscribe(data => {
      console.log(data);
      this.header = data.header.header;
      this.user = data.auth;
      this.car = data.car;
      this.car.pilot = data.pilot;
      this.car.pilot.team = data.team;
    });
  }
}

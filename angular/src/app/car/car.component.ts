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

  carId: number | undefined;

  header: string | undefined;
  user: User | undefined;
  car: Car | undefined;

  constructor(
    private route: ActivatedRoute,
    private carService: CarService
  ) {
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
    this.carService.getCar(this.carId!).subscribe(data => {
      this.header = data.header.header;
      this.user = data.auth;
      this.car = data.car;
      this.car!.pilot = data.pilot;
      this.car!.pilot.team = data.team;
    });
  }
}

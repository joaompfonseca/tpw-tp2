import { Injectable } from '@angular/core';
import {Car} from "../../interfaces/car"
import {Observable} from "rxjs";
import {HttpClient, HttpHeaders} from "@angular/common/http";

const httpOptions = {
  headers: new HttpHeaders({'Content-Type': 'application/json'})
};

@Injectable({
  providedIn: 'root'
})

export class CarService {
  private baseURL = 'http://localhost:8000/ws/';
  constructor(private http: HttpClient) { }

  getCar(id: number): Observable<Car> {
    const url = this.baseURL + "car?id=" + id;
    return this.http.get<Car>(url);
  }

  getCars(): Observable<Car[]> {
    const url = this.baseURL + "cars";
    return this.http.get<Car[]>(url);
  }

  createCar(car: Car): Observable<any> {
    const url = this.baseURL + "carcre";
    return this.http.post(url, car, httpOptions)
  }

  searchCar(model?: string, pilot?: string): Observable<Car[]> {
    if (model && pilot) {
      const url = this.baseURL + "carsearch?model=" + model + "&pilot=" + pilot;
      return this.http.get<Car[]>(url);
    }

    if (model && !pilot) {
      const url = this.baseURL + "carsearch?model=" + model;
      return this.http.get<Car[]>(url);
    }

    if (pilot && !model) {
      const url = this.baseURL + "carsearch?pilot=" + pilot;
      return this.http.get<Car[]>(url);
    }
    const url = this.baseURL + "carsearch?model=''&pilot=''";
    return this.http.get<Car[]>(url);
  }

  updateCar(id: number, car: Car): Observable<any>{
    const url = this.baseURL + "carupdate?id=" + id;
    return this.http.put(url, car, httpOptions);
  }

}

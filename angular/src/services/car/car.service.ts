import { Injectable } from '@angular/core';
import {Car} from "../../interfaces/car"
import {Observable} from "rxjs";
import {HttpClient, HttpHeaders} from "@angular/common/http";

const httpOptions = {
  headers: new HttpHeaders({'Content-Type': 'application/json'}),
  withCredentials: true
};

@Injectable({
  providedIn: 'root'
})

export class CarService {
  private baseURL = 'http://localhost:8000/ws/';
  constructor(private http: HttpClient) { }

  getCar(id: number): Observable<any> {
    const url = this.baseURL + "car?id=" + id;
    return this.http.get<any>(url, httpOptions);
  }

  getCars(): Observable<Car[]> {
    const url = this.baseURL + "cars";
    return this.http.get<Car[]>(url, httpOptions);
  }

  createCar(car: any): Observable<any> {
    const url = this.baseURL + "carcreate";
    return this.http.post(url, car, httpOptions)
  }

  searchCar(model?: string, pilot?: string): Observable<Car[]> {
    if (model && pilot) {
      const url = this.baseURL + "carsearch?model=" + model + "&pilot=" + pilot;
      return this.http.get<Car[]>(url, httpOptions);
    }

    if (model && !pilot) {
      const url = this.baseURL + "carsearch?model=" + model;
      return this.http.get<Car[]>(url, httpOptions);
    }

    if (pilot && !model) {
      const url = this.baseURL + "carsearch?pilot=" + pilot;
      return this.http.get<Car[]>(url, httpOptions);
    }
    const url = this.baseURL + "carsearch?model=''&pilot=''";
    return this.http.get<Car[]>(url, httpOptions);
  }

  updateCar(id: number, car: any): Observable<any>{
    const url = this.baseURL + "carupdate?id=" + id;
    return this.http.put(url, car, httpOptions);
  }

}

import { Injectable } from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {Observable} from "rxjs";
import {Home} from "../../interfaces/home";

@Injectable({
  providedIn: 'root'
})
export class HomeService {
  private baseURL = 'http://localhost:8000/ws/';
  constructor(private http: HttpClient) { }

  get(): Observable<Home> {
    const url = this.baseURL + "home";
    return this.http.get<Home>(url);
  }
}

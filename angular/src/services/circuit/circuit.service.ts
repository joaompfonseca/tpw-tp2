import { Injectable } from '@angular/core';
import {Circuit} from "../../interfaces/circuit"
import {Observable} from "rxjs";
import {HttpClient, HttpHeaders} from "@angular/common/http";


const httpOptions = {
  headers: new HttpHeaders({'Content-Type': 'application/json'})
};

@Injectable({
  providedIn: 'root'
})
export class CircuitService {
  private baseURL = 'http://localhost:8000/ws/';
  constructor(private http: HttpClient) { }

  getCircuit(id: number): Observable<any> {
    const url = this.baseURL + "circuit?id=" + id;
    return this.http.get<any>(url);
  }

  getCircuits(): Observable<Circuit[]> {
    const url = this.baseURL + "circuits";
    return this.http.get<Circuit[]>(url);
  }

  createCircuit(circuit: Circuit): Observable<any> {
    const url = this.baseURL + "circuitcre";
    return this.http.post(url, circuit, httpOptions)
  }

  searchCircuit(name: string): Observable<Circuit[]> {
    const url = this.baseURL + "circuitsearch?name=" + name;
    return this.http.get<Circuit[]>(url);
    }

  updateCircuit(id: number, circuit: Circuit): Observable<any>{
    const url = this.baseURL + "circuitupdate?id=" + id;
    return this.http.put(url, circuit, httpOptions);
  }

}

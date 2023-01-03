import { Injectable } from '@angular/core';
import {Circuit} from "../../interfaces/circuit"
import {Observable} from "rxjs";
import {HttpClient, HttpHeaders} from "@angular/common/http";


const httpOptions = {
  headers: new HttpHeaders({'Content-Type': 'application/json'}),
  withCredentials: true
};

@Injectable({
  providedIn: 'root'
})
export class CircuitService {
  private baseURL = 'http://localhost:8000/ws/';
  constructor(private http: HttpClient) { }

  getCircuit(id: number): Observable<any> {
    const url = this.baseURL + "circuit?id=" + id;
    return this.http.get<any>(url, httpOptions);
  }

  getCircuits(): Observable<Circuit[]> {
    const url = this.baseURL + "circuits";
    return this.http.get<Circuit[]>(url, httpOptions);
  }

  createCircuit(circuit: any): Observable<any> {
    const url = this.baseURL + "circuitcreate";
    return this.http.post(url, circuit, httpOptions)
  }

  searchCircuit(name: string): Observable<Circuit[]> {
    const url = this.baseURL + "circuitsearch?name=" + name;
    return this.http.get<Circuit[]>(url, httpOptions);
    }

  updateCircuit(id: number, circuit: any): Observable<any>{
    const url = this.baseURL + "circuitupdate?id=" + id;
    return this.http.put(url, circuit, httpOptions);
  }

}

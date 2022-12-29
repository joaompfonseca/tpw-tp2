import { Injectable } from '@angular/core';
import {Pilot} from "../../interfaces/pilot"
import {Observable} from "rxjs";
import {HttpClient, HttpHeaders} from "@angular/common/http";


const httpOptions = {
  headers: new HttpHeaders({'Content-Type': 'application/json'})
};

@Injectable({
  providedIn: 'root'
})
export class PilotService {
  private baseURL = 'http://localhost:8000/ws/';
  constructor(private http: HttpClient) { }

  getPilot(id: number): Observable<Pilot> {
    const url = this.baseURL + "pilot?id=" + id;
    return this.http.get<Pilot>(url);
  }

  getPilots(): Observable<Pilot[]> {
    const url = this.baseURL + "pilots";
    return this.http.get<Pilot[]>(url);
  }

  createPilot(pilot: Pilot): Observable<any> {
    const url = this.baseURL + "pilotcre";
    return this.http.post(url, pilot, httpOptions)
  }

  searchPilot(name: string): Observable<Pilot[]> {
    const url = this.baseURL + "pilotsearch?name=" + name;
    return this.http.get<Pilot[]>(url);
  }

  updatePilot(id: number, pilot: Pilot): Observable<any>{
    const url = this.baseURL + "pilotupdate?id=" + id;
    return this.http.put(url, pilot, httpOptions);
  }
}

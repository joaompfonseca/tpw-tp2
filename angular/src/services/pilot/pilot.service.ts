import {Injectable} from '@angular/core';
import {Pilot} from "../../interfaces/pilot"
import {Observable} from "rxjs";
import {HttpClient, HttpHeaders} from "@angular/common/http";


const httpOptions = {
  headers: new HttpHeaders({'Content-Type': 'application/json'}),
  withCredentials: true
};

@Injectable({
  providedIn: 'root'
})
export class PilotService {
  private baseURL = 'http://localhost:8000/ws/';

  constructor(private http: HttpClient) {
  }

  getPilot(id: number): Observable<any> {
    const url = this.baseURL + "pilot?id=" + id;
    return this.http.get<any>(url, httpOptions);
  }

  getPilotImage(id: number): Observable<Blob> {
    const url = this.baseURL + "image/pilot/" + id;
    return this.http.get(url, {...httpOptions, responseType: 'blob'});
  }

  getPilots(): Observable<Pilot[]> {
    const url = this.baseURL + "pilots";
    return this.http.get<Pilot[]>(url, httpOptions);
  }

  createPilot(pilot: any): Observable<any> {
    const url = this.baseURL + "pilotcreate";
    return this.http.post(url, pilot, httpOptions)
  }

  searchPilot(name: string): Observable<Pilot[]> {
    const url = this.baseURL + "pilotsearch?name=" + name;
    return this.http.get<Pilot[]>(url, httpOptions);
  }

  updatePilot(id: number, pilot: any): Observable<any> {
    const url = this.baseURL + "pilotupdate?id=" + id;
    return this.http.put(url, pilot, httpOptions);
  }
}

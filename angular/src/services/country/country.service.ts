import { Injectable } from '@angular/core';
import {Country} from "../../interfaces/country"
import {Observable} from "rxjs";
import {HttpClient, HttpHeaders} from "@angular/common/http";


const httpOptions = {
  headers: new HttpHeaders({'Content-Type': 'application/json'})
};

@Injectable({
  providedIn: 'root'
})
export class CountryService {
  private baseURL = 'http://localhost:8000/ws/';
  constructor(private http: HttpClient) { }

  getCountry(id: number): Observable<Country> {
    const url = this.baseURL + "country?id=" + id;
    return this.http.get<Country>(url);
  }

  getCountries(): Observable<Country[]> {
    const url = this.baseURL + "countries";
    return this.http.get<Country[]>(url);
  }

  createCountry(country: Country): Observable<any> {
    const url = this.baseURL + "countrycre";
    return this.http.post(url, country, httpOptions)
  }

  searchCountry(name: string): Observable<Country[]> {
    const url = this.baseURL + "countrysearch?name=" + name;
    return this.http.get<Country[]>(url);
  }

  updateCountry(id: number, country: Country): Observable<any>{
    const url = this.baseURL + "countryupdate?id=" + id;
    return this.http.put(url, country, httpOptions);
  }

}

import { Injectable } from '@angular/core';
import {Result} from "../../interfaces/result"
import {Observable} from "rxjs";
import {HttpClient, HttpHeaders} from "@angular/common/http";

const httpOptions = {
  headers: new HttpHeaders({'Content-Type': 'application/json'})
};

@Injectable({
  providedIn: 'root'
})
export class ResultService {
  private baseURL = 'http://localhost:8000/ws/';
  constructor(private http: HttpClient) { }

  getResult(id: number): Observable<Result> {
    const url = this.baseURL + "result?id=" + id;
    return this.http.get<Result>(url);
  }

  createResult(result: Result): Observable<any> {
    const url = this.baseURL + "resultcre";
    return this.http.post(url, result, httpOptions)
  }

  updateResult(id: number, result: Result): Observable<any>{
    const url = this.baseURL + "resultupdate?id=" + id;
    return this.http.put(url, result, httpOptions);
  }

}



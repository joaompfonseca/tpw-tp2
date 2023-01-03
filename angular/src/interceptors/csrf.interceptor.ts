import {Injectable} from '@angular/core';
import {HttpRequest, HttpHandler, HttpInterceptor} from '@angular/common/http';
import {Observable} from "rxjs";

@Injectable()
export class CsrfInterceptor implements HttpInterceptor {

  intercept(req: HttpRequest<any>, next: HttpHandler) {
    // Retrieve the CSRF token from a cookie or from local storage
    const csrfToken = this.getCsrfToken();

    // Clone the request and add the CSRF token to the headers
    const modifiedReq = req.clone({
      headers: req.headers.set('X-CSRFToken', csrfToken)
    });

    // Return the modified request
    return next.handle(modifiedReq);
  }

  getCsrfToken(): string {
    // Try to retrieve the CSRF token from a cookie
    const csrfCookie = this.getCookie('csrftoken');

    if (csrfCookie) {
      return csrfCookie;
    }

    // If the CSRF token is not in a cookie, try to retrieve it from local storage
    const csrfToken = localStorage.getItem('csrftoken');
    if (csrfToken) {
      return csrfToken;
    }

    // If the CSRF token is not in a cookie or in local storage, return an empty string
    return '';
  }

  getCookie(name: string): string {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) {
      // @ts-ignore
      return parts.pop().split(';').shift();
    }
    return '';
  }
}



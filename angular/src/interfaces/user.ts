import {SafeUrl} from "@angular/platform-browser";

export interface User {
  id: number;
  username: string
  email: string;
  is_authenticated: boolean
  is_superuser: boolean
  image?: SafeUrl
}

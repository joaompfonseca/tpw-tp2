export interface User {
  id: number;
  username: string;
  first_name: string;
  last_name: string;
  email: string;
  is_authenticated: boolean;
  is_superuser: boolean;
}

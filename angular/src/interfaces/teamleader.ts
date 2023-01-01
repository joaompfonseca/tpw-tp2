import {Team} from "./team";
import {SafeUrl} from "@angular/platform-browser";

export interface TeamLeader {
  id: number
  name: string
  team?: Team
  image?: SafeUrl
}

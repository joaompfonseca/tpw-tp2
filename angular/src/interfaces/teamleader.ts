import {Team} from "./team";

export interface TeamLeader {
  id: number
  name: string
  team?: Team
  image: string
}

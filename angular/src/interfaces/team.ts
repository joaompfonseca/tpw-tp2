import {TeamLeader} from "./teamleader";

export interface Team {
  id: number
  name: string
  date?: Date
  championships?: number
  points?: number
  image?: string
  teamleader?: TeamLeader
}

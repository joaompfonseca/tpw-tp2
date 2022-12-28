import {Pilot} from "./pilot";

export interface Car {
  id: number
  model: string
  engine: string
  weight: number
  pilot: Pilot
}

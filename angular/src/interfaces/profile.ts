import {Pilot} from "./pilot";
import {Team} from "./team";
import {User} from "./user";

export interface Profile {
  id: number
  user: User
  profile_image: string
  favourite_pilot: Pilot[]
  favourite_team: Team[]
}

import { TestBed } from '@angular/core/testing';

import { TeamLeaderService } from './team-leader.service';

describe('TeamLeaderService', () => {
  let service: TeamLeaderService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(TeamLeaderService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});

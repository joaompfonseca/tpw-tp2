import { ComponentFixture, TestBed } from '@angular/core/testing';

import { LoginpartialComponent } from './loginpartial.component';

describe('LoginpartialComponent', () => {
  let component: LoginpartialComponent;
  let fixture: ComponentFixture<LoginpartialComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ LoginpartialComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(LoginpartialComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

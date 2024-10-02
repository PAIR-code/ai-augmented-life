import {ComponentFixture, TestBed} from '@angular/core/testing';

import {CoordinationGameComponent} from './coordination-game.component';

describe('CoordinationGameComponent', () => {
  let component: CoordinationGameComponent;
  let fixture: ComponentFixture<CoordinationGameComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CoordinationGameComponent],
    }).compileComponents();

    fixture = TestBed.createComponent(CoordinationGameComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

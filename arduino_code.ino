#include <Stepper.h>

// initialize the stepper library on pins 8 through 11:
Stepper myStepper(200, 8, 9, 10, 11);

int sensor_pin = A0;
int threshold = 840; // threshold to differentiate black and white
int total_steps_taken = 0;
int sensor_value;
int width;

void setup() {
  // set the speed at 60 rpm:
  myStepper.setSpeed(30);
  Serial.begin(9600);
}

int calc_width() {
  // count the number of step until the next white
  int count = 1;
  while(sensor_value < threshold) {
    myStepper.step(1);
    total_steps_taken += 1;
    delay(100);
    sensor_value = analogRead(sensor_pin);
    count++;
  }

  return count;
}


void loop() {
//  myStepper.step(1);
//  count++;
//  Serial.println(count);
//  delay(200);
//  
  sensor_value = analogRead(sensor_pin);
  Serial.println(sensor_value);
  delay(500);
//  myStepper.step(2);


  // keep moving until black is detected
  while(sensor_value < threshold) {
    myStepper.step(2);
    total_steps_taken += 2;
    delay(500);
    sensor_value = analogRead(sensor_pin);
    Serial.println(sensor_value);
  }

  width = calc_width();

  // now the value of width is the number of steps to cover a single black strip

  int count = 0;

  // take reading after every "width" number of steps
  Serial.println("start");
  while(1) {
    myStepper.step(width);
    total_steps_taken += width;
    count++;
    sensor_value = analogRead(sensor_pin);
    if (sensor_value < threshold) {
      Serial.println("0");
    }
    else {
      Serial.println("1");
    }
    delay(500);

//    if (count == 88) {
//      Serial.println("stop");
//      break;
//    }
  }
}

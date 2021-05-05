//M1
const int m1 = A2;
const int s1 =  A3;
//M2
const int m2 =  2;
const int s2_oben =  3;
const int s2_unten =  4;
//M3
const int m3 =  5;
const int s3_oben =  6;
const int s3_unten =  7;
//M4
const int m4 =  8;
const int s4_oben =  9;
const int s4_unten =  10;
//M5
const int m5_right =  11;
const int m5_left =  12;
const int s5_oben =  13;
const int s5_unten =  A1;
//M6
const int m6 =  A4;
const int s6_oben =  A5; 
const int s6_unten =  A6;

//Global vars
int color_before = 0;

void setup() {
  //M1
  pinMode(m1, OUTPUT);
  pinMode(s1, INPUT);
  //M2
  pinMode(m2, OUTPUT);
  pinMode(s2_oben, INPUT);
  pinMode(s2_unten, INPUT);
  //M3
  pinMode(m3, OUTPUT);
  pinMode(s3_oben, INPUT);
  pinMode(s3_unten, INPUT);
  //M4
  pinMode(m4, OUTPUT);
  pinMode(s4_oben, INPUT);
  pinMode(s4_unten, INPUT);
  //M5
  pinMode(m5_right, OUTPUT);
  pinMode(m5_left, OUTPUT);
  pinMode(s5_oben, INPUT);
  pinMode(s5_unten, INPUT);
  //M6
  pinMode(m6, OUTPUT);
  pinMode(s6_oben, INPUT);
  pinMode(s6_unten, INPUT);
}

void loop() {
  printColor(2);
  delay(10000);
}

void waitForSensor(int buttonPin){
  int buttonState = 0;
  while(1){
    buttonState = digitalRead(buttonPin);
    if (buttonState == HIGH) {
      return;
    }
  }
}

void adjustMotor(int sensor, int motor){
  digitalWrite(motor, HIGH);
  waitForSensor(sensor);
  digitalWrite(motor, LOW);
  return;
}

void checkPosition(){
  adjustMotor(s1, m1);
  adjustMotor(s2_unten, m2);
  adjustMotor(s4_unten, m4);
  adjustMotor(s3_unten, m3);
  return;
}

void moveHead_Left(int count){
  for (int i = 0; i <= count; i++) {
    digitalWrite(m5_left, HIGH);
    delay(0.2);
    adjustMotor(15, 14);
  }
}

void moveHead_Right(int count){
  for (int i = 0; i <= count; i++) {
    digitalWrite(m5_right, HIGH);
    delay(0.2);
    adjustMotor(15, 13);
  }
}

void changeColor(int color){
  int diff = color - color_before;
  if(diff > 0){
    moveHead_Left(diff);
  } else if(diff < 0){
    moveHead_Right(diff);
  }
  color_before = color;
  return;
}

void printColor(int color){
  checkPosition();
  changeColor(2);
  return;
}

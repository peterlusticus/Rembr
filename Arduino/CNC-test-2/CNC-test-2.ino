//Ohne "ReadLines"-Library

#include <SPI.h>
#include <SD.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

//X-Axis
const int xdir = A2;
const int xpul = A1;
const int xena = A3;
//Y-Axis
const int ydir = A7;
const int ypul = 9;
const int yena = 10;
//M1
const int m1 = 13;
const int s1 =  2;

//Global vars
bool dir_left = HIGH;
bool dir_right = LOW;
File gcode;

void setup() {
  Serial.begin(9600);
  //X-Axis
  pinMode(xdir, OUTPUT);
  pinMode(xpul, OUTPUT);
  pinMode(xena, OUTPUT);
  //Y-Axis
  pinMode(ydir, OUTPUT);
  pinMode(ypul, OUTPUT);
  pinMode(yena, OUTPUT);
  //M1
  pinMode(m1, OUTPUT);
  pinMode(s1, INPUT);
  //Configure SD-Card
  Serial.print("Initializing SD card...");

  if (!SD.begin(4)) {
    Serial.println("initialization failed!");
    while (1);
  }
  Serial.println("initialization done.");
}

void loop() {
  Serial.println("[start]");
  //analogWrite(m1, 127); //255 is 100%
  lifr();
  //analogWrite(m1, 0);
  Serial.println("[end]");
  delay(100000);
}





int OpenFile(char Filename[]) {
  gcode = SD.open(Filename, FILE_WRITE);
  gcode = SD.open(Filename, FILE_READ);
  delay(500);
  if (gcode)
  {
    Serial.println("[SD]: file is open");
    return;
  } else {
    Serial.println("[SD]: error opening file");
    delay(100000);
  }
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

void lifr() {
  OpenFile("sample.txt");
    float x_before = 0;
    float y_before = 0;
  while (gcode.available()) {
    String line = gcode.readStringUntil('\r');
    if ((line.indexOf("X") > 0) && (line.indexOf("Y") > 0)) {
      line = line.substring(4);
      int y_idx = line.indexOf("Y");
      String Gx = line.substring(1,y_idx);
      String Gy = line.substring(y_idx+1);
      float x = (Gx.toFloat())*100;
      float y = (Gy.toFloat())*100;
      float x_steps = x - x_before;
      float y_steps = y - y_before + 10000;
      x_before = x;
      y_before = y;
      //waitForSensor(s1);
      Serial.println(String(round(x_steps)));
      Serial.println(String(round(y_steps)));
      jog(1, round(x_steps/100));
      jog(2, round(y_steps/100));
      delay(5000);
    }
  }
}

void jog(int axis, int delta) {
  if (delta > 0) {
    if (axis == 1) {
      x(abs(delta), 0);
    }
    if (axis == 2) {
      y(abs(delta), 0);
    }
  }
  if (delta < 0) {
    if (axis == 1) {
      x(0, abs(delta));
    }
    if (axis == 2) {
      y(0, abs(delta));
    }
  }
  return;
}

void x(int Fsteps, int Bsteps) {
  Serial.println("[X] forward: " + String(Fsteps) + "\tbackward: " + String(Bsteps));
  digitalWrite(xena, HIGH);
  for (int i = 0; i < Fsteps; i++) {
    xstep(dir_left);
  }
  for (int i = 0; i < Bsteps; i++) {
    xstep(dir_right);
  }
  return;
}

void y(int Fsteps, int Bsteps) {
  Serial.println("[Y] forward: " + String(Fsteps) + "\tbackward: " + String(Bsteps));
  digitalWrite(yena, HIGH);
  for (int i = 0; i < Fsteps; i++) {
    ystep(dir_left);
  }
  for (int i = 0; i < Bsteps; i++) {
    ystep(dir_right);
  }
  return;
}

void xstep(bool dir) {
  Serial.println("X-STEP");
  digitalWrite(xdir, dir);
  digitalWrite(xpul, HIGH);
  delay(9);
  digitalWrite(xpul, LOW);
  delay(9);
  Serial.println("X-STEP END");
  return;
}

void ystep(bool dir) {
  Serial.println("Y-STEP");
  digitalWrite(ydir, dir);
  digitalWrite(ypul, HIGH);
  delay(9);
  digitalWrite(ypul, LOW);
  delay(9);
  return;
}

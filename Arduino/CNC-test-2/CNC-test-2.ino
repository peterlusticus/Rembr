//Ohne "ReadLines"-Library

#include <SPI.h>
#include <SD.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

//X-Axis
const int xdir = 2;
const int xpul = 3;
const int xena = 4;
//Y-Axis
const int ydir = 5;
const int ypul = 6;
const int yena = 7;
//M1
const int m1 = 8;
const int s1 =  9;

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
  while (!SD.begin()) {
    Serial.println("[SD]: initialization failed");
    delay(10000);
  }
}

void loop() {
  Serial.println("[start]");
  analogWrite(m1, 127); //255 is 100%
  lifr();
  analogWrite(m1, 0);
  Serial.println("[end]");
  delay(100000);
}

void xstep(bool dir) {
  digitalWrite(xdir, dir);
  digitalWrite(xpul, HIGH);
  delay(9);
  digitalWrite(xpul, LOW);
  delay(9);
  return;
}

void ystep(bool dir) {
  digitalWrite(ydir, dir);
  digitalWrite(ypul, HIGH);
  delay(9);
  digitalWrite(ypul, LOW);
  delay(9);
  return;
}

void x(int Fsteps, int Bsteps) {
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
  digitalWrite(yena, HIGH);
  for (int i = 0; i < Fsteps; i++) {
    ystep(dir_left);
  }
  for (int i = 0; i < Bsteps; i++) {
    ystep(dir_right);
  }
  return;
}

void jog(char axis, int delta) {
  if (delta > 0) {
    if (axis == "X") {
      x(abs(delta), 0);
    }
    if (axis == "Y") {
      y(abs(delta), 0);
    }
  }
  if (delta < 0) {
    if (axis == "X") {
      x(0, abs(delta));
    }
    if (axis == "Y") {
      y(0, abs(delta));
    }
  }
  return;
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
  while (gcode.available()) {
    String line = gcode.readStringUntil('\r');
    if ((line.substring(0) == "X") && (line.substring(0) == "Y")) {
      int len = line.length() + 1; 
      char coordinates[len];
      line.toCharArray(coordinates,len);
      char * Gx = strtok(coordinates, " ");
      char * Gy = strtok(NULL, " ");
      Gx = strtok(Gx, "X");
      Gy = strtok(Gx, "Y");
      float x = atof(Gx);
      float y = atof(Gy);
      Serial.println("X-Steps: " + String((int)x * 10));
      Serial.println("Y-Steps: " + String((int)y * 10));
      waitForSensor(s1);
      jog("X", (int)x * 10);
      jog("Y", (int)y * 10);
    }
  }
}

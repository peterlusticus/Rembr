#include <SPI.h>
#include <SD.h>
#include <ReadLines.h>
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
char line1[RL_MAX_CHARS];


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
     Serial.println("initialization failed!");
     delay(10000);
  }
}

void loop() {
  lifr();
}

void xstep(dir){
  digitalWrite(xdir, dir);
  digitalWrite(xpul, HIGH);
  delay(9);  
  digitalWrite(xpul, LOW);
  delay(9);  
}

void ystep(dir){
  digitalWrite(ydir, dir);
  digitalWrite(ypul, HIGH);
  delay(9);  
  digitalWrite(ypul, LOW);
  delay(9);  
}

void x(int Fsteps, int Bsteps){
  digitalWrite(xena, HIGH);
  for(i, i<Fsteps, i++){
    xstep(dir_left);
  }
   for(i, i<Bsteps, i++){
    xstep(dir_right);
  }
}

void y(int Fsteps, int Bsteps){
  digitalWrite(yena, HIGH);
  for(i, i<Fsteps, i++){
    ystep(dir_left);
  }
   for(i, i<Bsteps, i++){
    ystep(dir_right);
  }
}

void jog(char axis, int delta){
  if(delta > 0){
    if(axis == "X"){
      x(abs(delta), 0)
    }
    if(axis == "Y"){
      y(abs(delta), 0)
    }
  }
  if(delta < 0){
    if(axis == "X"){
      x(0, abs(delta))
    }
    if(axis == "Y"){
      y(0, abs(delta))
    }
  }
}

void lifr(){
    RL.readLines("sample.txt", [](char* line, int index) {
        Serial.println(String(index) + ":  " + String(line));
        if ((String(line).substring(0) == "X") && (String(line).substring(0) == "Y")) {
            char * Gx = strtok(line," ");
            char * Gy = strtok(NULL," ");
            Gx = strtok(Gx,"X");
            Gy = strtok(Gx,"Y");
            //Try This:
            float x = (float)Gx;
            float y = (float)Gy;
            //Or This:
            //String x = String(Gx);
            //String y = String(Gy);
            //float xSteps = x.toFloat();
            //float ySteps = y.toFloat();

            //TODO: wait for btn press
            jog("X",(int)x*10);
            jog("Y",(int)y*10);
        }
    });
}

#include <SPI.h>
#include <SD.h>

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


//------------------------------------------SETUP------------------------------------------
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
  Serial.print("[setup]\t initializing SD card");

  if (!SD.begin(4)) {
    Serial.println("[setup]\t initialization failed!");
    while (1);
  }
  Serial.println("[setup]\t initialization done");
}

void loop() {
  Serial.println("[loop]\t start");
  //analogWrite(m1, 127); //255 is 100%
  lifr();
  //analogWrite(m1, 0);
  Serial.println("[loop]\t end");
  exit(0)
}



//--------------------------------------CNC FUNCTIONS--------------------------------------
void lifr() {
  OpenFile("sample.txt");
    float x_before = 0;
    float y_before = 0;
  while (gcode.available()) {
    String line = gcode.readStringUntil('\r');
    if ((line.indexOf("X") > 0) && (line.indexOf("Y") > 0)) {
      line = line.substring(line.indexOf("X"));
      String Gx = line.substring(1,line.indexOf("Y"));
      String Gy = line.substring(line.indexOf("Y")+1,line.indexOf("F"));
	  Serial.println("[lifr]\t Gx: " + Gx + "   Gy: " + Gy);
      float x = (Gx.toFloat())*100);
      float y = ((Gy.toFloat())*100);
      int x_steps = round((x - x_before)/100);
      int y_steps = round((x - x_before)/100);
      x_before = x;
      y_before = y;
	  Serial.println("[lifr]\t x-steps: " + String(x_steps));
      Serial.println("[lifr]\t y-steps: " + String(y_steps));
      //waitForSensor(s1);
      jog(1, x_steps); //1 for x
      jog(2, y_steps); //2 for y
      delay(1);
    }
  }
}

int OpenFile(char Filename[]) {
  gcode = SD.open(Filename, FILE_WRITE);
  gcode = SD.open(Filename, FILE_READ);
  delay(500);
  if (gcode)
  {
    Serial.println("[OpenFile]\t file is open");
    return;
  } else {
    Serial.println("[OpenFile]\t error opening file!");
    exit(0)
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

void jog(int axis, int delta) {
	Serial.println("[jog]\t steps: " + String(abs(delta)));
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
  Serial.println("[x]\t Fsteps: " + String(Fsteps) + "\t Bsteps: " + String(Bsteps));
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
  Serial.println("[y]\t Fsteps: " + String(Fsteps) + "\t Bsteps: " + String(Bsteps));
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
  Serial.println("[xstep]\t step");
  digitalWrite(xdir, dir);
  digitalWrite(xpul, HIGH);
  delay(9);
  digitalWrite(xpul, LOW);
  delay(9);
  return;
}

void ystep(bool dir) {
  Serial.println("[ystep]\t step");
  digitalWrite(ydir, dir);
  digitalWrite(ypul, HIGH);
  delay(9);
  digitalWrite(ypul, LOW);
  delay(9);
  return;
}

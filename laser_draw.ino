#include <Stepper.h>
#include <SPI.h>
#include <SD.h>

// Stepper Motor Info
const int stepsPerRevolution = 32;
Stepper xStepper(stepsPerRevolution, 6, 8, 7, 9);
Stepper yStepper(stepsPerRevolution, 2, 4, 3, 5);
const float StepInc = 1;
const float stepsPerDegree = 5.689;
const byte speed = 50;

// Starting Angles
const float X0 = 90;  // left/right angle
const float Y0 = 90;  // up/down angle

// Current Angles
float X = X0;
float Y = Y0;

// Upcoming Angles
float nextX, nextY;

// SD & File Stuff
const byte csPin = 10;
char fileName[] = "code.txt";

// Laser Pin
const byte laserPin = A0;

// Input Serial Timing
unsigned long timer = 0;
unsigned int timeout = 10000;

File codeFile;

void setup() {
  pinMode(laserPin, OUTPUT); // laser pin (using an analog input as a digital output)

  Serial.begin(9600); // Start Serial Communication

  Serial.print("Loading SD card... ");
  if (!SD.begin(csPin)) {
    Serial.println("Error!");
    while (1) {
      Serial.println("WHOOPS!");
      delay(1000);
    }
  }
  Serial.println("Done.");

  codeFile = SD.open(fileName);

  // file doesn't exist, wait for transmission
  if (!codeFile) {
    Serial.println("No file, waiting for serial transmission...");
    while (!Serial.available()) {} // wait until serial begins
    // once transmission begins, start timer
    timer = millis();
    while (abs(millis() - timer) < timeout) { // less than "timeout" milliseconds passed
      if (Serial.available()) {
        codeFile = SD.open(fileName, FILE_WRITE);
        timer = millis(); // reset timer
        codeFile.print(Serial.readString());
        Serial.println("Line written");
        codeFile.close();
      }
    }
  }

  codeFile = SD.open(fileName);

  Serial.print("Home: ");
  Serial.print(X);
  Serial.print(", ");
  Serial.println(Y);

  // Set the stepper motor speeds
  xStepper.setSpeed(speed);
  yStepper.setSpeed(speed);

  delay(2000);

  if (codeFile) {   // file opened successfully
    while (codeFile.available()) {
      String line = "";
      while (codeFile.peek() != '\n') // read until the end of the line
        line.concat(char(codeFile.read()));

      codeFile.read();  // flush the new-line character

      if (line.charAt(0) == 'X') { // Movement Instruction
        nextX = line.substring(line.indexOf('X') + 1, line.indexOf('Y')).toFloat();
        nextY = line.substring(line.indexOf('Y') + 1).toFloat();
        moveTo(nextX, nextY);
      }
      else if (line.charAt(0) == 'P') { // Laser on/off command
        if (line.charAt(1) == '0') { // Laser off
          Serial.println("Laser OFF");
          digitalWrite(laserPin, LOW);
        }
        else if (line.charAt(1) == '1') { // Laser on
          Serial.println("Laser ON");
          digitalWrite(laserPin, HIGH);
        }
      }
      else if (line.charAt(0) == 'D') { // Delete file after drawing
        codeFile.close();
        SD.remove(fileName);
        Serial.println("File deleted.");
        moveTo(X0, Y0);
        freewheel();
        while(1){}
      }
      else {
        Serial.print("Unknown command");
      }
    }
    codeFile.close();
  }
  else {
    Serial.println("Error opening instruction file!");
    while (1) {
    }
  }

  moveTo(X0, Y0); // home
  freewheel();    // disable holding torque
}

void loop()
{

}

// Move to specified angles (a, b)
void moveTo(float a, float b) {
  Serial.print("Going to ");
  Serial.print(a);
  Serial.print(", ");
  Serial.println(b);
  //  Convert angle to steps
  float a0 = X;
  float b0 = Y;

  //  Change in angle
  long da = abs(a * stepsPerDegree - a0 * stepsPerDegree);
  long db = abs(b * stepsPerDegree - b0 * stepsPerDegree);
  // Set direction +/-
  int sa = a0 < a ? StepInc : -StepInc;
  int sb = b0 < b ? StepInc : -StepInc;

  unsigned long i;
  long over = 0;

  if (da > db) {
    for (i = 0; i < da; ++i) {
      xStepper.step(sa);
      over += db;
      if (over >= da) {
        over -= da;
        yStepper.step(sb);
      }
    }
  }
  else {
    for (i = 0; i < db; ++i) {
      yStepper.step(sb);
      over += da;
      if (over >= db) {
        over -= db;
        xStepper.step(sa);
      }
    }
  }

  //  Update the positions
  X = a;
  Y = b;
}

void freewheel() {
  for (byte i = 2; i <= 9; i++)
    digitalWrite(i, LOW);
  Serial.println("Holding torque disabled");
}


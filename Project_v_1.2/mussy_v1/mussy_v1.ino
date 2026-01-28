#include "9_axis.h"
#include "WiFi_ESP32.h"
#include "motorMovement.h"
#include <math.h>
float alt;
float az;
float initial_alt;
float initial_az;
float current_alt;
float current_az;
float delta_alt; //will depend on step and gear ratio
float delta_az;  //will depend on step and gear ratio
float step_size = 1.8/16;

void calibrate(){
  startAltAz starter = getStartAltAz();
  Serial.println("CALIBRATING");
  while(starter.command != "stop"){
    starter = getStartAltAz();
    Serial.println(starter.command);
    if(starter.command == "w"){
      if(starter.speed == "f"){
        moveUp();
        moveUp();
        moveUp();
        moveUp();
        moveUp();
        moveUp();
      }
      moveUp();
    }
    else if(starter.command == "a"){
      if(starter.speed == "f"){
        moveLeft();
        moveLeft();
        moveLeft();
        moveLeft();
        moveLeft();
        moveLeft();
      }
      moveLeft();
    }
    else if(starter.command == "s"){
      if(starter.speed == "f"){
        moveDown();
        moveDown();
        moveDown();
        moveDown();
        moveDown();
        moveDown();
      }
      moveDown();
    }
    else if(starter.command == "d"){
      if(starter.speed == "f"){
        moveRight();
        moveRight();
        moveRight();
        moveRight();
        moveRight();
        moveRight();
      }
      moveRight();    
    }
  }
  initial_alt = starter.alt;
  initial_az = starter.az;
  current_alt = initial_alt;
  current_az = initial_az;
}

void setup(){
  Serial.begin(115200);
  //setupSensors();
  setupWiFi();
  //dec_mag = getMagDec();
  while(!clientConnected()){
    delay(10);
  }
  setupMotor();
  calibrate();
  Serial.println("Everything has been set up :3");
  delay(3000);
  
}

void loop(){
  //Orientation o = getOrientation();//these might need to be modified based on mechanical setup
  //roll = o.roll;
  //pitch = o.pitch;
  //heading = o.heading;
  //heading += dec_mag;
  AltAz c = getAltAz();
  float alt = c.alt;
  float az = c.az;

  delta_alt = alt - current_alt;
  delta_az = az - current_az; 
  delta_az *= 10; // GEAR RATIO
  delta_alt *= 10;

  if(alt <= 0){
    alt = 0;
    delta_alt = 0;
  }
  while (abs(delta_az) > step_size){ // GEAR RATIO 10-1
    if(delta_az >= 0){
      moveRight();
      delta_az -= step_size;
    } 
    else if(delta_az < 0){
      moveLeft();
      delta_az += step_size;
    }
    current_az = (10*az - delta_az)/10;
    Serial.printf("Current Azimuth: %.2f\n", current_az);
  }
  while (abs(delta_alt) > 1.8/16){   //GEAR RATIO 1-10
    if(delta_alt >= 0){
      moveUp();
      delta_alt -= step_size; 
    }
    else if(delta_alt < 0){
      moveDown();
      delta_alt += step_size;
    }
    current_alt = (10*alt - delta_alt)/10;
    Serial.printf("Current Altitude: %.2f\n", current_alt);
  }
  Serial.printf("Current Altitude: %.2f, Current Azimuth: %.2f\n", current_alt, current_az);

  delay(50);
}

#include "9_axis.h"
#include "WiFi_ESP32.h"
#include "motorMovement.h"
#include <math.h>
float roll;
float pitch;
float heading;
float alt;
float az;
float initial_alt;
float initial_az;
float current_alt;
float current_az;
float delta_alt; //will depend on step and gear ratio
float delta_az;  //will depend on step and gear ratio
float step_size = 1.8/32;
/*
float P_alt = 0;
float I_alt = 0;
float D_alt = 0;
float P_az = 0;
float I_az = 0;
float D_az = 0;
double kp = 0.56;    // Proportional gain
double ki = 0.0027;  // Integral gain
double kd = 0;  
float error_alt = 0;
float error_az = 0;
float previousError_alt = 0;
float previousError_az = 0;
*/
float dec_mag;
/*
struct PIDResult {
  double delay_alt;
  double delay_az;
  double speed_alt;
  double speed_az;
};
*/
void calibrate(){
  AltAz start = getStartAltAz();
  initial_alt = start.alt;
  initial_az = start.az;
  current_alt = initial_alt;
  current_az = initial_az;
}
/*
PIDResult PID(float alt, float az, float pitch, float heading){
  error_alt = alt - pitch;
  error_az = az - heading; 
  Serial.printf("error_alt = : %.2f, error_az = : %.2f\n", error_alt, error_az);
  P_alt = error_alt;
  D_alt = error_alt - previousError_alt;
  I_alt += error_alt; 
  P_az = error_az;
  D_az = error_az - previousError_az;
  I_az += error_az; 
  previousError_alt = error_alt;
  previousError_az = error_az;
  double speedChange_alt = (P_alt * kp + I_alt * ki + D_alt * kd);
  double speedChange_az = (P_az * kp + I_az * ki + D_az * kd);
  double delay_motor_alt = max(20.0, 800 - 9*abs(speedChange_alt)); // adjust 100 as base delay
  double delay_motor_az  = max(20.0, 800 - 9*abs(speedChange_az));
  Serial.printf("speed_alt = : %.2f, speed_az = : %.2f\n", speedChange_alt, speedChange_az);
  Serial.printf("delay_alt = : %.2f, delay_az = : %.2f\n", delay_motor_alt, delay_motor_az);
  return {delay_motor_alt, delay_motor_az, speedChange_alt, speedChange_az};

}
*/
void setup(){
  Serial.begin(115200);
  //setupSensors();
  setupWiFi();
  //dec_mag = getMagDec();
  while(!clientConnected()){
    delay(10);
  }
  calibrate();
  setupMotor();
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
  delta_az *= 10;
  delta_alt *= 3;

  if(alt <= 0){
    alt = 0;
    delta_alt = 0;
  }
  while (abs(delta_az) > step_size){ // GEAR RATIO 10-1
    move(delta_az, 1);
    float step = -1.0 * step_size;
    if(delta_az < 0){
      step = step_size;
    }
    delta_az += step;
    current_az = (10*az - delta_az)/10;
    Serial.printf("Current Azimuth: %.2f\n", current_az);
  }
  while (abs(delta_alt) > 1.8/32){   //GEAR RATIO 1-1
    move(delta_alt, 0);
    float step = -1.0 * step_size;
    if(delta_alt < 0){
      step = step_size;
    }
    delta_alt += step;
    current_alt = (3*alt - delta_alt)/3;
    Serial.printf("Current Altitude: %.2f\n", current_alt);
  }
  Serial.printf("Current Altitude: %.2f, Current Azimuth: %.2f\n", current_alt, current_az);
  
  /*
  while(abs(error_alt) > 1.18 || abs(error_az) > 400){
    Orientation m = getOrientation();//these might need to be modified based on mechanical setup
    roll = m.roll;
    pitch = m.pitch;
    heading = m.heading + dec_mag;
    PIDResult p = PID(alt, az, pitch, heading);
    float del_alt = p.delay_alt;
    float del_az = p.delay_az;
    float speedchange_alt = p.speed_alt;
    float speedchange_az = p.speed_az;
    move(del_alt, speedchange_alt, 0); // Motor alt is DIR_1
    move(del_az, speedchange_az, 1); //Motor az is DIR_2
    delay(200);
  }
  */
  delay(50);
}
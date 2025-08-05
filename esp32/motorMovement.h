const int DIR_1 = 26; //MOTOR 1 IS THE ONE WITH THE DRIVER FURTHER AWAY FROM POWER SUPPLY
const int STEP_1 = 27;
const int DIR_2 = 18;
const int STEP_2 = 19;
const int high_1 = 12;
const int high_2 = 14;
const int high_3 = 33;
const int high_4 = 32;
const int M0_1 = 15;
const int M1_1 = 13;
const int M2_1 = 2;
const int M0_2 = 4;
const int M1_2 = 25;
const int M2_2 = 16;
const int  steps_per_rev = 200 * 16;
 

void setupMotor()
{
  pinMode(STEP_1, OUTPUT);
  pinMode(DIR_1, OUTPUT);
  pinMode(STEP_2, OUTPUT);
  pinMode(DIR_2, OUTPUT);
  pinMode(high_1, OUTPUT);
  pinMode(high_2, OUTPUT);
  pinMode(high_3, OUTPUT);
  pinMode(high_4, OUTPUT);
  pinMode(M0_1, OUTPUT);
  pinMode(M1_1, OUTPUT);
  pinMode(M2_1, OUTPUT);
  pinMode(M0_2, OUTPUT);
  pinMode(M1_2, OUTPUT);
  pinMode(M2_2, OUTPUT);
  digitalWrite(high_1, HIGH);
  digitalWrite(high_2, HIGH);
  digitalWrite(high_3, HIGH);
  digitalWrite(high_4, HIGH);
  digitalWrite(M1_1, LOW);
  digitalWrite(M1_2, LOW);
  digitalWrite(M0_1, HIGH);
  digitalWrite(M0_2, HIGH);
  digitalWrite(M2_1, HIGH);
  digitalWrite(M2_2, HIGH);

}
void move(double speedchange, bool motor)
{
  int DIR = DIR_2;
  int STEP = STEP_2;
  if(motor == 0){
    DIR = DIR_1;
    STEP = STEP_1;
  }
  if(speedchange >= 0){
    digitalWrite(DIR, HIGH); // This will depend on motor wiring if HIGH or LOW
  }
  if(speedchange < 0){
    digitalWrite(DIR, LOW);
  }
  
  

  digitalWrite(STEP, HIGH);
  delayMicroseconds(300);
  digitalWrite(STEP, LOW);
  delayMicroseconds(50);
  
  
  
}
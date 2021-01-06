// initialize the pin 
int ENA = 5;
int ENB = 6;
int IN1 = 10;
int IN2 = 9;
int IN3 = 8;
int IN4 = 7;


void MotorWriting( int vL, int vR, int delayTime) // enter the left speed, right speed, and delay time
{
  bool dirL = 0;   // the left tire direction, 1 for forward, 0 for backward
  bool dirR = 0;   // the right tire direction, 1 for forward, 0 for backward
  unsigned int vLAbs = 0;   // the left tire speed magnitude
  unsigned int vRAbs = 0;   // the right tire speed magnitude
  double vLAdj = 0;
  double vRAdj = 0;
  
  int L3 = digitalRead(A0);
  int L2 = digitalRead(A1);
  int L1 = digitalRead(A2);
  int R1 = digitalRead(A3);
  int R2 = digitalRead(A4);
  int R3 = digitalRead(A5);

  double sumError = (-6) * L3 + (-2) * L2 + 2 * R2 + 6 * R3;
  int counter = L3 + L2 + L1 + R1 + R2 + R3;
  double error;
  if(counter == 0){
    error = 0;
  }
  else{
    error = sumError / counter;
  }
  vLAdj = vL + (70 * error);
  vRAdj = vR - (70 * error);
  if(vLAdj >= 0 )      // if vL is positive, dirL = 1, otherwise, dirL = 0
  {
    dirL = 1;
    vLAbs = vLAdj;     // assure that vLAbs is positive
  }  
  else
  {
    dirL = 0;
    vLAbs = -vLAdj;  
  }

  if(vRAdj >= 0 )      // if vR is positive, dirR = 1, otherwise, dirR = 0
  {
    dirR = 1;
    vRAbs = vRAdj;     // assure that vRAbs is positive
  }  
  else
  {
    dirR = 0;
    vRAbs = -vRAdj;  
  }
/*
  if(error == -5){
    vRAbs = 100;
    vLAbs = 100;
    dirL = 0;
    dirR = 0;
  }
*/
  if( dirL == 1 )  // left tire move forward with the speed vLAbs
  {

    digitalWrite(IN3,HIGH);
    digitalWrite(IN4,LOW);
  }
  else            // left tire move backward with the speed vLAbs
  {
    digitalWrite(IN3,LOW);
    digitalWrite(IN4,HIGH);
  }

  if( dirR == 1 )  // right tire move forward with the speed vRAbs
  {

    digitalWrite(IN1,HIGH);   
    digitalWrite(IN2,LOW);
  }
  else             // right tire move backward with the speed vRAbs
  {
    digitalWrite(IN1,LOW);
    digitalWrite(IN2,HIGH);
  }
  analogWrite(ENA,vRAbs);
  analogWrite(ENB,vLAbs);
  //delay(delayTime * 1000);   // delayTime s change to ms

  
  
  
}

void setup() { //define the pin as output
  
  
  pinMode(ENA,OUTPUT);  
  pinMode(IN1,OUTPUT);
  pinMode(IN2,OUTPUT);
  pinMode(IN3,OUTPUT);
  pinMode(IN4,OUTPUT);
  pinMode(ENB,OUTPUT);
  pinMode(A0, INPUT);
  pinMode(A1, INPUT);
  pinMode(A2, INPUT);
  pinMode(A3, INPUT);
  pinMode(A4, INPUT);
  pinMode(A5, INPUT);
}

void loop() {    
    
    MotorWriting( 100, 100, 0);
    delay(10);
    //analogWrite( ENA, 0 );  // stop the left tire
    //analogWrite( ENB, 0 );  // stop the right tire
}
/*
double error() {
  int L3 = digitalRead(A0);
  int L2 = digitalRead(A1);
  int L1 = digitalRead(A2);
  int R1 = digitalRead(A3);
  int R2 = digitalRead(A4);
  int R3 = digitalRead(A5);

  double sumError = (-3) * L3 + (-2) * L2 + (-1) * L1 + 1 * R1 + 2 * R2 + 3 * R3;
  int counter = L3 + L2 + L1 + R1 + R2 + R3;
  int a = 0;
  if (counter == 0){
    return -5;
  }
  else{
    return sumError / counter;
  }
}
*/
/*
#include  <SoftwareSerial.h>
SoftwareSerial BT(10, 11); // RX | TX
String message;
  
void setup()
{
  
  Serial.begin(9600);
  Serial.println("BT is ready!");
  BT.begin(9600);
}
  
void loop()
{
    while(Serial.available())
  {
    //while there is data available on the serial monitor
    message+=char(Serial.read());//store string from serial command
  }
  if(!Serial.available())
  {
    if(message!="")
    {
      //if data is available
      BT.println(message); //show the data
      message=""; //clear the data
    }
  }
    while(BT.available())
  {
    //while there is data available on the serial monitor
    message+=char(BT.read());//store string from serial command
  }
  if(!BT.available())
  {
    if(message!="")
    {
      //if data is available
      Serial.println(message); //show the data
      message=""; //clear the data
    }
  }
    
}
*/

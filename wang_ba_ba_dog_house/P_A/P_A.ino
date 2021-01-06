#include  <SoftwareSerial.h>
SoftwareSerial BT(3, 2); // RX | TX

// initialize the pin 
int ENA = 5;
int ENB = 6;
int IN1 = 10;
int IN2 = 9;
int IN3 = 8;
int IN4 = 7;

int old_err = 0;
int P_err;
int I_err = 0;
int D_err = 0;
double Kd = 1;
double Ki = 1;
double Kp = 80;

int err;
int control = 0;

String message;
String instruction;

void rightForward()
{
  digitalWrite(IN1,HIGH);
  digitalWrite(IN2,LOW);
  //Serial.println("Right forward");
}

void leftForward()
{
  digitalWrite(IN3,HIGH);
  digitalWrite(IN4,LOW);
  //Serial.println("Left forward");
}

void rightBackward()
{
  digitalWrite(IN1,LOW);
  digitalWrite(IN2,HIGH);
  //Serial.println("Right backward");
}

void leftBackward()
{
  digitalWrite(IN3,LOW);
  digitalWrite(IN4,HIGH);
  //Serial.println("Left backward");
}

void moveForward()
{
  analogWrite(ENA,100);
  analogWrite(ENB,100);
  leftForward();
  rightForward();
}

void moveBackward()
{
  analogWrite(ENA,100);
  analogWrite(ENB,100);
  leftBackward();
  rightBackward();  
}

void turnLeftCenter()
{
  analogWrite(ENA,100);
  analogWrite(ENB,100);
  leftBackward();
  rightForward();
}


void turnRightCenter()
{
  analogWrite(ENA,100);
  analogWrite(ENB,100);
  leftForward();
  rightBackward();
}


void turnLeftPherical()
{
  analogWrite(ENA,100);
  analogWrite(ENB,50);
  leftBackward();
  rightForward();
}
void turnRightPherical()
{
  analogWrite(ENA,50);
  analogWrite(ENB,100);
  leftForward();
  rightBackward();
}

void stopCar()
{
  analogWrite(ENA,0);
  analogWrite(ENB,0);
  leftForward();
  rightForward();  
}

void motorWriting(int vL, int vR, int error){      //speed and dir control

  int vRAdj = 0;
  int vLAdj = 0;


  vRAdj = vR - error;
  vLAdj = vL + error;

  
  if( vRAdj >= 0 )
    rightForward();
  else
  {
    rightBackward();
    vRAdj = -vRAdj;
  }
  
  if( vLAdj >= 0 )
    leftForward();
  else
  {
    leftBackward();  
    vLAdj = -vLAdj;
  }


  if(vRAdj > 255)
  {
    vRAdj = 255;
  }
  if(vLAdj > 255)
  {
    vLAdj = 255;
  }
  
  //Serial.print("vRAdj: ");
  //Serial.println(vRAdj);
  //Serial.print("vLAdj: ");
  //Serial.println(vLAdj);

  analogWrite(ENA ,vRAdj);
  analogWrite(ENB, vLAdj);

  //delay(2000);

  
 
  
}

// compute the error
int error(){

  int L3;
  int L2;
  int L1;
  int R1;
  int R2;
  int R3;

  int L3A = analogRead(A0);
  int L2A = analogRead(A1);
  int L1A = analogRead(A2);
  int R1A = analogRead(A3);
  int R2A = analogRead(A4);
  int R3A = analogRead(A5); 
   

  if(L3A > 70){
    L3 = 1;
  }
  else{
    L3 = 0;
  }
  if(L2A > 70){
    L2 = 1;
  }
  else{
    L2 = 0;
  }
  if(L1A > 70){
    L1 = 1;
  }
  else{
    L1 = 0;
  }
  if(R1A > 70){
    R1 = 1;
  }
  else{
    R1 = 0;
  }
  if(R2A > 70){
    R2 = 1;
  }
  else{
    R2 = 0;
  }
  if(R3A > 70){
    R3 = 1;
  }
  else{
    R3 = 0;
  }
  //int counter = L3 + L2 + L1 + R1 + R2 + R3;
  P_err = L3 * (-2) + L2 * (-1) + R2 * 1 + R3 * 2;
  I_err = I_err + P_err;
  D_err = P_err - old_err;

  old_err = P_err;
  
  double power = Kp*P_err + Ki*I_err + Kd*D_err;
  return power;
  /*
  if( counter == 0 )
  {
    return 0;
  }
  else
    return sum / counter;
  */  
}
void setup() {
  
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
  Serial.begin(9600);
  Serial.println("BT is ready!");
  BT.begin(9600);
}

void loop() {

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
      instruction = message;
      message=""; //clear the data
    }

    if(instruction == "w")
    {
      moveForward();
    }
    else if(instruction == "s")
    {
      moveBackward();
    }
    else if(instruction == "a")
    {
      turnLeftPherical();
    }
    else if(instruction == "d")
    {
      turnRightPherical();
    }
    else if(instruction == "q")
    {
      stopCar();
    }
    else
      Serial.println("Wrong Instructions!");
  
    if(instruction == "p")
    {
      control = 1;
    }
    else{
      control = 0;
    }
   
  
    if(control == 1){
      err = error();
      motorWriting(80 ,80, err);
    }   
  } 
  //delay(1);
}

/*
void loop(){
  err = error();
  motorWriting(100,100,err);

  delay(1);
}
*/

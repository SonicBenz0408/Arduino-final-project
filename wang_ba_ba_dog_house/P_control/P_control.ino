#include  <SoftwareSerial.h>
SoftwareSerial BT(3, 2); // RX | TX


// initialize the pin 
int ENA = 5;
int ENB = 6;
int IN1 = 10;
int IN2 = 9;
int IN3 = 8;
int IN4 = 7;

int Kp = 75;
double err;

String message;

void motorWriting(int vL, int vR){      //speed and dir control

  // P_control
  if(error() == 100){
    analogWrite(ENA, 0); //stop
    analogWrite(ENB, 0); //stop
    delay(50);
    //back
    vL = -100;
    vR = -100;
  }
  else{
    vL = vL + Kp*error();
    vR = vR - Kp*error();
  }
  
  // move forward or backward
  
  //right tire forward
  if(vR>0){
    digitalWrite(IN1,HIGH);   
    digitalWrite(IN2,LOW);
  }
  //right tire backward
  else{
    digitalWrite(IN1,LOW);   
    digitalWrite(IN2,HIGH);
    vR = -vR;
  }
  //left tire forward
  if(vL>0){
    digitalWrite(IN3,HIGH);   
    digitalWrite(IN4,LOW);
  }
  //left tire backward
  else{
    digitalWrite(IN3,LOW);   
    digitalWrite(IN4,HIGH);
    vL = -vL;
  }
  
  analogWrite(ENA, vR); //give speed(right)
  analogWrite(ENB, vL); //give speed(left)

  // back 0.1s
  if(error() == 100){
    delay(150);
  }
}

// compute the error
double error(){

  int L3 = digitalRead(A0);
  int L2 = digitalRead(A1);
  int L1 = digitalRead(A2);
  int R1 = digitalRead(A3);
  int R2 = digitalRead(A4);
  int R3 = digitalRead(A5);

  int sum = L3*(-2)+ L2*(-1) + R2*1 + R3*2;
  int counter = L3 + L2 + L1 + R1 + R2 + R3;
  if(counter == 0){
    err = 100;
  }
  else{
    err = sum/counter;
  }

  return err;
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

  String instruction = "";

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
  else if(instruction == "p")
  {
    err = error();
    motorWriting(100,100,err);
  }
  else if(instruction == "q")
  {
    stopCar();
  }
  else
    Serial.println("Wrong Instructions!");
   
  delay(1);
  } 
}

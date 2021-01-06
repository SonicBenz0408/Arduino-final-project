#include  <SoftwareSerial.h>
SoftwareSerial BT(3, 2); // RX | TX

// initialize the pin 
int ENA = 5;
int ENB = 6;
int IN1 = 10;
int IN2 = 9;
int IN3 = 8;
int IN4 = 7;

int Kp = 50;

int err;

String message;



void rightForward()
{
  digitalWrite(IN1,HIGH);
  digitalWrite(IN2,LOW);
  Serial.println("Right forward");
}

void leftForward()
{
  digitalWrite(IN3,HIGH);
  digitalWrite(IN4,LOW);
  Serial.println("Left forward");
}

void rightBackward()
{
  digitalWrite(IN1,LOW);
  digitalWrite(IN2,HIGH);
  Serial.println("Right backward");
}

void leftBackward()
{
  digitalWrite(IN3,LOW);
  Serial.println("Left backward");
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
  digitalWrite(IN4,HIGH);
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


  vRAdj = vR - error * Kp;
  vLAdj = vL + error * Kp;

  
  
  
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

  if(err == -8 )
  {
    vRAdj = 0;
    vLAdj = 0;
  }
  /*
  Serial.print("vRAdj: ");
  Serial.println(vRAdj);
  Serial.print("vLAdj: ");
  Serial.println(vLAdj);
  */

  analogWrite(ENA ,vRAdj);
  analogWrite(ENB, vLAdj);

  //delay(2000);

  
 
  
}

// compute the error
int error(){

  
  int L3A = analogRead(A0);
  int L2A = analogRead(A1);
  int L1A = analogRead(A2);
  int R1A = analogRead(A3);
  int R2A = analogRead(A4);
  int R3A = analogRead(A5);

  
  int maxA = L3A;
  int err = -4;

  if( L2A > maxA )
  {
    maxA = L2A;
    err = -2;
  }  
  if( L1A > maxA )
  {
    maxA = L1A;
    err = 0;
  }
  if( R1A > maxA )
  {
    maxA = R1A;
    err = 0;
  }
  if( R2A > maxA )
  {
    maxA = R2A;
    err = 2;
  }
  if( R3A > maxA )
  {
    maxA = R3A;
    err = 4;
  }

  if(maxA < 50 )
  {
    err = -8;
  }


 
  

  
  int L3 = digitalRead(A0);
  int L2 = digitalRead(A1);
  int L1 = digitalRead(A2);
  int R1 = digitalRead(A3);
  int R2 = digitalRead(A4);
  int R3 = digitalRead(A5);
  


  Serial.print("L3: ");
  Serial.println(L3);
  Serial.print("L2: ");
  Serial.println(L2);
  Serial.print("L1: ");
  Serial.println(L1);
  Serial.print("R1: ");
  Serial.println(R1);
  Serial.print("R2: ");
  Serial.println(R2);
  Serial.print("R3: ");
  Serial.println(R3);

  Serial.print("L3A: ");
  Serial.println(L3A);
  Serial.print("L2A: ");
  Serial.println(L2A);
  Serial.print("L1A: ");
  Serial.println(L1A);
  Serial.print("R1A: ");
  Serial.println(R1A);
  Serial.print("R2A: ");
  Serial.println(R2A);
  Serial.print("R3A: ");
  Serial.println(R3A);

  
  
   

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
  

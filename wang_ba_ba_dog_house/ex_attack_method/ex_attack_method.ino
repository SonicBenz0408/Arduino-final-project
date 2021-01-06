// initialize the pin 
int ENA = 5;
int ENB = 6;
int IN1 = 10;
int IN2 = 9;
int IN3 = 8;
int IN4 = 7;


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
  analogWrite(ENB,0);
  leftBackward();
  rightForward();
}
void turnRightPherical()
{
  analogWrite(ENA,0);
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

void MotorWriting(int vL, int vR){      //speed and dir control

  int vRAdj = 0;
  int vLAdj = 0;


  vRAdj = vR;
  vLAdj = vL;

  
  
  
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

// determine the speed (main func)
void ex_method(){

  int vL, vR;

  //stop to turn left
  if(type() == 1){
    vL = -100;
    vR = 100;
  }
  //stop to turn right
  else if(type() == 2){
    vL = 100;
    vR = -100;
  }

  //left tire set to zero to turn left
  else if(type() == 3){
    vL = 0;
    vR = 100;
  }
  //right tire set to zero to turn right
  else if(type() == 4){
    vL = 100;
    vR = 0;
  }
  //slow to turn left
  else if(type() == 5){
    vL = 50;
    vR = 110;
  }
  //slow to turn right
  else if(type() == 6){
    vL = 110;
    vR = 50;
  }
  //stop (outside the road)
  else if(type() == 7){
    vL = 75;
    vR = 75;
  }

  // straight gogo
  else if(type() == 8){
    vL = 125;
    vR = 125;
  }

  //give the motor speed
  MotorWriting(vL, vR);
}
// determine the type
int type(){

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
  
  int kind;

  int stop_sum = L3 + L2 + L1 + R1 + R2 + R3;

  
  //type 1: only L3=1
  if(L3 == 1 && L2 != 1){
    kind = 1;
  }
  //type 2: only R3=1
  else if(R3 == 1 && R2 != 1){
    kind = 2;
  }
  //type 3: L3=1 and L2=1
  else if(L3 == 1 && L2 == 1){
    kind = 3;
  }
  //type 4: R3=1 and R2=1
  else if(R3 == 1 && R2 == 1){
    kind = 4;
  }
  //type 5: L2=1
  else if(L2 == 1){
    kind = 5;
  }
  //type 6: R2=1
  else if(R2 == 1){
    kind = 6;
  }  
  //type 7: stop
  else if(stop_sum == 0){
    kind = 7;
  }

  // type 8: straight
  else{
    kind = 8;
  }

  return kind;
}
void setup() {

  //pin setting
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

  //main function
  ex_method();
  
  // 1ms dalay
  delay(1);
  
}

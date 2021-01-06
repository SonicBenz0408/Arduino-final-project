/***************************************************************************/
// File			  [node.h]
// Author		  [Erik Kuo, Joshua Lin]
// Synopsis		[Code for managing car movement when encounter a node]
// Functions  [/* add on yout own! */]
// Modify		  [2020/03/027 Erik Kuo]
/***************************************************************************/

#include <SoftwareSerial.h>
#include <Wire.h>
#include "track.h"

/*===========================import variable===========================*/
int extern r1, l1, r2, l2, r3, l3;
int extern _Tp;

/*===========================import variable===========================*/
// TODO: add some function to control your car when encounter a node

void makeaturn (char command[100]){

  unsigned static int counter = 0;
  # ifdef DEBUG
  Serial.println("makeaturn");
  Serial.print("command[ ");
  Serial.print(counter);
  Serial.print(" ]: ");
  Serial.println(command[counter]);
  
 
  Serial.print("counter: ");
  Serial.println(counter);

  #endif
  
if(command[counter]=='a')//往前
{
  //Serial.print("counter0");
  moveForward();
  delay(200);
}
else if(command[counter]=='u')//迴轉
{
  turnRightCenter();
  delay(700);
   while(findlineyet()){
    stopCar();
    delay(50);
    turnRightCenter();
    delay(50);
}
}
else if(command[counter]=='r')// 右轉
{
  #ifdef DEBUG
  Serial.println("right eight");
  #endif
   turnRightCenter();
  delay(400);
  while(findlineyet()){
    stopCar();
    delay(50);
    turnRightCenter();
    delay(50);
  }
}
else if(command[counter]=='l')//左轉
{
  turnLeftCenter();
   delay(490);
    while(findlineyet()){
    stopCar();
    delay(50);
    turnLeftCenter();
    delay(50); 
  }
}
else{
  ;
}

#ifdef DEBUG
Serial.print("command[ ");
Serial.print(counter);
Serial.print(" ]: ");
Serial.println(command[counter]);

#endif
/*else if(command[i]==NULL);
{
  stopCar();
  exit;
}*/
if(counter<99)
  counter++;
if(counter==99)
  stopCar();
}
// here are something you can try: left_turn, right_turn... etc.

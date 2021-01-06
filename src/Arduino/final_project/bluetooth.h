/***************************************************************************/
// File			  [bluetooth.h]
// Author		  [Erik Kuo]
// Synopsis		[Code for bluetooth communication]
// Functions  [ask_BT, send_msg, send_byte]
// Modify		  [2020/03/27 Erik Kuo]
/***************************************************************************/

/*if you have no idea how to start*/
/*check out what you have learned from week 2*/

#include<SoftwareSerial.h>
extern SoftwareSerial BT;
enum BT_CMD {
    FORWARD,
    LEFT,
    BACKWARD,
    RIGHT,
  NOTHING,
  // TODO: add your own command type here
};

char ask_BT_begin(){
  static char val = ' ';
  if(BT.available()){
    val = BT.read();
    return val;
  }
}
BT_CMD ask_BT(char* command){
    BT_CMD message=NOTHING;
    char val;
    static unsigned int j = 0;
      while(val != 'e'){
        if (BT.available()) {
          val = BT.read();
          command[ j ] = val;
          j++;
        }
      }  

      #ifdef DEBUG
   
      for(int i = 0; i < 100; i++)
      {
        Serial.print(command[i]);
        Serial.print(" ");
      }
      #endif
   
    
  
  /*
    char cmd = "";
    if(BT.available()){
      cmd = char(BT.read());
      if(cmd == 'w')
      {
          message = FORWARD;
      }
      if(cmd == 'a')
      {
          message = LEFT;
      }
      if(cmd == 's')
      {
          message = BACKWARD;
      }
      if(cmd == 'd')
      {
          message = RIGHT;
      }
      cmd = "";
      
      // TODO:
      // 1. get cmd from SoftwareSerial object: BT
      // 2. link bluetooth message to your own command type
      #ifdef DEBUG
      Serial.print("cmd : ");
      Serial.println( cmd );
      #endif
      
    }
    return message;
    */
}// ask_BT

// send msg back through SoftwareSerial object: BT
// can use send_byte alternatively to send msg back
// (but need to convert to byte type)
void send_msg(const char& msg)
{
    BT.print(msg);
     // TODO:
}// send_msg

// send UID back through SoftwareSerial object: BT
void send_byte(byte *id, byte& idSize) {

  
  for (byte i = 0; i < idSize; i++) {  // Send UID consequently.
    //BT.write(id[i]);
    
    Serial.print(id[i], HEX);
  }
  
  #ifdef DEBUG
  Serial.print("Sent id: ");
  for (byte i = 0; i < idSize; i++) {  // Show UID consequently.
    Serial.print(id[i], HEX);
  }
  Serial.println();
  
  #endif
  for (byte i = 0; i < idSize; i++) {  // Send UID consequently.
    id[ i ] = 0;
  }
}// send_byte

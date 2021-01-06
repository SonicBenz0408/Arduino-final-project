/***************************************************************************/
// File       [final_project.ino]
// Author     [Erik Kuo]
// Synopsis   [Code for managing main process]
// Functions  [setup, loop, Search_Mode, Hault_Mode, SetState]
// Modify     [2020/03/27 Erik Kuo]
/***************************************************************************/

//#define DEBUG // debug flag
//#define testCar
// for BlueTooth
#include<SoftwareSerial.h>
// for RFID
#include <SPI.h>
#include <MFRC522.h>
// Import header files




/*===========================define pin & create module object================================*/
// BlueTooth
SoftwareSerial BT(2,1);   // TX,RX on bluetooth module, 請按照自己車上的接線寫入腳位
// L298N, 請按照自己車上的接線寫入腳位(左右不一定要跟註解寫的一樣)
#define MotorR_I1      3 //定義 I1 接腳（右）
#define MotorR_I2      4 //定義 I2 接腳（右）
#define MotorL_I3      7 //定義 I3 接腳（左）
#define MotorL_I4      8 //定義 I4 接腳（左）
#define MotorL_PWML    6 //定義 ENA (PWM調速) 接腳
#define MotorR_PWMR    5  //定義 ENB (PWM調速) 接腳
// 循線模組, 請按照自己車上的接線寫入腳位
#define L1   A2  // Define Left Most Sensor Pin
#define L2   A1  // Define Left Middle Sensor Pin
#define L3   A0  // Define Middle Left Sensor Pin
#define R3   A5  // Define Middle Right Sensor Pin
#define R2   A4  // Define Right Middle Sensor Pin
#define R1   A3  // Define Right Most Sensor Pin
// RFID, 請按照自己車上的接線寫入腳位
#define RST_PIN     9         // 讀卡機的重置腳位
#define SS_PIN      10        // 晶片選擇腳位
MFRC522 mfrc522(SS_PIN, RST_PIN);  // 建立MFRC522物件

/*===========================define pin & create module object===========================*/
#include "RFID.h"
#include "track.h"
#include "bluetooth.h"
#include "node.h"
/*===========================declare function prototypes===========================*/
// search graph
void Search_Mode();
// wait for command
void Hault_Mode();
void SetState();
byte idSize;
byte* prfid;
char* command;


/*===========================declare function prototypes===========================*/

/*===========================define function===========================*/
void setup()
{
   //bluetooth initialization
   BT.begin(9600);
   //Serial window
   Serial.begin(9600);
   //RFID initial
   SPI.begin();
   mfrc522.PCD_Init();
   //L298N pin
   pinMode(MotorR_I1,   OUTPUT);
   pinMode(MotorR_I2,   OUTPUT);
   pinMode(MotorL_I3,   OUTPUT);
   pinMode(MotorL_I4,   OUTPUT);
   pinMode(MotorL_PWML, OUTPUT);
   pinMode(MotorR_PWMR, OUTPUT);
   
   //tracking pin
   pinMode(R1, INPUT); 
   pinMode(R2, INPUT);
   pinMode(R3, INPUT);
   pinMode(L1, INPUT);
   pinMode(L2, INPUT);
   pinMode(L3, INPUT);
   
    SetState();
    
   
   
 
   
#ifdef DEBUG
  Serial.println("Start!");
#endif
  analogWrite(MotorR_PWMR,0);
  analogWrite(MotorL_PWML,0);

  

}// setup


// initalize parameter
// variables for 循線模組
int r2=0,r1=0,r3=0,l3=0,l1=0,l2=0;
// variable for motor power
int _Tp=30;
// enum for car states, 不懂得可以自己google C++ enum
enum ControlState
{
   HAULT_STATE,
   SEARCH_STATE,
};
ControlState _state=HAULT_STATE;
// enum for bluetooth message, reference in bluetooth.h line 2
BT_CMD _cmd = NOTHING;
const char test1 ={'w'};
const char test2 ={'u'};
const char test3 ={'d'};
const char test4 ={'a'};

#ifdef testCar
const char test[100] ={'r','r','u','r','r'};
#endif

void loop()
{
   // search graph
   
    Search_Mode();
 
    
    //if(int(prfid)!=0)
    if(checknode()!=0)
    {
        prfid = rfid(idSize);
      if(int(prfid)!=0)
        send_byte(prfid,idSize);
       moveForward();
       delay(340);
      Hault_Mode();
      delay(200);
      //Serial.print("counter: ");
      //Serial.print(counter);
     #ifdef testCar
     makeaturn(test);
     #endif
     #ifndef testCar
     makeaturn(command);
     #endif
     Hault_Mode();
     delay(500);
     
    }
    

   //tracking();
   
   }// loop

void SetState()// Get command from bluetooth 
{
   command = new char [100];
   for(int i = 0; i < 100; i++)
    command[ i ] = ' ';
   char judge = "";   
   # ifndef testCar
   while(judge != 's')
   {
    judge = ask_BT_begin();       
   }
    
   
   //Serial.println(judge); 
   //Serial.println("I'm here!");
   ask_BT(command);
   #endif
   
}

void Hault_Mode()
{stopCar();}

void Search_Mode()
{tracking();}
/*===========================define function===========================*/

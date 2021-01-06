import BT
import bfs
import time
class interface():
    end_go = 'x'
    end_back = 'y'
    def __init__(self):
        print("")
        print("Arduino Bluetooth Connect Program.")
        print("")
        self.ser = BT.bluetooth()
        port = "COM8"  #input("PC bluetooth port name: ")
        while(not self.ser.do_connect(port)):
            if(port == "quit"):
                self.ser.disconnect()
                quit()
            time.sleep(1)
            port = "COM8"   #input("PC bluetooth port name: ")
        self.path = ""
        input("Ready to work!")
        self.ser.SerialWrite('p')

    def start_signal(self):
        return self.ser.SerialWrite('s')

    def send_action_go(self,dirc_m):
        # TODO : send the action to car
        print('action:' + dirc_m)
        return self.ser.SerialWrite(dirc_m+interface.end_go)
    def send_action_back(self,dirc_m):
        # TODO : send the action to car
        print('action:' + dirc_m)
        return self.ser.SerialWrite(dirc_m+interface.end_back)

    def send_weight(self, weight):

        if weight == 0:
            print("請確認是否有選擇餐點！")
        elif weight > 0 and weight < 7:
            print("dishNum:"+str(weight))
            return self.ser.SerialWrite(str(weight))
        else:
            print("dishNum:"+"0")
            return self.ser.SerialWrite('0')
    def send_number(self, num):
        if num > 0 or num < 7:
            print("tableNum:"+str(num))
            return self.ser.SerialWrite(str(num))
        else:
            print("table number is invalid.")

    def get_response(self):
        while True:
            judge = self.ser.SerialReadString()
            if judge != '':
                break
        print("ok")
        return judge
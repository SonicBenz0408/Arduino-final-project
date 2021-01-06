import BT
import maze_dijk
import score

# hint: You may design additional functions to execute the input command, which will be helpful when debugging :)

class interface:
    def __init__(self):
        print("")
        print("Arduino Bluetooth Connect Program.")
        print("")
        self.ser = BT.bluetooth()
        port = input("PC bluetooth port name: ")
        while(not self.ser.do_connect(port)):
            if(port == "quit"):
                self.ser.disconnect()
                quit()
            port = input("PC bluetooth port name: ")
        input("Press enter to start.")
        self.ser.SerialWrite('s')

    def get_UID(self):
        while True:
            UID = self.ser.SerialReadByte()
            if UID != 0:
                return UID
        #return self.ser.SerialReadByte()

    def save_action(self,dirc):
        # TODO : send the action to car
        if dirc == 1:
            message = 'a' #advance
        elif dirc == 2:
            message = 'u' #U turn
        elif dirc == 3:
            message = 'r' #turn right
        elif dirc == 4:
            message = 'l' #turn left
        elif dirc == 5:
            message = 'h' #halt
            
        return message

    def send_action(self,dirc_m):
        # TODO : send the action to car
        print('action:' + dirc_m)
        return self.ser.SerialWrite(dirc_m+'e')

    def get_message(self):
        # get the message from car
        return self.ser.SerialReadString()

"""
    def end_process(self):
        self.ser.SerialWrite('e')
        self.ser.disconnect()
"""
if __name__ == '__main__':
    interf = interface()

    
from evdev import InputDevice, categorize, ecodes
from select import select
import pistomp.encoderswitch as EncoderSwitch


class InputDeviceDispatcher:
    def __init__(self, device_fs, cb_enc_top, cb_enc_sw, footswitches):
        try:
            self.device = InputDevice(device_fs)
        except:
            self.device = None
            pass

        self.footswitches = footswitches
        self.cb_enc_top = cb_enc_top
        self.cb_enc_sw = cb_enc_sw
        print("Initializing joystick", self.device)
        print("Footswitches", self.footswitches)
        
    def read_joystick(self):
        if self.device:
            try:
                r,w,x = select([self.device], [], [])
                for event in self.device.read():
                    # print(categorize(event), "E", event.code, event.type, event.value)

                    if event.code == 0 and event.type == 3 and event.value < 127:
                        self.cb_enc_top(-1)
                    elif event.code == 0 and event.type == 3 and event.value > 127:
                        self.cb_enc_top(1)
                    if event.code == 1 and event.type == 3 and event.value < 127:
                        self.cb_enc_top(-1)
                    elif event.code == 1 and event.type == 3 and event.value > 127:
                        self.cb_enc_top(1)
                        
                    elif event.code == 297 and event.type == 1 and event.value == 0:
                        self.cb_enc_sw(EncoderSwitch.Value.RELEASED)
                    elif event.code == 296 and event.type == 1 and event.value == 0:
                        self.cb_enc_sw(EncoderSwitch.Value.LONGPRESSED)
                        
                    elif event.code == 292 and event.type == 1 and event.value == 0:
                        self.footswitches[4].pressed(True)
                    elif event.code == 293 and event.type == 1 and event.value == 0:
                        self.footswitches[4].pressed(True)
                        
                    elif event.code == 291 and event.type == 1 and event.value == 0:
                        self.footswitches[0].pressed(True)
                    elif event.code == 290 and event.type == 1 and event.value == 0:
                        self.footswitches[1].pressed(True)
                    elif event.code == 288 and event.type == 1 and event.value == 0:
                        self.footswitches[2].pressed(True)
                    elif event.code == 289 and event.type == 1 and event.value == 0:
                        self.footswitches[3].pressed(True)                                            
                    
            except Exception as e:
                print("Error in joystick capture", str(e))
                pass

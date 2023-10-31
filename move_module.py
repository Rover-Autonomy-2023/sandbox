from pyPS4Controller.controller import Controller
from roboclaw_3 import Roboclaw

# Initialize the Roboclaw controllers
RC_front = Roboclaw("/dev/ttyACM0", 38400)
RC_back = Roboclaw("/dev/ttyACM1", 38400)

RC_front.Open()
RC_back.Open()

# Function to map thumbstick values to motor speed range
def map_speed(value, in_min, in_max, out_min, out_max):
    return int((value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

class MyController(Controller):
    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)

    # Callback when left thumbstick is moved
    def on_L3_up(self, value):
        speed = map_speed(value, -1, 1, 0, 128)
        RC_front.ForwardM1(128, speed)
        RC_front.ForwardM2(128, speed)

    # Callback when right thumbstick is moved
    def on_R3_up(self, value):
        speed = map_speed(value, -1, 1, 0, 128)
        RC_back.ForwardM1(128, speed)
        RC_back.ForwardM2(128, speed)

# Create the controller instance
controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)

try:
    controller.listen()
except KeyboardInterrupt:
    controller.disconnect()



#   This class handles the button input from Arduino


class Input:
    # Required for communication with Arduino
    import pyfirmata
    from pyfirmata import Arduino, util
    import time

    from sound import Sound

    def __init__(self):

        # Set port
        self.port = "COM5"
        self.ard = Input.pyfirmata.Arduino(self.port)

        # Set button pins
        self.b0 = self.ard.get_pin("d:2:i").pin_number  # Digital pin 2, Output
        self.b1 = self.ard.get_pin("d:3:i").pin_number  # Digital pin 3, Output
        self.b2 = self.ard.get_pin("d:4:i").pin_number  # Digital pin 4, Output
        self.b3 = self.ard.get_pin("d:5:i").pin_number  # Digital pin 5, Output
        self.b4 = self.ard.get_pin("d:6:i").pin_number  # Digital pin 6, Output
        self.b5 = self.ard.get_pin("d:7:i").pin_number  # Digital pin 7, Output
        self.b6 = self.ard.get_pin("d:8:i").pin_number  # Digital pin 8, Output
        self.buttons = [self.b0, self.b1, self.b2, self.b3, self.b4, self.b5, self.b6]  # Load buttons into array for easy looping

        # Instance of Iterator reads and handles data from Arduino over the serial port,
        # it keeps the boards pin values up to date
        self.iterator = Input.pyfirmata.util.Iterator(self.ard)
        self.iterator.start()

    # Check if digital pin is read FALSE (when pressed)
    def check_pressed(self, pin_num):
        pressed = self.ard.digital[pin_num].read()

        if pressed == 0:
            # Return corresponding column value for the specific button (directly related to button)
            if self.pin_num == self.b0:
                return 0
            elif self.pin_num == self.b1:
                return 1
            elif self.pin_num == self.b2:
                return 2
            elif self.pin_num == self.b3:
                return 3
            elif self.pin_num == self.b4:
                return 4
            elif self.pin_num == self.b5:
                return 5
            elif self.pin_num == self.b6:
                return 6
        else:
            return None



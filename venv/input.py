#   This class handles the button input from Arduino


class Input:

    def __init__(self):
        # Required for communication with Arduino


        # Set port
        port = "COM5"
        ard = pyfirmata.Arduino(port)

        # Set button pins
        b0 = ard.get_pin("d:2:i").pin_number  # Digital pin 2, Output
        b1 = ard.get_pin("d:3:i").pin_number  # Digital pin 3, Output
        b2 = ard.get_pin("d:4:i").pin_number  # Digital pin 4, Output
        b3 = ard.get_pin("d:5:i").pin_number  # Digital pin 5, Output
        b4 = ard.get_pin("d:6:i").pin_number  # Digital pin 6, Output
        b5 = ard.get_pin("d:7:i").pin_number  # Digital pin 7, Output
        b6 = ard.get_pin("d:8:i").pin_number  # Digital pin 8, Output

        buttons = [b0, b1, b2, b3, b4, b5, b6]  # Load buttons into array for easy looping

        n1 = ard.get_pin("d:9:p").pin_number  # Digital pin 9, Input

        # Instance of Iterator reads and handles data from Arduino over the serial port,
        # it keeps the boards pin values up to date
        iterator = pyfirmata.util.Iterator(ard)
        iterator.start()

    # Check if digital pin is read FALSE (when pressed)
    def check_pressed(self, pin_num):
        pressed = ard.digital[pin_num].read()

        if pressed == 0:
            play_note()  # Play default sound upon click

            # Return corresponding column value for the specific button (directly related to button)
            if self.pin_num == b0:
                return 0
            elif self.pin_num == b1:
                return 1
            elif self.pin_num == b2:
                return 2
            elif self.pin_num == b3:
                return 3
            elif self.pin_num == b4:
                return 4
            elif self.pin_num == b5:
                return 5
            elif self.pin_num == b6:
                return 6
        else:
            return None

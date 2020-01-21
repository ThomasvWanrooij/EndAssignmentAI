import pyfirmata
import tone
from pyfirmata import Arduino, util
import time

port = "COM5"
board = pyfirmata.Arduino(port)

b1 = board.get_pin("d:2:i").pin_number
b2 = board.get_pin("d:3:i").pin_number
b3 = board.get_pin("d:4:i").pin_number
b4 = board.get_pin("d:5:i").pin_number
b5 = board.get_pin("d:6:i").pin_number
b6 = board.get_pin("d:7:i").pin_number
b7 = board.get_pin("d:8:i").pin_number

buttons = [b1, b2, b3, b4, b5, b6, b7]

n1 = board.get_pin("d:9:p").pin_number

iterator = pyfirmata.util.Iterator(board)
iterator.start()

lose = 0
win = 0


def play_note():
    notes_click = [2.5, 0, 5, 0]
    notes_win = [5, 0, 5, 2.5, 0, 5, 0, 5, 0]
    notes_lose = [5, 5, 5, 4, 4, 4, 2, 2, 2, 2, 0]
    noteDurations = [1/12]
    pauseBetweenNotes = noteDurations[0] * 1.30

    if win:
        for i in notes_win:
            time.sleep(pauseBetweenNotes)
            board.digital[n1].write(i)
    elif lose:
        for i in notes_lose:
            time.sleep(pauseBetweenNotes)
            board.digital[n1].write(i)
    else:
        for i in notes_click:
            time.sleep(pauseBetweenNotes)
            board.digital[n1].write(i)


def check_pressed(pinNum):
    pressed = board.digital[pinNum].read()

    if pressed == 0:
        play_note()
        if pinNum == b1:
            print("Button 1 is pressed")
        elif pinNum == b2:
            print("Button 2 is pressed")
        elif pinNum == b3:
            print("Button 3 is pressed")
        elif pinNum == b4:
            print("Button 4 is pressed")
        elif pinNum == b5:
            print("Button 5 is pressed")
        elif pinNum == b6:
            print("Button 6 is pressed")
        elif pinNum == b7:
            print("Button 7 is pressed")


for x in buttons:
    time.sleep(0.001)
    check_pressed(x)

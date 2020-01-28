#   This class handles the sound effects that are present in the game


class Sound:

    def __init__(self):
        # Set to false at the start of the game, for sound selection
        win = False
        lose = False

    def play_note():
        notes_click = [2.5, 0, 5, 0]  # Sequence of voltages for click
        notes_win = [5, 0, 5, 2.5, 0, 5, 0, 5, 0]  # Sequence of voltages for win (player)
        notes_lose = [5, 5, 5, 4, 4, 4, 2, 2, 2, 2, 0]  # Sequence of voltages for loss (player)
        noteDurations = [
            1 / 12]  # All notes have same duration, but this can be changed by adding more possible durations
        pauseBetweenNotes = noteDurations[0] * 1.30  # This value seemed to sound best

        if win:
            for i in notes_win:  # Pick from win sequence
                time.sleep(pauseBetweenNotes)
                ard.digital[n1].write(i)  # Write to Arduino pin 9
        elif lose:
            for i in notes_lose:  # Pick from loss sequence
                time.sleep(pauseBetweenNotes)
                ard.digital[n1].write(i)  # Write to Arduino pin 9
        else:
            for i in notes_click:  # Pick from click sequence
                time.sleep(pauseBetweenNotes)
                ard.digital[n1].write(i)  # Write to Arduino pin 9



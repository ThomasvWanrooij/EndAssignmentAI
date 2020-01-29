#   This class handles the sound effects that are present in the game


class Sound:
    import simpleaudio as sa

    def __init__(self):

        self.play_obj = None
        self.game_state = None

        self.click_sound = Sound.sa.WaveObject.from_wave_file("coin.wav")
        self.win_sound = Sound.sa.WaveObject.from_wave_file("win.wav")
        self.lose_sound = Sound.sa.WaveObject.from_wave_file("lose.wav")

    def set_tune(self, game_state):
        self.game_state = game_state

    def play_note(self):
        self.play_obj = None
        if self.game_state == 0:
            self.play_obj = self.click_sound.play()
            self.play_obj.wait_done()
        elif self.game_state == 1:
            self.play_obj = self.win_sound.play()
            self.play_obj.wait_done()
        elif self.game_state == 2:
            self.play_obj = self.lose_sound.play()
            self.play_obj.wait_done()
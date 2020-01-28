#   This class handles the sound effects that are present in the game


class Sound:

    import simpleaudio as sa

    # Set to false at the start of the game, for sound selection
    game_state = None
    win = False
    lose = False
    play_obj = None

    lose_sound = sa.WaveObject.from_wave_file("lose.wav")
    win_sound = sa.WaveObject.from_wave_file("win.wav")
    click_sound = sa.WaveObject.from_wave_file("coin.wav")

    def set_tune(self, game_state):
        self.game_state = game_state

    def play_note(self):
        if self.game_state == 0:
            self.play_obj = self.click_sound.play()
            self.play_obj.wait_done()
        elif self.game_state == 1:
            self.play_obj = self.win_sound.play()
            self.play_obj.wait_done()
        elif self.game_state == 2:
            self.play_obj = self.lose_sound.play()
            self.play_obj.wait_done()


geluidje = Sound()
geluidje.set_tune(0)
geluidje.play_note()
geluidje.set_tune(1)
geluidje.play_note()
geluidje.set_tune(2)
geluidje.play_note()

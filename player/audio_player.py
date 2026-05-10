import pygame


class AudioPlayer:

    def __init__(self):

        pygame.mixer.init()

        self.current_song = None
        self.paused = False

    def load(self, song_path):

        pygame.mixer.music.load(song_path)

        self.current_song = song_path

    def play(self):

        pygame.mixer.music.play()
        self.paused = False

    def pause(self):

        pygame.mixer.music.pause()
        self.paused = True

    def resume(self):

        pygame.mixer.music.unpause()
        self.paused = False

    def stop(self):

        pygame.mixer.music.stop()

    def is_playing(self):

        return pygame.mixer.music.get_busy()
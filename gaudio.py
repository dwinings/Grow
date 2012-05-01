from pygame import mixer
from pygame.mixer import Sound
from random import choice
import os



class Audio:

    PLAY  = 0
    PAUSE = 1
    STOP  = 2
    GRAVITY = 0
    DEATH = 1
    
    def __init__(self):
        mixer.init(frequency=44100, size=-16, channels=4, buffer=4096)
        self._background_s = Sound(os.path.join('res', 'background.ogg'))
        self._background_s.set_volume(0.4)
        self._grav_fxs_s = [Sound(os.path.join('res', 'grav1.wav')), Sound(os.path.join('res', 'grav2.wav')), Sound(os.path.join('res','grav3.wav'))]
        self._death_s = Sound(os.path.join('res', 'death.wav'))
        
        self._background_channel = mixer.find_channel()
        self._fx_channel = mixer.find_channel()
        self.effect_playing = False
        self.bg_playing = False
        
    def bg(self, state=0):
        if state == self.PLAY:
            if self._background_channel.get_sound() == None:
                self._background_channel.play(self._background_s, loops=-1, fade_ms=250)
            else:
                self._background_channel.unpause()
            self.bg_playing = True
        elif state == self.PAUSE:
            self._background_channel.pause()
            self.bg_playing = False
        else:
            self._background_channel.stop()
            self.bg_playing = False
            
    def fx(self, state=0, fx = 0):
        if state == self.PLAY:
            if fx == self.GRAVITY:
                if self._fx_channel.get_sound() not in self._grav_fxs_s:
                    self._fx_channel.stop()
                    self._fx_channel.play(choice(self._grav_fxs_s), loops=0, fade_ms=0)
            else:
                if self._fx_channel.get_sound() != self._death_s:
                    self._fx_channel.stop()
                    self._fx_channel.play(self._death_s, loops=0, fade_ms=0)
                
        elif state == self.PAUSE:
            self._fx_channel.pause()
        else:
            self._fx_channel.stop()
        

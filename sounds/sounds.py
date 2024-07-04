from enum import Enum, auto
from pygame import mixer


class SoundName(Enum):
    COIN_COLLECTED = auto()
    GAME_OVER = auto()
    JUMP = auto()
    MENU_BUTTON_CLICK = auto()
    LEVEL_COMPLETE = auto()
    PIPE_ENTER_EXIT = auto()
    GAME_COMPLETE = auto()
    STOMP = auto()
    PLAYER_DEATH = auto()
    KEY_COLLECTED = auto()

    def get_file_name(self):
        return "sounds/" + self.name.lower() + ".wav"

    def get_sound(self):
        return mixer.Sound(self.get_file_name())

    @classmethod
    def get_all(cls):
        return [_ for _ in cls]

class MusicName(Enum):
    FIELDS_OF_ICE = auto()
    FOR_ME = auto()
    THE_WAY_YOU_LOVE = auto()
    TITLE_THEME = auto()
    WAVES_IN_FLIGHT = auto()

    def get_file_name(self):
        return "sounds/" + self.name.lower() + ".wav"

    @classmethod
    def get_all(cls):
        return [_ for _ in cls]


def play_sound(sound: SoundName):
    mixer.Sound.play(sound.get_sound())


def play_music(music: MusicName):
    mixer.music.load(music.get_file_name())
    mixer.music.play(-1)


def pause_music():
    mixer.music.pause()


all_sounds = SoundName.get_all()
all_music = MusicName.get_all()
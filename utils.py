from gtts import gTTS
from playsound import playsound
import itertools
import os


def add_affix(main=None, pre=None, suf=None):
    if pre == suf is None:
        comb = list(itertools.product(main))
    elif pre is None:
        comb = list(itertools.product(main, suf))
    elif suf is None:
        comb = list(itertools.product(pre, main))
    else:
        comb = list(itertools.product(pre, main, suf))

    comb_list = list(map(lambda x: ' '.join(x), comb))

    return comb_list


def playaudio(text_to_speak):
    tts = gTTS(text=text_to_speak, lang='bn', lang_check=True)
    mp3_file = '1.mp3'
    tts.save(mp3_file)
    # os.system('mpg321 {}'.format(mp3_file))
    playsound(mp3_file)
    os.remove(mp3_file)


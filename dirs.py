import os
from assets import music


def play_music(filename):
    basedir = os.getcwd()

    filedir = (str(basedir) + "\\assets\\music\\")

    path_to_file = (str(filedir) + str(filename) + ".mp3")

    print(path_to_file)



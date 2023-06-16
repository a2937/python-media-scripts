#!/usr/bin/env python3 # [1]

import speech_recognition as sr
import sys 
import os

from os import path

# Get the name of the audio file to be read
file_name = sys.argv[1] 

# Get the path of the file
AUDIO_FILE = path.abspath(file_name)

# use the audio file as the audio source
r = sr.Recognizer()
with sr.AudioFile(AUDIO_FILE) as source:
    audio = r.record(source)  # read the entire audio file

# recognize speech using Sphinx
try:
    extension_index = file_name.index(".")
    extension = file_name[extension_index:]
    proper_name = file_name.replace(extension,"_lyrics.txt")
    f = open(proper_name, 'w', encoding='utf-8')
    f.write("# This is a rough transcription by Sphinx and may not be fully accurate\n\n")
    speech = r.recognize_sphinx(audio)
    f.write(speech)
    f.close()
    print("Successfully written to " + proper_name + ".")
except sr.UnknownValueError:
    print("Sphinx could not understand the audio")
except sr.RequestError as e:
    print("Sphinx error; {0}".format(e))

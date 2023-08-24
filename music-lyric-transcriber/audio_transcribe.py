#!/usr/bin/env python3 # [1]

import speech_recognition as sr
import sys 
import os

from os import path

def main():
    if len(sys.argv) < 2:
        print("Usage: python audio_transcribe.py audio_file.wav")
        return

    file_name = sys.argv[1]

    if not os.path.exists(file_name):
        print("Error: File does not exist.")
        return

    audio_file_path = path.abspath(file_name)

    r = sr.Recognizer()
    with sr.AudioFile(audio_file_path) as source:
        audio = r.record(source)

    try:
        base_name = os.path.splitext(file_name)
        proper_name = base_name + "_lyrics.txt"
        
        with open(proper_name, 'w', encoding='utf-8') as f:
            f.write("# This is a rough transcription by Sphinx and may not be fully accurate\n\n")
            speech = r.recognize_sphinx(audio)
            f.write(speech)
        
        print("Successfully written to " + proper_name + ".")
    except sr.UnknownValueError:
        print("Sphinx could not understand the audio")
    except sr.RequestError as e:
        print("Sphinx error:", e)

if __name__ == "__main__":
    main()
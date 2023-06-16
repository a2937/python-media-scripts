#!/usr/bin/env python3 # [1]
from os import path,remove
import sys 
import whisper_timestamped as whisper
import time
from moviepy.editor import *
import json

file_name = sys.argv[1] 

# Get the path of the file
VIDEO_FILE = path.abspath(file_name)

# Insert Local Video File Path
clip = VideoFileClip(VIDEO_FILE)


extension_index = file_name.index(".")
extension = file_name[extension_index:]
#proper_name = file_name.replace(extension,"_audio.wav")
proper_name = 'audio.wav' 
#clip.audio.write_audiofile(proper_name,codec='pcm_s16le')




# wait for the file to be written 
seconds = 10 


for i in range(0, int(seconds * 100)):
          while True:
            time.sleep(seconds / 100)
            if os.path.exists(proper_name):
                print("Audio Copy loaded")
                # open the file
                print(proper_name)

                audio = whisper.load_audio(proper_name)
                model = whisper.load_model("base")
                result = whisper.transcribe(model, audio, language="en")
                print(json.dumps(result, indent = 2, ensure_ascii = False))
                break
          break

print("Should have exited the loop")          
# Cleanup the old audio file            
remove(proper_name)

#!/usr/bin/env python3 # [1]
import sys
from os import path, remove
from moviepy import *
import whisper_timestamped as whisper

def generate_subtitles(transcribed_dialogues, duration_per_dialogue=3):
    subtitles = []
    current_timestamp = 0

    for dialogue in transcribed_dialogues:
        start_timestamp = format_timestamp(current_timestamp)
        current_timestamp += duration_per_dialogue
        end_timestamp = format_timestamp(current_timestamp)

        subtitles.append({
            "start": start_timestamp,
            "end": end_timestamp,
            "dialogue": dialogue,
            'index': len(subtitles) + 1
        })

    return subtitles

def write_srt(subtitle, output_srt_file):
    with open(output_srt_file, "a") as f:  # Use "a" mode for append
        f.write(str(subtitle["index"]) + "\n")
        f.write(subtitle["start"] + " --> " + subtitle["end"] + "\n")
        f.write(subtitle["dialogue"] + "\n\n")

def format_timestamp(seconds):
    hours = int(seconds / 3600)
    minutes = int((seconds % 3600) / 60)
    seconds = int(seconds % 60)
    milliseconds = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"

def main():
    if len(sys.argv) < 2:
        print("Usage: python script_name.py video_file.mp4")
        return
    
    file_name = sys.argv[1]

    if not path.exists(file_name):
      print("Error: File does not exist.")
      return

    VIDEO_FILE = path.abspath(file_name)
    clip = VideoFileClip(VIDEO_FILE)

    extension_index = file_name.rfind(".")
    if extension_index != -1:
        base_name,ext = path.splitext(file_name)
        proper_name = base_name + "_audio.wav"
        output_srt_file = base_name + ".srt"
        
        # Write audio to the proper_name file
        clip.audio.write_audiofile(proper_name, codec='pcm_s16le')

        audio = whisper.load_audio(proper_name)
        model = whisper.load_model("base")
        result = whisper.transcribe(model, audio, language="en")
        transcribed_dialogues = [item['text'] for item in result['segments']]

        subtitles = generate_subtitles(transcribed_dialogues)
        remove(output_srt_file)
        for subtitle in subtitles:
            print(str(subtitle["index"]) + "\n")
            print(f"{subtitle['start']} --> {subtitle['end']}")
            print(subtitle['dialogue'])
 
            write_srt(subtitle, output_srt_file)  # Write subtitles to the SRT file line by line

        remove(proper_name)
        print("Subtitles generated and saved as", output_srt_file)
    else:
        print("Invalid file name format.")
        return 

if __name__ == "__main__":
    main()
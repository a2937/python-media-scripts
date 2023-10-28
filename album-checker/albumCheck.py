#!/usr/bin/env python # [1]
import sys
import os
import openpyxl
from openpyxl.styles.fills import PatternFill
from openpyxl.styles import colors

location = os.path.abspath(sys.argv[1])
# get all files' and folders' names in the current directory
artistNames = os.listdir(location)
Dictionary = {}

wb = openpyxl.Workbook()
sheet = wb.active
sheet.title = "Albums"

# Headers
sheet['A1'] = "Artist"
sheet['B1'] = "Album"
sheet['C1'] = "Song"
sheet['D1'] = "Status"
sheet['E1'] = 'Notes'
currentRow = 2


def is_movie_file(path):
    valid_extensions = [".mkv", ".avi", ".mp4", ".webm", ".m4v"]
    if os.path.isfile(path):
        for ext in valid_extensions:
            if path.lower().endswith(ext):
                return True
    return False


def process_artist_folder(artist_path, artist_name,  current_row, sheet):
    potential_album_names = os.listdir(artist_path)

    yellow_fill = PatternFill(
        patternType='solid', fgColor=colors.Color(rgb='FFFF00'))

    for album in potential_album_names:
        album_path = os.path.join(artist_path, album)
        if os.path.isdir(album_path):
            song_list = os.listdir(album_path)
            album_song_count = 0
            for song in song_list:

                if is_movie_file(os.path.join(album_path, song)):
                    album_song_count += 1
                    sheet.cell(row=current_row, column=1).value = artist_name
                    sheet.cell(row=current_row, column=2).value = album
                    sheet.cell(row=current_row,
                               column=3).value = album_song_count

                    if album_song_count > 3:
                        sheet.cell(row=current_row,
                                   column=2).fill = yellow_fill
                        sheet.cell(row=current_row, column=4).value = "Full"
                    else:
                        sheet.cell(row=current_row,
                                   column=4).value = "Incomplete"


def main():
    if len(sys.argv) < 2:
        print("Usage: python script_name.py directory_path")
        return

    location = os.path.abspath(sys.argv[1])

    wb = openpyxl.Workbook()
    sheet = wb.active
    sheet.title = "Albums"


    currentRow = 2


    # Headers
    sheet['A1'] = "Album"
    sheet['B1'] = "Artist"
    sheet['C1'] = "Song"
    sheet['D1'] = "Status"

    artist_names = os.listdir(location)

    for artist_name in artist_names:
        artist_path = os.path.join(location, artist_name)
        if os.path.isdir(artist_path):
            process_artist_folder(artist_path, artist_name, sheet)
            currentRow += 1

    output_file = 'album_list.xlsx'
    wb.save(output_file)
    print("Album list saved as", output_file)


if __name__ == "__main__":
    main()

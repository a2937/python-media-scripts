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

def isMusicFile(path):
    # is it a song
    print(path)
    if os.path.isfile(path) and (path.lower().endswith(".mp3") or path.lower().endswith(".m4a")
                                 or path.lower().endswith(".flac")):
        return True
    else:
        return False


for artist in artistNames:  # loop through all the files and folders
    potArtistPath = os.path.join(os.path.abspath(location), artist)
    if os.path.isdir(potArtistPath):
        # Grab every album by that artist
        potentialAlbumNames = os.listdir(potArtistPath)
        for album in potentialAlbumNames:  # Look through every album
            potAlbumPath = os.path.join(os.path.abspath(
                potArtistPath), album)  # Get the path of the album
            if os.path.isdir(potAlbumPath):
                songList = os.listdir(potAlbumPath)
                albumSongCount = 0
                Dictionary[artist + ";" + album] = 0
                for song in songList:
                    musicPath = os.path.join(os.path.abspath(
                        potAlbumPath), song)
                    if (isMusicFile(musicPath)):
                        albumSongCount += 1

                        Dictionary[artist + ";" + album] = albumSongCount

yellowFill = PatternFill(patternType='solid', fgColor=colors.Color(rgb='FFFF00'))
#f = open('albumSongCount.txt', 'w', encoding='utf-8')
for index, (artist, count) in enumerate(sorted(Dictionary.items())): 
    currentRow += 1
    artistTrueName = artist.split(";")[0]
    albumName = artist.split(";")[1]
    sheet['A' + str(currentRow)] = artistTrueName
    sheet['B' + str(currentRow)] = albumName
    if count > 3 : 
        sheet.cell(row=currentRow,column=2).fill = yellowFill
        sheet['D' + str(currentRow)] = "Full"
    else:
        sheet['D' + str(currentRow)] = "Incomplete"
    sheet['C' + str(currentRow)] = count
   

#  f.write("%s ; %d \n" % (artist, count))
#f.close()


wb.save('album_list.xlsx')
#!/usr/bin/env python # [1]
import sys
import os
import cv2

location = sys.argv[1]

# get all files' and folders' names in the current directory
filenames = os.listdir(location)
Dictionary = {}


def isMovieFile(path):
    print(path)
    # is it a movie
    if os.path.isfile(path) and (path.lower().endswith(".mkv") or path.lower().endswith(".avi") or path.lower().endswith(".mp4")
                                 or path.lower().endswith(".webm") or path.lower().endswith(".m4v")):
        return True
    else:
        return False


for filename in filenames:  # loop through all the files and folders
    # check whether the current object is a folder or not
    potMoviePath = os.path.join(os.path.abspath(location), filename)
    if os.path.isdir(potMoviePath):
        # Grab everything in that directory
        potentialFileNames = os.listdir(potMoviePath)
        fullNames = []
        for i in potentialFileNames:
            # Get the full path to everything
            fullNames.append(os.path.join(os.path.abspath(
                location), filename, potMoviePath, i))
        movies = list(filter(isMovieFile, fullNames))
        # Determine if there actually is a movie in there
        if (movies.__len__() > 0):
            movieName = movies[0]
        else:
            print("No movie found")
            Dictionary[filename] = "Unknown"
            continue
        moviePath = os.path.join(
            os.path.abspath(location), filename, movieName)
        try:
            vid = cv2.VideoCapture(moviePath)
            if vid.isOpened():
                print(moviePath)
                height = vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
                width = vid.get(cv2.CAP_PROP_FRAME_WIDTH)
                vid.release()
                if (height > 720 and width > 576):
                    Dictionary[filename] = "Blu-ray"
                else:
                    Dictionary[filename] = "DVD"
            else:
                print("Cannot read : " + moviePath + " properly")
                Dictionary[filename] = "Unknown"

        except:
            Dictionary[filename] = "Unknown"

cv2.destroyAllWindows()
# To save Folders names to a file.
f = open('fileListings.txt', 'w', encoding='utf-8')
for index, (filename, definition) in enumerate(Dictionary.items()):
    f.write("%s : %s \n" % (filename, definition))

f.close()

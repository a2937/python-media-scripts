#!/usr/bin/env python # [1]
import sys
import os
import cv2

location = os.path.abspath(sys.argv[1])

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
                size = "?"
                if height < 460:
                    size = "SD"
                elif height >= 460 and height <= 480:
                    size = "480p"
                elif height > 480 and height <= 720:
                    size = "720p"
                elif height > 720 and height <= 1080:
                    size = "1080p"
                else:
                    size = "4K"
                vid.release()
                if (height > 720 and width > 576):
                    Dictionary[filename] = ["Blu-ray",height,size]
                else:
                    Dictionary[filename] = ["DVD",height,size]
            else:
                print("Cannot read : " + moviePath + " properly")
                Dictionary[filename] = ["Unknown",0,"Unknown"]

        except:
            Dictionary[filename] = ["Unknown",0,"Unknown"]

cv2.destroyAllWindows()
# To save Folders names to a file.
f = open('fileListings.txt', 'w', encoding='utf-8')
for index, (filename, size) in enumerate(sorted(Dictionary.items())):
    f.write("%s : %s : %d : %s \n" % (filename, size[0],size[1],size[2]))

f.close()

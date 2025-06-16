import sys
import os


def main():
    location = "" 
    if len(sys.argv) < 2:
        location = input("Enter file path>")
    else :
        location = os.path.abspath(sys.argv[1])
    file = open(location) 
    data = file.read()
    while data:
      print(data)
      data = file.read(3)
    file.close()


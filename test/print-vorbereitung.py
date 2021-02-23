import RPi.GPIO as GPIO
import time

#--------------------define location to call the print-method--------------------------
location = "C:\Users\rpe\Pictures"
print(location)



def print(path):
    #Read out gcode-filenames from the "path"
    gcodefiles = ["blue.gcode", "red.gcode", "green.gcode"]
    #Print every gcode-file by calling the changecolor-, embroiderystart-, cncstart-, cncstop- and embroiderystop-methods in a clever order
    for x in gcodefiles:
        #Call changecolor method
        changecolor(gcodefiles[x].split(".gcode"))
        #Call expectedduration method
        duration = expectedduration(gcodefiles[x])
        #Call embroiderystart method
        embroiderystart()
        #Call cncstart method
        cncstart(path, x)
        #After the duration-time, call embroiderystop- and cncstop methods
        time.sleep(duration)
        embroiderystop()
        cncstop()
        #Call cutthread method - not a must (can also use the changecolor method)

#
def changecolor(color):
    #

#
def expectedduration(color):
    #

#
def embroiderystart():
    #

#
def cncstart(path, name):
    #

#
def embroiderystop():
    #

#
def cncstop():
    #
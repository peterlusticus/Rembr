#Richard P - 05/02/2021
#This library convert a 2-axis-gcode-file into stepper steps
#It supply coordinates in a text file called "test.txt" - file needs specific format: 
#G01 X10 Y15
#G01 X20 Y25

#Depending librarys
import RPi.GPIO as GPIO
import time

#Global var's
filename = 'test.txt'

#Open gcode-file and replace coordinates wit their steps
def CONVERT():
        #Local var's
        file = open(filename, "r")
        new_file_content = ""
        Cx_before = 0
        Cy_before = 0
        i = 0
        #Replace coordinates wit their steps in every line 
        for line in file:
                if "X" and "Y" in line:
                        #Read out X- and Y-value
                        Cx = (line.split(' ')[1])
                        Cx = (Cx[1:])
                        Cx = float(Cx)
                                
                        Cy = (line.split(' ')[2]) 
                        Cy = (Cy[1:])
                        Cy = float(Cy)
                                
                        #Calculate Steps
                        Sx = (Cx - Cx_before)
                        Sy = (Cy - Cy_before)
                        print("X:  " + str(Cx) + " - " + str(Cx_before) + " = " + str(Sx))
                        print("Y:  " + str(Cy) + " - " + str(Cy_before) + " = " + str(Sy))

                        #Scale
                        #Sx = Sx*100
                        #Sy = Sy*100

                        #Replace coordinates with steps
                        #stripped_line = line.strip()
                        #new_line = stripped_line.replace(str(Cx), str(Sx))
                        #new_line = new_line.replace(str(Cy), str(Sy))
                        new_line = "G01 X"+str(int(Sx))+" Y"+str(int(Sy))
                        new_file_content += new_line +"\n"
                        #print("4) Content:" + "\n" + new_file_content)
                                
                        #Save X- and Y-value
                        Cx_before = Cx
                        Cy_before = Cy
                        i += 1
                        print(str(i))
                                
        file.close()
        time.sleep(5)
        #Write content into file
        writing_file = open(filename, "w")
        print(new_file_content)
        writing_file.write(new_file_content)
        writing_file.close()

CONVERT()

exit()

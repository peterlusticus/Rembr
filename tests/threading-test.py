import time
import threading

def embroideryStart():
    for x in range(10):
        time.sleep(.5)
        print("[FUNCTION] embroideryStart(): "+x)
    print("[FUNCTION] embroideryStart(): end")

def cncStart():
    for x in range(5):
        time.sleep(.5)
        print("[FUNCTION] cncStart(): "+x)
    print("[FUNCTION] cncStart(): end")

def printColor():
    embroidery = threading.Thread(target=embroideryStart)
    cnc = threading.Thread(target=cncStart)
    embroidery.start()
    time.sleep(.1)
    cnc.start()
    embroidery.join()
    cnc.join()
    print("[FUNCTION] printColor(): end")
    time.sleep(.1)

def execute():
    printColor()
    print("[FUNCTION] execute(): end")
    
execute()
GPIO.cleanup()
exit()

#Erwartete Konsolenausgabe:
#[FUNCTION] embroideryStart(): 0
#[FUNCTION] cncStart(): 0
#[FUNCTION] embroideryStart(): 1
#[FUNCTION] cncStart(): 1
#[FUNCTION] embroideryStart(): 2
#[FUNCTION] cncStart(): 2
#[FUNCTION] embroideryStart(): 3
#[FUNCTION] cncStart(): 3
#[FUNCTION] embroideryStart(): 4
#[FUNCTION] embroideryStart(): end
#[FUNCTION] cncStart(): 4
#[FUNCTION] cncStart(): 5
#[FUNCTION] cncStart(): 6
#[FUNCTION] cncStart(): 7
#[FUNCTION] cncStart(): 8
#[FUNCTION] cncStart(): 9
#[FUNCTION] cncStart(): end
#[FUNCTION] printColor(): end
#[FUNCTION] execute(): end

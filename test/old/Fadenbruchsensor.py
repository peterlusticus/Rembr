#Fadenbruchsensor.py
fbs = 26
GPIO.setup(fbs, GPIO.IN)

if GPIO.input(fbs): #Fadenbruchsensor aktiv wenn faden gebrochen
        execute(pause)
print"Faden Gebrochen/ Problem mit fadenführung/ Schpannung des Fadens"

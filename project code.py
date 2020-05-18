import RPi.GPIO as GPIO
from time import sleep, time
from Tkinter import *
from math import trunc

lowset = 6      #cup is full  
midset = 14 #cup is middle 
highset = 22    #cup needs to be refilled
toofar= 33

#set the RPi to the Broadcom pin layout
GPIO.setmode(GPIO.BCM)

#GPIO pins
REDLED = 16
GREENLED = 13
BLUELED = 12
TRIG = 18  #the sensors TRIG pin
ECHO = 27  #the sensors ECHO pin

timed = 0

GPIO.setup(REDLED, GPIO.OUT)
GPIO.setup(GREENLED, GPIO.OUT)
GPIO.setup(BLUELED, GPIO.OUT)
GPIO.setup(TRIG, GPIO.OUT)  #TRIG is an output
GPIO.setup(ECHO, GPIO.IN)   #ECHO is an input

class GUItest(Frame):
    def __init__(self,master):
        Frame.__init__(self,master)
        self.master=master
    def setupGUI(self):
        L1 = Label(self.master, text="Refill not needed.")
        L1.grid(row = 0, column = 0, sticky = N+E+S+W)

        img = PhotoImage(file="GUIhigh.gif")
        F1 = Label(self.master, image=img)
        F1.image = img
        F1.grid(row = 1, column = 0, sticky = N+S+E+W)
    
# uses the sensor to calculate the distance to an object
def getDistance():
    #trigger the sensor by setting it high for a short time and then setting it low
    GPIO.setmode(GPIO.BCM)
    global timed
    global timer

    GPIO.setup(REDLED, GPIO.OUT)
    GPIO.setup(GREENLED, GPIO.OUT)
    GPIO.setup(BLUELED, GPIO.OUT)
    GPIO.setup(TRIG, GPIO.OUT)  #TRIG is an output
    GPIO.setup(ECHO, GPIO.IN)   #ECHO is an input

    sleep(1)

    GPIO.output(TRIG, GPIO.HIGH)
    sleep(0.00001)
    GPIO.output(TRIG, GPIO.LOW)
    #wait for the ECHO pin to read high
    #once the ECHO pin is high, the start time is set
    #once the ECHO pin is low again, the end time is set
    while(GPIO.input(ECHO) == GPIO.LOW):
        start = time()
    while(GPIO.input(ECHO) == GPIO.HIGH):
        end = time()
    #calculate the duration that the ECHO pin was high
    #this is how long the pulse took to get from the sensor to the object and back
    duration = end - start
    #calculate the total distance that the pulse traveled by factoring in the speed of sound
    distance = duration * 343
    #the distance from the sensor to the object is half of the distance
    distance /= 2
    #convert from m to cm
    distance *= 100
    print distance
    if(distance > lowset and distance < midset):
        timed=0
        GPIO.output(GREENLED, True)
        GPIO.output(BLUELED, False)
        GPIO.output(REDLED, False)            
        img = PhotoImage(file="GUIhigh.gif")
        F1 = Label(t.master, image=img)
        F1.image = img
        F1.grid(row = 1, column = 0, sticky = N+S+E+W)
        L1 = Label(t.master, text="Refill not needed.")
        L1.grid(row = 0, column = 0, sticky = N+E+S+W)
        
    if(distance > midset and distance < highset):
        timed=0
        GPIO.output(BLUELED, True)
        GPIO.output(GREENLED, False)
        GPIO.output(REDLED, False)
        img = PhotoImage(file="GUImid.gif")
        F2 = Label(t.master, image=img)
        F2.image = img
        F2.grid(row = 1, column = 0, sticky = N+S+E+W)
        L2 = Label(t.master, text="Refill needed soon.")
        L2.grid(row = 0, column = 0, sticky = N+E+S+W)
        
    if(distance > highset and distance < toofar):
        if(timed==1):
            L4 = Label(t.master, text="Refill needed for {} seconds.".format(trunc(time()-timer)))
            L4.grid(row = 0, column = 0, sticky = N+E+S+W)
            
        if(timed == 0):
            L3 = Label(t.master, text="Refill needed." )
            L3.grid(row = 0, column = 0, sticky = N+E+S+W)
            timed=1
            timer=time()
            
        GPIO.output(REDLED, True)
        GPIO.output(BLUELED, False)
        GPIO.output(GREENLED, False)
        img = PhotoImage(file="GUIlow.gif")
        F3 = Label(t.master, image=img)
        F3.image = img
        F3.grid(row = 1, column = 0, sticky = N+S+E+W)      
        
        
    window.update()
    window.after(2000, getDistance())
    
GPIO.output(18, GPIO.LOW)
sleep(1)
GPIO.cleanup()

window = Tk()
t=GUItest(window)
t.setupGUI()
getDistance()
window.mainloop()

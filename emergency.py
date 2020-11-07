import time
import os
import sys
from random import randint 
from queue import PriorityQueue

class Main:

    def __init__(self):        
        self.currentTime    = 0        
        self.fileName       = ""
        self.patNum         = 28064212       
        self.remainingRooms = 3       
        self.queue          = PriorityQueue() # Holds events
        self.nextAssessmentTime  = 0        
        self.pastPatients   = [] # Used for patient summary
    
    def getfile(self):
        self.fileName = input("Enter local filename: ")
        print("You entered the file " + self.fileName)

    def start(self):        
        self.getfile()
        try:
            file = open(self.fileName,"r")
        except OSError:
            print("Error opening file '" + self.fileName + "' please enter a valid file name from the current directory.")
            sys.exit()
        
        # Creates an array of each line in the file
        patients = file.readlines()        
        j = 0 # Used as an offset for patient IDs 
        for line in patients:
            # Initializing variables
            i = 0           
            arivalTime = ""
            code = ""
            treatmentTime = ""
            length = len(line)
            # Gets the first number
            # Loops until new line is found (Applies to all loops)
            # Grabs values that aren't whitespace (Applies to all loops)
            while line[i] != '\n' :
                if(line[i].isspace()):
                    break
                else:
                    temp = line[i]
                    arivalTime += temp
                    i+=1
            # Gets the "code"
            i+=1
            while line[i] != '\n' :
                if(line[i].isspace()):
                    break
                else:
                    temp = line[i]
                    code += temp
                    i+=1
            # Gets the treatmentTime
            i+=1
            while i < length and line[i] != '\n' :
                if(line[i].isspace()):
                    break
                else:
                    temp = line[i]
                    treatmentTime += temp
                    i+=1
            # Creates object and prints out the input files info
            # Casts strings to ints where needed
            tempID = (self.patNum + j)            
            temp = Patient(int(arivalTime),code,int(treatmentTime),tempID)
            # Sets arrival time
            if j == 0:
                self.currentTime += int(arivalTime)
            elif j > 0:
                self.currentTime += ( int(arivalTime) - self.currentTime )
            # Patient arrived           
            self.arrival(temp)                    
            j+=1     
            # time.sleep(1) # Used for debugging  
             
    def arrival(self,patient):
        temp = "Time " + str(self.currentTime) + ": " + str(patient.idNum) + " " + str(patient.code) + " arrives"  
        self.queue.put(temp,patient.arivalTime)
          
        if patient.code == "W":
            self.nextAssessmentTime = self.currentTime + 4            
            self.assessment(patient)
        else:
            patient.setPriortiy(1)
            self.waitingRoom(patient)  
            pass
        

    def assessment(self,patient):
        # Determines if there is currently a patient beign assessed
        finishTime = self.currentTime + 4

        if finishTime != self.nextAssessmentTime: # assessment in progress at this time            
            futureTime = finishTime - self.nextAssessmentTime
            temp = "Time " + str(futureTime + finishTime) + ": " + str(patient.idNum) + " starting assessment"
            patient.assessmentTime += futureTime + finishTime
            self.queue.put(temp,(futureTime + finishTime))
            # Gives patient a random priority level
            rand = randint(2,5)
            patient.setPriortiy(rand)
            # Incremets sys time by 4s
            futureTime += 4
            # Adds patient to waiting room queue                
            temp = "Time " + str(futureTime + finishTime) + ": " + str(patient.idNum) + " assessment complete priority now level " + str(patient.priority)
            self.queue.put(temp,futureTime + finishTime)

        else: # No assessment occuring            
            temp = "Time " + str(self.currentTime) + ": " + str(patient.idNum) + " starting assessment"
            patient.assessmentTime += self.currentTime
            self.queue.put(temp,self.currentTime)
            # Gives patient a random priority level
            rand = randint(2,5)
            patient.setPriortiy(rand)
            # Incremets sys time by 4s
            self.currentTime += 4
            # Adds patient to waiting room queue                 
            temp = "Time " + str(self.currentTime) + ": " + str(patient.idNum) + " assessment complete priority now level " + str(patient.priority)      
            self.queue.put(temp,self.currentTime)

        self.waitingRoom(patient)

    def waitingRoom(self,patient):
        # Enters waiting room
        temp = "Time " + str(self.currentTime) + ": " + str(patient.idNum) + " (Priority " + str(patient.priority) + ") entered the waiting room"
        self.queue.put(temp,self.currentTime)
                                       
        self.remainingRooms -= 1
        temp = "Time " + str(self.currentTime) + ": " + str(patient.idNum) + " (Priority " + str(patient.priority) + ") starting treatment " + str(self.remainingRooms) + " rm(s) remaining"
        self.queue.put(temp,self.currentTime)
        self.treatment(patient)                
    
    def treatment(self,patient):
        # Finish treatment
        finishTime = self.currentTime + patient.treatmentTime
        temp = "Time " + str(finishTime) + ": " + str(patient.idNum) + " (Priority " + str(patient.priority) + ") finished treatment"     
        self.queue.put(temp,finishTime)

        if patient.priority > 1:
            finishTime += 1            
            self.remainingRooms += 1
            temp = "Time " + str(finishTime) + ": " + str(patient.idNum) + " (Priority " + str(patient.priority) + ") departs " + str(self.remainingRooms) + " rm(s) remaining"
            self.queue.put(temp,finishTime)  
            patient.departTime += finishTime         
        else:
            # Hospital admision
            finishTime += 3            
            temp = "Time " + str(finishTime) + ": " + str(patient.idNum) + " (Priority " + str(patient.priority) + ") admitted to hospital"           
            self.queue.put(temp,finishTime)    
            self.remainingRooms += 1
            temp = "Time " + str(finishTime) + ": " + str(patient.idNum) + " (Priority " + str(patient.priority) + ") departs " + str(self.remainingRooms) + " rm(s) remaining"
            self.queue.put(temp,finishTime)   
            patient.departTime += finishTime
        self.pastPatients.append(patient)

    def viewEvents(self):        
        while not self.queue.empty():
            print(self.queue.get())
            
    def patientSummary(self):
        print("")        
        print("Patient Priority   Arrival Assessment   Treatment   Departure  Waiting")
        print("Number               Time       Time    Required        Time     Time")
        print("-----------------------------------------------------------------------")
        avgWait = 0
        for x in self.pastPatients:
            avgWait += x.waitTime
            print(str(x.idNum) + "        " + str(x.priority) + "        " + str(x.arivalTime) + "        " + str(x.assessmentTime) + "        " + str(x.treatmentTime) + "        " + str(x.departTime) + "        " + str(x.waitTime))
        print("Total Patients: " + str(len(self.pastPatients)))
        avgWait /= len(self.pastPatients)
        print("Average wait time: " + str(avgWait))

class Patient:

    def __init__(self,arivalTime,code,treatmentTime,idNum):        
        self.arivalTime      = arivalTime 
        self.code            = code
        self.treatmentTime   = treatmentTime   
        self.idNum           = idNum
        self.priority        = 0
        self.waitTime        = 0
        self.assessmentTime  = 0
        self.departTime      = 0        

    def viewInfo(self):
        print(str(self.arivalTime) + " " + self.code + " " + str(self.treatmentTime) + " " + str(self.idNum))

    def getCode(self):
        return self.code

    def getID(self):
        return self.idNum

    def getArivalTime(self):
        return self.arivalTime

    def setPriortiy(self,num):
        self.priority += num

if __name__ == "__main__":
    prog = Main()
    prog.start()
    prog.viewEvents()
    prog.patientSummary()
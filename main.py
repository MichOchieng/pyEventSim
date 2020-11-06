import time
from random import randint 
from queue import PriorityQueue

class Main:

    def __init__(self):        
        self.currentTime    = 0
        self.arrivalTime    = 0
        self.fileName       = ""
        self.patNum         = 28064212
        self.patients       = []
        self.queue          = PriorityQueue()
        self.remainingRooms = 3
        self.waitStart      = 0
        
    
    def getfile(self):
        self.fileName = input("Enter local filename: ")
        print("You entered the file " + self.fileName)

    def arrival(self):        
        self.getfile()
        file = open(self.fileName,"r") 
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
            self.arrived(temp)                  
            j+=1     
            # time.sleep(1) # Used for debugging   
        for ppl in self.patients:
            self.arrived(ppl)     

    def arrived(self,patient):
        print("Time " + str(self.currentTime) + ": " + str(patient.idNum) + " " + str(patient.code) + " arrives")
        if patient.code == 'E':
            # Goto waiting room
            patient.setPriortiy(1)
            self.queue.put(patient,1)                        
            self.waitingRoom()  
        elif patient.code == 'W':
            # Goto assesment Queue
            self.assessment(patient)                 
            self.waitingRoom()           
        else:
            print("Patient " + str(patient.idNum) + " does not have an arival code.")

    def assessment(self,patient):
        print("Time " + str(self.currentTime) + ": " + str(patient.idNum) + " (Priority " + str(patient.priority) + ") starting assessment")
        # Gives patient a random priority level
        rand = randint(1,5)
        patient.setPriortiy(rand)
        # Incremets sys time by 4s
        self.currentTime += 4
        # Adds patient to waiting room queue
        self.queue.put(patient,rand)       
        print("Time " + str(self.currentTime) + ": " + str(patient.idNum) + " assessment complete priority now level " + str(patient.priority)) 
        
    def waitingRoom(self):
        temp = self.queue.get()
        print("Time " + str(self.currentTime) + ": " + str(temp.idNum) + " (Priority " + str(temp.priority) + ") entered the waiting room")
        if self.remainingRooms > 0:
            self.remainingRooms -= 1 
            print("Time " + str(self.currentTime) + ": " + str(temp.idNum) + " (Priority " + str(temp.priority) + ") starting treatment " + str(self.remainingRooms) + " rm(s) remaining")  
            self.treatment(temp)                                 
        else:
            print("gotta wait bucko")
            
        

    def treatment(self,patient):        
        # Finish treatment
        self.currentTime += patient.treatmentTime
        print("Time " + str(self.currentTime) + ": " + str(patient.idNum) + " (Priority " + str(patient.priority) + ") finished treatment")
        self.remainingRooms += 1
        if patient.priority > 1:
            self.currentTime += 1
            print("Time " + str(self.currentTime) + ": " + str(patient.idNum) + " (Priority " + str(patient.priority) + ") departs " + str(self.remainingRooms) + " rm(s) remaining")            
        else:
            # Hospital admision
            self.currentTime += 3
            print("Time " + str(self.currentTime) + ": " + str(patient.idNum) + " (Priority " + str(patient.priority) + ") admitted to hospital")
            self.currentTime += 1
            print("Time " + str(self.currentTime) + ": " + str(patient.idNum) + " (Priority " + str(patient.priority) + ") departs " + str(self.remainingRooms) + " rm(s) remaining")
            

class Patient:

    def __init__(self,arivalTime,code,treatmentTime,idNum):        
        self.arivalTime      = arivalTime 
        self.code            = code
        self.treatmentTime   = treatmentTime   
        self.idNum           = idNum
        self.priority        = 0
        self.waitTime        = 0

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
    prog.arrival()
    
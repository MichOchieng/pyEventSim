import time
from random import randint 
from queue import PriorityQueue
class Main:

    def __init__(self):        
        self.currentTime = 0
        self.fileName = ""
        self.patNum = 28064212
        self.queue = PriorityQueue()
        
    
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
            if i == 0:
                self.currentTime += int(arivalTime)
            elif i > 0:
                self.currentTime += ( int(arivalTime) - self.currentTime )

            # Patient arrived            
            print("Time " + str(self.currentTime) + ": " + str(temp.idNum) + " " + str(temp.code) + " arrives")
            if code == 'E':
                # Goto waiting room
                temp.setPriortiy(1)
                self.queue.put(temp,1)
                self.waitingRoom() 
            elif code == 'W':
                # Goto assesment Queue
                self.assessment(temp)      
                self.waitingRoom()           
            else:
                print("Patient " + str(tempID) + " does not have an arival code.")                  
            j+=1     
            # time.sleep(1) # Used for debugging        

    def assessment(self,patient):
        # Gives patient a random priority level
        rand = randint(0,6)
        patient.setPriortiy(rand)
        # Incremets sys time by 4s
        self.currentTime += 4
        # Adds patient to waiting queue
        self.queue.put(patient,rand)
        
    def waitingRoom(self):
       temp = self.queue.get()
       temp.viewInfo()

class Patient:

    def __init__(self,arivalTime,code,treatmentTime,idNum):        
        self.arivalTime      = arivalTime 
        self.code            = code
        self.treatmentTime   = treatmentTime   
        self.idNum           = idNum
        self.priority        = 0

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
    
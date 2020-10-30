import time

class Main:

    def __init__(self):        
        self.currentTime = 0
        self.fileName = ""
        self.patNum = 28064212
    
    def getfile(self):
        self.fileName = input("Enter local filename: ")
        print("You entered the file " + self.fileName)

    def arrival(self):        
        self.getfile()
        file = open(self.fileName,"r") 
        # Creates an array of each line in the file
        patients = file.readlines()        
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
            temp = Patient(int(arivalTime),code,int(treatmentTime))
            temp.viewInfo()            
            time.sleep(1) # Used for debugging


class Patient:

    def __init__(self,arivalTime,code,treatmentTime):        
        self.arivalTime      = arivalTime 
        self.code            = code
        self.treatmentTime   = treatmentTime   
        self.idNum           = 0

    def viewInfo(self):
        print(str(self.arivalTime) + " " + self.code + " " + str(self.treatmentTime))


if __name__ == "__main__":
    prog = Main()
    prog.arrival()
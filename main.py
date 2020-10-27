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
            # Temp solution for parsing
            i = 0
            # Gets the first number
            while line != ' ':
                temp = line[i]
                arivalTime += temp
                i+=1
            # Gets the code

            # Gets the treatmentTime

            # Creates object and adds to queue
                
            print(arivalTime)
            time.sleep(1)


class Patient:

    def __init__(self,arivalTime,code,treatmentTime):        
        self.arivalTime      = arivalTime 
        self.code            = code
        self.treatmentTime   = 0   
        self.idNum           = 0
    
if __name__ == "__main__":
    prog = Main()
    prog.arrival()
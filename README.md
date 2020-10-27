# Emergency Room Simulation

This program simulates the processing of patients through a
hospital emergency room, using a discrete event simulation. The ultimate goal is to determine how
long patients have to wait to see a doctor, and how their time in the emergency ward in general is
spent.
As of right now this program expect CORRECT input from a file.

## Input file example

  18 E 2  
  18 W 3  
  19 E 28  
  20 W 19  
  20 E 36  
  21 W 1  
  24 E 10  
  
 Where:  
 * First column is the arival time   
 * Second column is the arrival code E (emergency) or W (wait)  
 * Third column is the total treatment time  

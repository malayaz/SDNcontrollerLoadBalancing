##########################################################################################
#                                                                                        #
#                                                                                        #
#       File Name ----- SuperController_collection_accumulation.py                       #
#                                                                                        #
#       Purpose ----- Listens on socket and every 10 secs collects the average 		 #	
#			number of flow requests for superController_average_accumulation #	
#                                                                                        #
#       Contributors  ----- Rushikesh , Malayaz , Priya , Neha                           #
#                                                                                        #
#       Revison Version ----- Latest                                                     #
#                                                                                        #      
#                                                                                        #
##########################################################################################




from __future__ import print_function
import socket               # Import socket module
import pickle
import threading
iterations = 5


list_created_c1 = [["controller",1]]
list_created_c2 = [["controller",2]]
list_created_c3 = [["controller",3]]


switchid = [0,0,0,0,0]
switchidvalue = [0,0,0,0,0]
controller1_count = 0
controller2_count = 0
controller3_count = 0

#########################################################################################
#                                                                                       #
#                                                                                       #
#       Function Name --- load_calculator		                                #
#                                                                                       #
#       Arguments ---- A load notification from Controller in a list		        #
#                                                                                       #
#       Purpose ----   Calculates the average load on a controller over a time          #
#                                    period of 10s					#
#                                                                                       #
#       Return Value ---- NONE			                                        #
#                                                                                       #
#                                                                                       #
#                                                                                       #
#                                                                                       #
#########################################################################################


def load_calculator(listfetched):
    global list_created_c1
    global list_created_c2 
    global list_created_c3
    global iterations
    global controller1_count 
    global controller2_count 
    global controller3_count 
    iterator = 0
    length = len(listfetched) #listfetched should have single line entry #
    if (length > 1):
        i=0
        controllerid = listfetched[0][1]
        length = length-1 # to account for controller
        while ( (i+1) <= length ):
            switchid[i] = listfetched[i+1][0]
            switchidvalue[i]= listfetched[i+1][1]
            

            if ( controllerid == '1'):
                for sublist in list_created_c1:
                    if switchid[i] in sublist[0]:
                        index = [y[0] for y in list_created_c1].index(switchid[i])			
                        list_created_c1[index][1] = list_created_c1[index][1] + switchidvalue[i]/iterations # cumulative
                        iterator = 1
			controller1_count = controller1_count + 1
                        break
                    else:
                        continue
                if ( iterator == 0):
                    new_switch_id_list = [switchid[i],switchidvalue[i]]
                    list_created_c1.append( new_switch_id_list)
                    
            elif ( controllerid == '2'):
                 for sublist in list_created_c2:
                    if switchid[i] in sublist[0]:
                        index = [y[0] for y in list_created_c2].index(switchid[i])
                        list_created_c2[index][1] =  list_created_c2[index][1] + switchidvalue[i]/iterations
                        iterator = 1
			controller2_count = controller2_count + 1
                        break
                    else:
                        continue
                 if ( iterator == 0):
                        new_switch_id_list = [switchid[i],switchidvalue[i]]
                        list_created_c2.append( new_switch_id_list)
                        
            elif ( controllerid == '3'):
		 for sublist in list_created_c3:
                    if switchid[i] in sublist[0]:
                        index = [y[0] for y in list_created_c3].index(switchid[i])
                        list_created_c3[index][1] = list_created_c3[index][1]+ switchidvalue[i]/iterations
                        iterator = 1
			controller3_count = controller3_count + 1
                        break
                    else:
                        continue
                 if ( iterator == 0):
                        new_switch_id_list = [switchid[i],switchidvalue[i]]
                        list_created_c3.append( new_switch_id_list)
  
            i=i+1   
            
    else:
        nothing = 1 


    print (list_created_c1,end='')
    print (list_created_c2,end='')
    print (list_created_c3,end='')
    print ('\033[F')

#########################################################################################
#                                                                                       #
#                                                                                       #
#       Function Name --- flush_all                                                     #
#                          	                                                        #
#       Arguments ---- NONE        	                                                #
#                                                                                       #
#       Purpose ----   Reinitialize the list for next 10s		                #
#                                  load balancing					#
#                                                                                       #
#       Return Value ---- NONE			                                        #
#                                                                                       #
#                                                                                       #
#                                                                                       #
#                                                                                       #
#########################################################################################

def flush_all():
	length_c1 = len(list_created_c1)
	length_c2 = len(list_created_c2)
	length_c3 = len(list_created_c3)
	controller1_count = 0	
	controller2_count = 0	
	controller3_count = 0	
	i = 1
	t = threading.Timer(10,flush_all)
	t.start()

	fp = open("c1.pkl","wb")
	pickle.dump(list_created_c1,fp)
	fp.close()
	fp = open("c2.pkl","wb")
	pickle.dump(list_created_c2,fp)
	fp.close()
	fp = open("c3.pkl","wb")
	pickle.dump(list_created_c3,fp)
	fp.close()
	while( i < length_c1):
		list_created_c1[i][1] = 0	
		i = i+1
			
	i = 1
        while( i < length_c2):
        	list_created_c2[i][1] = 0
        	i = i+1

	i = 1
        while( i < length_c3):
        	list_created_c3[i][1] = 0
                i = i+1
	
	print ('\r')
	print (list_created_c1,end=' ')
	print (list_created_c2,end=' ')
	print (list_created_c3)
			
	flush_counter = -1

	flush_counter = flush_counter + 1

#################socket code ############################################
flush_counter = 1
if __name__ == '__main__':
	flush_all()
	s = socket.socket()         # Create a socket object
	host = '' # Get local machine name
	port = 65511           # Reserve a port for your service.
	s.bind((host, port))        # Bind to the port
	s.listen(5)                 # Now wait for client connection.
	while True:
   		c, addr = s.accept()     # Establish connection with client.
   
   		listfetched = pickle.loads(c.recv(1024))	
   		load_calculator(listfetched);
	

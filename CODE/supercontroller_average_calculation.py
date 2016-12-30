##########################################################################################
#                                                                                        #
#                                                                                        #
#       File Name ----- superController_average_accumulation.py                          #
#                                                                                        #
#       Purpose ----- runs the algorithm every 10 sec and   				 #
#                       sends MASTER role request to controllers,        		 #
#                                                                                        #
#       Contributors  ----- Rushikesh , Malayaz , Priya , Neha                           #
#                                                                                        #
#       Revison Version ----- Latest                                                     #
#                                                                                        #      
#                                                                                        #
##########################################################################################

import socket               # Import socket module
import pickle
import time
import threading
import numpy as np

list_created_c1 = [[]]
list_created_c2 = [[]]
list_created_c3 = [[]]

threshold1 = 750
threshold2 = 750
threshold3 = 900

controller1 = '128.194.6.178'
controller2 = '128.194.6.141'
controller3 = '128.194.6.170'


t = [[10,0,0],[0,10,0],[0,0,10]]

controller_list = [controller1,controller2,controller3]
threshold_list = [threshold1,threshold2,threshold3]
print("The thresholds as [T1, T2, T3] on C1 C2 C3 respectively: ")
print(threshold_list)             

#########################################################################################
#                                                                                       #
#                                                                                       #
#       Function Name --- MyThreadX                                                     #
#                                                                                       #
#       Arguments ---- Load Balanced Time slices                                        #
#                                                                                       #
#       Purpose ----    Accepts socket connection from supercontroller to               #
#                               send the role request to become MASTER for a switch     #
#                                                                                       #
#       Return Value ---- NONE			                                        #
#                                                                                       #
#                                                                                       #
#                                                                                       #
#                                                                                       #
#########################################################################################

def MyThread1(t1,t2,t3):

    #print( "inside thread 1")
    t = [t1,t2,t3]
    print ( " values of t")
    print(t)
    flag = 0
    j = 0
    while j < 3:
            if ( t[j] != 0):
                    s = socket.socket()         # Create a socket object
                    host = controller_list[j]      # Get controller 1
                    port = 13999                # Reserve a port for your service.
                    try : 
		    	s.connect((host, port))
                    except:
			print("connection not possible")
			flag = 1
		    if ( flag != 1):	
		    	i=1
                    	while( i < (len(list_created_c1))):
                            dpid = int(list_created_c1[i][0],16)
                            print("======= 1")
			    print(dpid)
                            s.send(pickle.dumps(dpid))
			    print("New MASTER is controller" +str(j+1) + " for Switch with -- dpid " + hex(dpid))
                            i=i+1
                    	s.close                     # Close the socket when done

            time.sleep(t[j])
            j = j + 1
	    flag = 0

def MyThread2(t1,t2,t3):

    t = [t1,t2,t3]
    iter = 0
    j = 1
    flag = 0
    while iter < 3:
            if ( t[j] != 0):
                    s = socket.socket()         # Create a socket object
                    host = controller_list[j]      # Get controller 1
                    port = 13999                # Reserve a port for your service.
                    try:
		    	s.connect((host, port))
                    except:
			print("connection not possible")
			flag = 1
		    if ( flag != 1):	
                    	i=1
                    	while( i < (len(list_created_c2))):
                            dpid = int(list_created_c2[i][0],16)
                            print("======= 2")
			    print(dpid)
                            s.send(pickle.dumps(dpid))
			    print("New MASTER is controller" +str(j+1) + " for Switch with -- dpid " + hex(dpid))
                    	    i=i+1
                    	s.close                     # Close the socket when done

            time.sleep(t[j])
            iter = iter + 1
            j = (j + 1)%3
	    flag = 0


def MyThread3(t1,t2,t3):

    t = [t1,t2,t3]
    iter = 0
    j = 2
    flag = 0
    while iter < 3:
            if ( t[j] != 0):
                    s = socket.socket()         # Create a socket object
                    host = controller_list[j]      # Get controller 1
                    port = 13999                # Reserve a port for your service.
                    try:
                    	s.connect((host, port))
                    except:
			print("connection not possible")
			flag = 1
		    if ( flag != 1):	
                    	i=1
                    	while( i < (len(list_created_c3))):
                            dpid = int(list_created_c3[i][0],16)
                            print("======= 3")
			    print(dpid)
			    s.send(pickle.dumps(dpid))
			    print("New MASTER is controller" +str(j+1) + " for Switch with -- dpid " + hex(dpid))
			    i=i+1
                    	s.close                     # Close the socket when done

            time.sleep(t[j])
            iter = iter + 1
            j = (j + 1)%3
	    flag = 0


#########################################################################################
#                                                                                       #
#                                                                                       #
#       Function Name --- algo                               	                        #
#                                                                                       #
#       Arguments ---- Average Loads on Controllers C1,C2,C3                            #
#                                                                                       #
#       Purpose ----    Performs Load balancing based on the Average Loads on           #
#                            Controllers C1,C2,C3 				        #
#											#
#       Return Value ---- Load Balanced Time Slices                                     #
#                                                                                       #
#                                                                                       #
#                                                                                       #
#                                                                                       #
#########################################################################################


def algo(average_c1,average_c2,average_c3):
        avg_c = [average_c1,average_c2,average_c3]

	global t
        lc1 = average_c1 - threshold1
        lc2 = average_c2 - threshold2
        lc3 = average_c3 - threshold3
	on = [1,1,1]
	off = [1,1,1]
	sign_on = [1,1,1]
	sign_off = [1,1,1]
		
	offload = [1,1,1]
	onload = [1,1,1]
        if ( lc1 >0 and lc2 > 0 and lc3 > 0 ):
                print("\n Balancing is not possible here, recheck after 10 seconds")
                #time.sleep(10)
		
		t1 = threading.Thread(target=MyThread1, args=(t[0][0],t[0][1],t[0][2],))
		t2 = threading.Thread(target=MyThread2, args=(t[1][0],t[1][1],t[1][2],))
		t3 = threading.Thread(target=MyThread3, args=(t[2][0],t[2][1],t[2][2],))
				
		t1.start()
		t2.start()	
		t3.start()

		t1.join()
		t2.join()
		t3.join()
                return
        elif ( lc1 < 0 and lc2 <0 and lc3 < 0):
                print("\n No Balancing is required as none of the  Controller is above threshold, recheck after 10 seconds")
                #time.sleep(10)
		
		t1 = threading.Thread(target=MyThread1, args=(t[0][0],t[0][1],t[0][2],))
		t2 = threading.Thread(target=MyThread2, args=(t[1][0],t[1][1],t[1][2],))
		t3 = threading.Thread(target=MyThread3, args=(t[2][0],t[2][1],t[2][2],))
				
		t1.start()
		t2.start()	
		t3.start()

		t1.join()
		t2.join()
		t3.join()
                return
        else:
                print("\n Either full or partial balancing is possible here, doing load balancing now")
                lc = [lc1,lc2,lc3]
                i=0
                while i < len(lc):
                        if ( lc[i] < 0 ):
                                onload[i] = abs(lc[i])
                                offload[i] = 0
                        else:
                                offload[i] = lc[i]
                                onload[i] = 0
                        i = i + 1
                sum_onload = onload[0] + onload[1] + onload[2]
                sum_offload = offload[0] + offload[1] + offload[2]

                i=0
                while i < 3:
                        on[i] = (onload[i] /sum_onload) * min(sum_offload,onload[i])
                        off[i] = (offload[i] / sum_offload) * min( offload[i], sum_onload)

                        sign_on[i] = np.sign(on[i])
                        sign_off[i] = np.sign(off[i])
                        i = i + 1

		print ("\n onloading list")
		print(on)
		print ("\n offloading list")
		print(off)
	

		a = np.array(sign_on)
		new_sign_on = np.diag(a)	
		
		a = np.array(sign_off)
		new_sign_off = np.diag(a)	

		print ( "\n signum onloading list")
		print(sign_on)
		print ( "\n signum diagonal offloading list")
		print(new_sign_off)
	
	
                t = [[10,0,0],[0,10,0],[0,0,10]]
                i=0
                while i < 3:
                        if ((sign_off[i] == 1) and (avg_c[i] != 0)):
                                j=0
                                while j < 3:	
                                        t[i][j] = (1 - off[j]/avg_c[i])*new_sign_off[j][i]*10 + (min(off[i],on[j])/avg_c[i])*sign_on[j]*10
                                        j=j+1
                        i = i + 1
		print("\n Time Matrix after calculation")
		print(t)


		t1 = threading.Thread(target=MyThread1, args=(t[0][0],t[0][1],t[0][2],))
		t2 = threading.Thread(target=MyThread2, args=(t[1][0],t[1][1],t[1][2],))
		t3 = threading.Thread(target=MyThread3, args=(t[2][0],t[2][1],t[2][2],))
				
		t1.start()
		t2.start()	
		t3.start()

		t1.join()
		t2.join()
		t3.join()

		


average_c1 = 0.00
average_c2 = 0.00
average_c3 = 0.00

#########################################################################################
#                                                                                       #
#                                                                                       #
#       Function Name --- role_change_update                                            #
#                                                                                       #
#       Arguments ---- NONE	                                                        #
#                                                                                       #
#       Purpose ----   Reads contents from the shared memory and calls the              #
#                               algo function						#
#                                                                                       #
#       Return Value ---- NONE			                                        #
#                                                                                       #
#                                                                                       #
#                                                                                       #
#                                                                                       #
#########################################################################################


def role_change_update():
    i=1
    j=1
    k=1
    global average_c1
    global average_c2
    global average_c3
    	
    average_c1 = 0.00
    average_c2 = 0.00
    average_c3 = 0.00

    global list_created_c1
    global list_created_c2
    global list_created_c3
   
    
    fp = open("c1.pkl","rb")
    list_created_c1 = pickle.load(fp)
    fp2 = open("c2.pkl","rb")
    list_created_c2 = pickle.load(fp2)
    fp3 = open("c3.pkl","rb")
    list_created_c3 = pickle.load(fp3)


    print( " list created received")
    print(list_created_c1)
    print(list_created_c2)
    print(list_created_c3)
    
    	

    length_c1 = len(list_created_c1)
    length_c2 = len(list_created_c2)
    length_c3 = len(list_created_c3)
      
    print("length of c1 " + str(length_c1))
    print("length of c2 " + str(length_c2))
    print("length of c3 " + str(length_c3))

 
    while ( i < length_c1):
        print( "length of c1" + str(length_c1))
        print ( "value of i " + str(i))
        average_c1 = average_c1 + (list_created_c1[i][1])
        print ( " Intermediate average c1 ====>  ")
	print(average_c1)
        i=i+1
            
    while ( j < length_c2):
        average_c2 = average_c2 + (list_created_c2[j][1])
        print ( " Intermediate average c2 ====>  ")
	print(average_c2)
        j=j+1
        
    while ( k < length_c3):
        average_c3 =  average_c3 + (list_created_c3[k][1])
        print ( " Intermediate average c3 ====>  ")
	print(average_c3)
        k=k+1

    algo ( average_c1,average_c2,average_c3)

    
            
while 1:
	role_change_update()




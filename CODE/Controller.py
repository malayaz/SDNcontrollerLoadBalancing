##########################################################################################
# 											 #
# 											 #
#	File Name ----- Controller.py                                                    #
#											 #
#	Purpose ----- Provides Packet_IN  functionality , Gives count of flow requests   #
#			provides functionality to send MASTER,SLAVE role request,	 #
#											 #
#	Contributors  ----- Rushikesh , Malayaz , Priya , Neha				 #
#											 #
#	Revison Version ----- Latest							 #
#											 #	
#											 #
##########################################################################################


from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller import dpset
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import ether_types
import threading
import socket
import pickle

count = 1
dpid_list=[['Controller','1']]
dpid_list_static = [['dpid','datapath']]
test_datapath=[[]]





class MainClass(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION] 
    def __init__(self, *args, **kwargs):
        super(MainClass, self).__init__(*args, **kwargs)
        self.mac_to_port = {}


#########################################################################################
#											#
#											#		
#	Function Name --- super_controller_update					#
#											#	
#	Arguments ---- NONE								#
#											#
#	Purpose ---- 	Accepts socket connection from supercontroller to		#
#		 		send the role request to become MASTER for a switch 	#	
#											#		
#	Return Value ---- string SUCCESSFUL 						#	
#											#		
#											#	
#											#	
#											#
#########################################################################################	


    def super_controller_update(self):
	s = socket.socket()        	 # Create a socket object
	host = '' 			 # Get local machine name
	port = 13999    		 # Reserve a port for your service.

	s.bind((host, port))       	 # Bind to the port
	s.listen(5)                	 # Now wait for client connection.
	while True:
	   c, addr = s.accept()    	 # Establish connection with client.
	   print 'Got connection from', addr
	   #dpid_change = str(c.recv(1024))
 	   dpid_change = pickle.loads(c.recv(1024))
	   print("======================================")
	   dpid_change = str(hex(dpid_change)) 
	   print(dpid_change)
           
	   #The dpid_list_static is a list of the format [['dpid#1', 'datapath#1'],['dpid#2','datapath#2']....]
           dpids = zip(*dpid_list_static)[0]		#All the dpids in the dpid_list_static
           datapaths = zip(*dpid_list_static)[1] 	#All the datapaths in the dpid_static_list
           if dpid_change in dpids:			#If the dpid received from the supercontroller is present..
                index = dpids.index(dpid_change)	#.. in the dpid_list_static, the role change is sent..
                datapath = datapaths[index]		#.. to the appropriate switch identified by its datapath
                self.send_role_request(datapath)
	   print(dpid_list)
	   c.send('SUCCESSFUL')
	   c.close()


#########################################################################################
#											#
#											#		
#	Function Name --- matrixpush							#
#											#	
#	Arguments ---- NONE								#
#											#
#	Purpose ---- 	sends via socket connection to supercontroller the		#
#		 		matrix formed every 2 seconds of each			#
#					switches flow requests and dpid			#
#											#		
#	Return Value ---- NONE 								#	
#											#		
#											#	
#											#	
#											#
#########################################################################################	


    def matrixpush(self):
     	global dpid_list
	global dpid_list_static
	global test_datapath
	
	threading.Timer(2.0,self.matrixpush).start()	
	print(" Flow Requests received in last 2 seconds " + str(dpid_list))
	flow_requests_total_all_switches = 0
	length = len(dpid_list)
	if ( length > 1):
		i = 1
		while ( i < length):
			flow_requests_total_all_switches = flow_requests_total_all_switches + dpid_list[i][1]   #Accumulate the count of total load
			i = i+1	
	print("Total flow requests in last 2 seconds from switch " + str(flow_requests_total_all_switches))
	if ( flow_requests_total_all_switches > 750):
		print("Maximum flow requests handling capacity of the controller exceeded Warning: Controller Overloaded, total requests received : " + str(flow_requests_total_all_switches))
	s = socket.socket()         # Create a socket object
	server = '128.194.6.147'    # Get local machine name
	port = 65511                # Reserve a port for your service.
	try :
		s.connect((server, port))
	except:
		dpid_list = [['Controller','1']]
		return
	s.send(pickle.dumps(dpid_list))	
	s.close                     # Close the socket when done
	f = open('my_logs','w')
	f.write(str(dpid_list))
	f.close()
	f = open('sw_logs','w')
	f.write(str(dpid_list_static))
	f.close()
	dpid_list = [['Controller','1']]



    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath		#Extract datapath
        ofproto = datapath.ofproto		#Extract OpenFlow Protocol
        parser = datapath.ofproto_parser	#Extract OpenFlow Protocol Parser
	dpid = datapath.id			#Extract dpid (datapath id)
	found = [y for [x,y] in dpid_list_static if x == dpid]
        if found:
                dummy = 0
        else:
                dpid_list_static.append([dpid,datapath]) #Update static list to store dpid and datapaths

        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                          ofproto.OFPCML_NO_BUFFER)]
        self.add_flow(datapath, 0, match, actions)

#########################################################################################
#											#
#											#		
#	Function Name --- send_role_request						#
#											#	
#	Arguments ---- datapath of switch						#
#											#
#	Purpose ---- 	send the role request to become MASTER for a switch	 	#	
#											#		
#	Return Value ---- NONE								#	
#											#		
#											#	
#											#	
#											#
#########################################################################################	

    def send_role_request(self,datapath):
	ofp = datapath.ofproto
	ofp_parser = datapath.ofproto_parser
	req = ofp_parser.OFPRoleRequest(datapath, ofp.OFPCR_ROLE_MASTER,5)
	datapath.send_msg(req)

#########################################################################################
#											#
#											#		
#	Function Name --- role_reply_handler						#
#											#	
#	Arguments ---- event information						#
#											#
#	Purpose ---- listens for the reply to the send_role_request and displays	#
#		 		it's new role					 	#	
#											#		
#	Return Value ---- string SUCCESSFUL 						#	
#											#		
#											#	
#											#	
#											#
#########################################################################################	

    @set_ev_cls(ofp_event.EventOFPRoleReply,MAIN_DISPATCHER)	
    def role_reply_handler(self,ev):
	msg = ev.msg
	dp = msg.datapath
	ofp = dp.ofproto

	if msg.role == ofp.OFPCR_ROLE_NOCHANGE:
		role = 'NOCHANGE'
	elif msg.role == ofp.OFPCR_ROLE_EQUAL:
		role = 'EQUAL'
	elif msg.role == ofp.OFPCR_ROLE_MASTER:
		role = 'MASTER'
	elif msg.role == ofp.OFPCR_ROLE_SLAVE:
		role = 'SLAVE'
	else:
		role = 'unknown'
	self.logger.debug('OFPReplySuccess: %s',role)
	print("Role : " + str(role) + " for switch " + str(hex(dp.id)))
	
#########################################################################################
#											#
#											#		
#	Function Name --- add_flow							#
#											#	
#	Arguments ---- datapath of switch						#
#											#
#	Purpose ---- 	Adds Flow entry in switch from which Packet-in occurred		#
#		 	 								#	
#											#		
#	Return Value ---- NONE		 						#	
#											#		
#											#	
#											#	
#											#
#########################################################################################	

    def add_flow(self, datapath, priority, match, actions, buffer_id=None):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                             actions)]
        if buffer_id:
            mod = parser.OFPFlowMod(datapath=datapath, buffer_id=buffer_id,
                                    priority=priority, match=match,
                                    instructions=inst)
        else:
            mod = parser.OFPFlowMod(datapath=datapath, priority=priority,
                                    match=match, instructions=inst)
        datapath.send_msg(mod)
   
#########################################################################################
#											#
#											#
#	Function Name --- process							#
#											#
#	Arguments ---- datapath								#
#											#
#	Purpose ---- 	Accepts socket connection from supercontroller to		#
#		 		send the role request to become MASTER for a switch 	#
#											#
#	Return Value ---- string SUCCESSFUL 						#
#											#
#											#
#											#
#											#
#########################################################################################

    def process(self,datapath):
    	global dpid_list
	global dpid_list_static
	global test_datapath
	#print('DATAAAAAAAAAAAAAAAAPATH')
	temp = [datapath]
	datapath = temp[0]
	ofproto = datapath.ofproto
	#print(ofproto)
	dpid = datapath.id
	dpid = hex(dpid)
	#print(dpid)
	found = [[x,y] for [x,y] in dpid_list if x == dpid]
	if found:
		INDEX = dpid_list.index(found[0])		#Increment of the count of number..
		dpid_list[INDEX][1] = dpid_list[INDEX][1] + 1	#.. of requests recieved from a..
 	else:							#.. particular switch
		dpid_list.append([dpid,1])
	found = [y for [x,y] in dpid_list_static if x == dpid]
	if found:
		askda = 5
	else:
		test_datapath.append(datapath)
		dpid_list_static.append([dpid,datapath])

#########################################################################################
#											#
#											#
#	Function Name ---- _packet_in_handler						#
#											#
#	Arguments ---- NONE								#
#											#
#	Purpose ---- 	Handles the incoming packets					#
#		 		 							#
#											#
#	Return Value ---- NONE 								#
#											#
#											#
#											#
#											#
#########################################################################################

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
	global ev_datapath
	msg = ev.msg
        datapath = msg.datapath
	ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        in_port = msg.match['in_port']

        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocols(ethernet.ethernet)[0]

        if eth.ethertype == ether_types.ETH_TYPE_LLDP:
            # ignore lldp packet
            return
        dst = eth.dst
        src = eth.src

        dpid = datapath.id
        self.mac_to_port.setdefault(dpid, {})
        self.mac_to_port[dpid][src] = in_port

        if dst in self.mac_to_port[dpid]:
            out_port = self.mac_to_port[dpid][dst]
        else:
            out_port = ofproto.OFPP_FLOOD

        actions = [parser.OFPActionOutput(out_port)]

        if out_port != ofproto.OFPP_FLOOD:
            match = parser.OFPMatch(in_port=in_port, eth_dst=dst)
            if msg.buffer_id != ofproto.OFP_NO_BUFFER:
                self.add_flow(datapath, 1, match, actions, msg.buffer_id)
                return
            else:
                self.add_flow(datapath, 1, match, actions)
        data = None
        if msg.buffer_id == ofproto.OFP_NO_BUFFER:
            data = msg.data

        out = parser.OFPPacketOut(datapath=datapath, buffer_id=msg.buffer_id,
                                  in_port=in_port, actions=actions, data=data)
        datapath.send_msg(out)
	self.process(datapath)


a = MainClass()
a.matrixpush()
t = threading.Thread(target=a.super_controller_update)
t.start()

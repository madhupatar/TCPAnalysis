import os

#Initializing the various TCP variants for Experiment1 in NS-2:
Variants = ['Tahoe', 'Reno', 'NewReno', 'Vegas']
ns_cmd = "/course/cs4700f12/ns-allinone-2.35/bin/ns "
tab = '\t'
newline = '\n'

class Fields:
	def __init__(self, line):
		contents = line.split()
		self.event = contents[0]
		self.time = float(contents[1])
		self.from_node = contents[2]
		self.to_node = contents[3]
		self.pkt_type = contents[4]
		self.pkt_size = int(contents[5])
		self.flow_id = contents[7]
		self.src_addr = contents[8]
		self.dst_addr = contents[9]
		self.seq_num = contents[10]
		self.pkt_id = contents[11]
    
        
def Throughput(tcpvar, cbrrate):
    filename = tcpvar + "_op" + str(cbrrate) + ".tr"
    f= open(filename)
    fields = f.readlines()
    f.close()
    start_time = 10.0
    end_time = 0.0
    received_size = 0
	
    for line in fields:
	    field = Fields(line)
	    if field.flow_id == "1":
		    if field.event == "+" and field.from_node == "0":
			    if(field.time < start_time):
				    start_time = field.time
		    if field.event == "r":
			    received_size += field.pkt_size * 8
			    end_time = field.time
	
    duration = (end_time - start_time) / (1024 * 1024)		    
    throughput = received_size / duration		    
    return throughput




def PacketDrop(tcpvar, cbrrate):
	filename = tcpvar + "_op" + str(cbrrate) + ".tr"
	f = open(filename)
	lines = f.readlines()
	f.close()
	sendNum = recvdNum = 0
	for line in lines:
		field = Fields(line)
		if field.flow_id == "1":
			if field.event == "+":
				sendNum += 1
			if field.event == "r":
				recvdNum += 1
				
	totalrecvd = sendNum - recvdNum
	if sendNum == 0:
		return 0
	else:
		return float(totalrecvd)/ float(sendNum)


def Latency(tcpvar, cbrrate):
	filename = tcpvar + "_op" + str(cbrrate) + ".tr"
	f = open(filename)
	lines = f.readlines()
	f.close()
	start_time = {}
	end_time = {}
	total_duration = 0.0
	total_packet = 0
	for line in lines:
		field = Fields(line)
		if field.flow_id == "1":
			if field.event == "+" and field.from_node == "0":
				start_time.update({field.seq_num : field.time})
			if field.event == "r" and field.to_node == "0":
				end_time.update({field.seq_num : field.time})
	packets = {x for x in start_time.keys() if x in end_time.keys()}
	for i in packets:
		start = start_time[i]
		end = end_time[i]
		duration = end - start
		if(duration > 0):
			total_duration += duration
			total_packet += 1
	if total_packet == 0:
		return 0
		
	latency = total_duration / total_packet *1000
	return latency




#trace files generation
for variants in Variants:
    for cbrrate in range(1,11):
        os.system(ns_cmd + 'Experiment1.tcl '+variants+' '+ str(cbrrate))


throughput_ = open('Exp1_throughput.dat','w')
pktDrop_ = open('Exp1_packetDrop.dat','w')
delay_ = open('Exp1_latency.dat','w')
#Generating output files for writing the required values 
for tcpvar in Variants:
    throughput = ''
    pktDrop = ''
    delay = ''
    for cbrrate in range(1,11):
        throughput = throughput + tab + str(Throughput(tcpvar,cbrrate))
        pktDrop = pktDrop + tab + str(PacketDrop(tcpvar,cbrrate))
        delay = delay + tab + str(Latency(tcpvar,cbrrate))
    throughput_.write(str(cbrrate) + throughput + newline)
    pktDrop_.write(str(cbrrate) + pktDrop + newline)
    delay_.write(str(cbrrate) + delay + newline)

throughput_.close()
pktDrop_.close()
delay_.close()

os.system('rm *.tr')    
        
    

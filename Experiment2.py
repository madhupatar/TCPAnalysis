import os

#Initializing the various TCP variants for Experiment 2 in NS-2:
TCP_Variant2=['Reno_Reno', 'NewReno_Reno', 'Vegas_Vegas', 'NewReno_Vegas']

#Assigning the ns command to run without human intervention:
ns_cmd = "/course/cs4700f12/ns-allinone-2.35/bin/ns "
tab = '\t'
newline = '\n'

class NetworkData:
	def __init__(self, line):
		contents = line.split()
		self.event = contents[0]
		self.time = float(contents[1])
		self.start_node = contents[2]
		self.end_node = contents[3]
		self.pkt_type = contents[4]
		self.pkt_size = int(contents[5])
		self.flow_id = contents[7]
		self.src_addr = contents[8]
		self.dst_addr = contents[9]
		self.seq_num = contents[10]
		self.pkt_id = contents[11]


#Function to get the throughput values for TCP variant along with CBR rate:
def fetchThroughput(tcpvar, cbrrate):
	filename = tcpvar + "_output-" + str(cbrrate) + ".tr"
	f = open(filename)
	lines = f.readlines()
	f.close()
	# Set the counters start_time and end_time
	start_time1 = start_time2 = 10.0
	end_time1 = end_time2 = 0.0
	recvdSize1 = recvdSize2 = 0

	for line in lines:
		data = NetworkData(line)
		if data.flow_id == "1":#TCP stream from 1 to 4
			if data.event == "+" and data.start_node == "0":
				if(data.time < start_time1):
					start_time1 = data.time
			if data.event == "r":
				recvdSize1 += data.pkt_size * 8
				end_time1 = data.time
				
		if data.flow_id == "2":#TCP stream from 5 to 6
			if data.event == "+" and data.start_node == "4":
				if(data.time < start_time2):
					start_time2 = data.time
			if data.event == "r":
				recvdSize2 += data.pkt_size * 8
				end_time2 = data.time
				
	time1 = (end_time1 - start_time1)/ (1024 * 1024)
	time2 = (end_time2 - start_time2) / (1024 * 1024)
	#Throughput is calculated as the total received Size of the packets divided by total duration in Mb
	#print('DEBUG:' + str(recvdSize) + ' ' + str(end_time) + ' ' + str(start_time))
	throughput1 = recvdSize1 /time1
	throughput2 = recvdSize2 /time2
	finalthroughput = str(throughput1) + tab + str(throughput2)
	
	return finalthroughput

#Function the get the drop rate passing TCP variant and CBR Rate:
def fetchDropRate(tcpvar, cbrrate):
	filename = tcpvar + "_output-" + str(cbrrate) + ".tr"
	f = open(filename)
	lines = f.readlines()
	f.close()

	sendNum1 = 0
	sendNum2 = 0
	recvdNum1 = 0
	recvdNum2 = 0

	for line in lines:
		data = NetworkData(line)
		if data.flow_id == "1":
			if data.event == "+":
				sendNum1 += 1
			if data.event == "r":
				recvdNum1 += 1
		if data.flow_id == "2":
			if data.event == "+":
				sendNum2 += 1
			if data.event == "r":
				recvdNum2 += 1
				
	# Drop rate is calculated by finding the percentage of packets that are lost during transmission 
	droprate1 = 0 if sendNum1 == 0 else float(sendNum1 - recvdNum1) / float(sendNum1)
	droprate2 = 0 if sendNum2 == 0 else float(sendNum2 - recvdNum2) / float(sendNum2)
	finaldroprate = str(droprate1) + tab + str(droprate2)
	
	return finaldroprate

#Function to get the latency for the TCP variant and CBR rate:
def fetchLatency(tcpvar, cbrrate):
	filename = tcpvar + "_output-" + str(cbrrate) + ".tr"
	f = open(filename)
	lines = f.readlines()
	f.close()

	#Setting Counters start and end time:
	start_time1 = {}
	end_time1 = {}
	start_time2 = {}
	end_time2 = {}
	total_duration1 = total_duration2 = 0.0
	total_packet1 = total_packet2 = 0
	
	for line in lines:
		data = NetworkData(line)
		if data.flow_id == "1":
			if data.event == "+" and data.start_node == "0":
				start_time1.update({data.seq_num : data.time})
			if data.event == "r" and data.end_node == "0":
				end_time1.update({data.seq_num : data.time})
		if data.flow_id == "2":
			if data.event == "+" and data.start_node == "4":
				start_time2.update({data.seq_num : data.time})
			if data.event == "r" and data.end_node == "4":
				end_time2.update({data.seq_num : data.time})
	packets = {x for x in start_time1.keys() if x in end_time1.keys()}
	
	for i in packets:
		start = start_time1[i]
		end = end_time1[i]
		duration = end - start
		if(duration > 0):
			total_duration1 += duration
			total_packet1 += 1
	packets= {x for x in start_time2.keys() if x in end_time2.keys()}
	
	for i in packets:
		start = start_time2[i]
		end = end_time2[i]
		duration = end - start
		if(duration > 0):
			total_duration2 += duration
			total_packet2 += 1

	#Latency is calculated by finding the total network duration divided by the total packets sent in the network
	latency1 = 0 if total_packet1 == 0 else total_duration1 / total_packet1 * 1000
	latency2 = 0 if total_packet2 == 0 else total_duration2 / total_packet2 * 1000
	finallatency = str(latency1) + '\t' + str(latency2)
	
	return finallatency


#Function to generate the trace file for the two TCP variants passed
for var in TCP_Variant2:   
    for cbrrate in range(1, 11):
        tcps = var.split('_')
        os.system(ns_cmd +"Experiment2.tcl "+tcps[0]+" " +tcps[1]+" "+str(cbrrate))


#Creating the dat files for TCP variant data on comparison.
f1th = open('Exp2_Reno_Reno_throughput.dat', 'w')
f1dr = open('Exp2_Reno_Reno_droprate.dat', 'w')
f1de = open('Exp2_Reno_Reno_delay.dat', 'w')
f2th = open('Exp2_NewReno_Reno_throughput.dat', 'w')
f2dr = open('Exp2_NewReno_Reno_droprate.dat', 'w')
f2de = open('Exp2_NewReno_Reno_delay.dat', 'w')
f3th = open('Exp2_Vegas_Vegas_throughput.dat', 'w')
f3dr = open('Exp2_Vegas_Vegas_droprate.dat', 'w')
f3de = open('Exp2_Vegas_Vegas_delay.dat', 'w')
f4th = open('Exp2_NewReno_Vegas_throughput.dat', 'w')
f4dr = open('Exp2_NewReno_Vegas_droprate.dat', 'w')
f4de = open('Exp2_NewReno_Vegas_delay.dat', 'w')

for rate in range(1, 11):
	for var in TCP_Variant2:
		if var == 'Reno_Reno':
			f1th.write(str(rate) + tab + fetchThroughput(var, rate) + newline)
			f1dr.write(str(rate) + tab + fetchDropRate(var, rate) + newline)
			f1de.write(str(rate) + tab + fetchLatency(var, rate) + newline)
		if var == 'NewReno_Reno':
			f2th.write(str(rate) + tab + fetchThroughput(var, rate) + newline)
			f2dr.write(str(rate) + tab + fetchDropRate(var, rate) + newline)
			f2de.write(str(rate) + tab + fetchLatency(var, rate) + newline)
		if var == 'Vegas_Vegas':
			f3th.write(str(rate) + tab + fetchThroughput(var, rate) + newline)
			f3dr.write(str(rate) + tab + fetchDropRate(var, rate) + newline)
			f3de.write(str(rate) + tab + fetchLatency(var, rate) + newline)
		if var == 'NewReno_Vegas':
			f4th.write(str(rate) + tab + fetchThroughput(var, rate) + newline)
			f4dr.write(str(rate) + tab + fetchDropRate(var, rate) + newline)
			f4de.write(str(rate) + tab + fetchLatency(var, rate) + newline)

#Close the files
f1th.close()
f1dr.close()
f1de.close()
f2th.close()
f2dr.close()
f2de.close()
f3th.close()
f3dr.close()
f3de.close()
f4th.close()
f4dr.close()
f4de.close()

os.system('rm *.tr')

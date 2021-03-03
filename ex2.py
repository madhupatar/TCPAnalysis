import os

#Initializing the various TCP variants in NS-2:
TCP_Variant2=['Reno_Reno', 'NewReno_Reno', 'Vegas_Vegas', 'NewReno_Vegas']

#Assigning the ns command 
ns_command = "ns "

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


#Function to get the throughput values for TCP variant along with CBR rate
def fetchThroughput(variant, cbrrate):
	filename = variant + "_output-" + str(cbrrate) + ".tr"
	f = open(filename)
	lines = f.readlines()
	f.close()
	# Set counters
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

	#Throughput is calculated as the total received Size of the packets divided by total duration in Mb
	#print('DEBUG:' + str(recvdSize) + ' ' + str(end_time) + ' ' + str(start_time))
	throughput1 = recvdSize1 / (end_time1 - start_time1) / (1024 * 1024)
	throughput2 = recvdSize2 / (end_time2 - start_time2) / (1024 * 1024)
	throughput = str(throughput1) + '\t' + str(throughput2)
	
	return throughput

#Function the get the drop rate passing TCP variant and CBR Rate:
def fetchDropRate(variant, cbrrate):
	filename = variant + "_output-" + str(cbrrate) + ".tr"
	f = open(filename)
	lines = f.readlines()
	f.close()

	sendNum1 = recvdNum1 = 0
	sendNum2 = recvdNum2 = 0

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
	droprate = str(droprate1) + '\t' + str(droprate2)
	
	return droprate

#Function to get the latency for the TCP variant and CBR rate:
def fetchLatency(variant, cbrrate):
	filename = variant + "_output-" + str(cbrrate) + ".tr"
	f = open(filename)
	lines = f.readlines()
	f.close()

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
	latency = str(latency1) + '\t' + str(latency2)
	
	return latency


#Function to generate the trace file for the two TCP variants passed
for var in TCP_Variant2:   
    for cbrrate in range(1, 11):
        tcps = var.split('_')
        os.system("ns "+"ex2.tcl "+tcps[0]+" " +tcps[1]+" "+str(cbrrate))


#Create dat files to store variant comparison data.
f11 = open('exp2_RenoReno_throughput.dat', 'w')
f12 = open('exp2_RenoReno_droprate.dat', 'w')
f13 = open('exp2_RenoReno_delay.dat', 'w')
f21 = open('exp2_NewRenoReno_throughput.dat', 'w')
f22 = open('exp2_NewRenoReno_droprate.dat', 'w')
f23 = open('exp2_NewRenoReno_delay.dat', 'w')
f31 = open('exp2_VegasVegas_throughput.dat', 'w')
f32 = open('exp2_VegasVegas_droprate.dat', 'w')
f33 = open('exp2_VegasVegas_delay.dat', 'w')
f41 = open('exp2_NewRenoVegas_throughput.dat', 'w')
f42 = open('exp2_NewRenoVegas_droprate.dat', 'w')
f43 = open('exp2_NewRenoVegas_delay.dat', 'w')

for rate in range(1, 11):
	for var in TCP_Variant2:
		if var == 'Reno_Reno':
			f11.write(str(rate) + '\t' + fetchThroughput(var, rate) + '\n')
			f12.write(str(rate) + '\t' + fetchDropRate(var, rate) + '\n')
			f13.write(str(rate) + '\t' + fetchLatency(var, rate) + '\n')
		if var == 'NewReno_Reno':
			f21.write(str(rate) + '\t' + fetchThroughput(var, rate) + '\n')
			f22.write(str(rate) + '\t' + fetchDropRate(var, rate) + '\n')
			f23.write(str(rate) + '\t' + fetchLatency(var, rate) + '\n')
		if var == 'Vegas_Vegas':
			f31.write(str(rate) + '\t' + fetchThroughput(var, rate) + '\n')
			f32.write(str(rate) + '\t' + fetchDropRate(var, rate) + '\n')
			f33.write(str(rate) + '\t' + fetchLatency(var, rate) + '\n')
		if var == 'NewReno_Vegas':
			f41.write(str(rate) + '\t' + fetchThroughput(var, rate) + '\n')
			f42.write(str(rate) + '\t' + fetchDropRate(var, rate) + '\n')
			f43.write(str(rate) + '\t' + fetchLatency(var, rate) + '\n')

#Close the files
f11.close()
f12.close()
f13.close()
f21.close()
f22.close()
f23.close()
f31.close()
f32.close()
f33.close()
f41.close()
f42.close()
f43.close()

os.system('rm *.tr')

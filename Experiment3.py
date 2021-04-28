import os

#Initializing the various TCP variants and queuing algorithms for Experiment3 in NS-2:
TCP_Variant=['Reno', 'SACK']
QUEUE_Variant=['DropTail', 'RED']

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

def fetchThroughput(tcpvar, queuevar, granularity = 0.5):
	f = open(tcpvar + "-" +queuevar + "_output.tr")
	output = open('Exp3_' + tcpvar + '_' + queuevar + '_throughput.dat', 'w')
	lines = f.readlines()
	f.close()
	clock = 0.0
	sum1 = sum2 = 0

	for line in lines:
		data = NetworkData(line)
		if data.flow_id == "0" and data.event == "r" and data.end_node == "5":
			#CBR
			sum1 += data.pkt_size * 8
		if data.flow_id == "1" and data.event == "r":
			#TCP
			sum2 += data.pkt_size * 8

		if(data.time - clock <= granularity):
			pass
		else:
			# Calculate throughput as total receivedSize of packets divided by total duration in Mb
			throughput1 = sum1 / granularity / (1024 * 1024)
			throughput2 = sum2 / granularity / (1024 * 1024)
			
			output.write(str(clock) + tab + str(throughput1)+ tab + str(throughput2) + newline)

			clock += granularity
			sum1 = sum2 = 0

	# print(str(clock) + "\t" + str(throughput1)+ "\t" + str(throughput2))
	output.write(str(clock) + "\t" + str(throughput1)+ "\t" + str(throughput2) + "\n")
	output.close()

def fetchLatency(tcpvar, queuevar, granularity = 0.5):
	f = open(tcpvar + "-" +queuevar + "_output.tr")
	output = open('Exp3_' + tcpvar + '_' + queuevar + '_delay.dat', 'w')
	lines = f.readlines()
	f.close()
	
	#Set counter start and end time
	start_time1 = {}
	end_time1 = {}
	total_duration1 = total_duration2 = 0.0
	total_packet1 = total_packet2 = 0
	start_time2 = {}
	end_time2 = {}
	clock = 0.0

	for line in lines:
		data = NetworkData(line)
		
		#For sent packets handle the startTime, sentPacket count and sequencing
		#For received packets handle the endTime, received packets and duration for ACK Message to reach for a certain seq number
		if data.flow_id == "0":
			if data.event == "+" and data.start_node == "4":
				start_time1.update({data.seq_num : data.time})
			if data.event == "r" and data.end_node == "5":
				end_time1.update({data.seq_num : data.time})
		if data.flow_id == "1":
			if data.event == "+" and data.start_node == "0":
				start_time2.update({data.seq_num : data.time})
			if data.event == "r" and data.end_node == "0":
				end_time2.update({data.seq_num : data.time})

		if(data.time - clock <= granularity):
			pass
		else:
			packets = {x for x in start_time1.keys() if x in end_time1.keys()}
			for i in packets:
				duration = end_time1.get(i) - start_time1.get(i)
				if(duration > 0):
					total_duration1 += duration
					total_packet1 += 1
			#
			packets= {x for x in start_time2.keys() if x in end_time2.keys()}
			for i in packets:
				duration = end_time2.get(i) - start_time2.get(i)
				if(duration > 0):
					total_duration2 += duration
					total_packet2 += 1

			# Calculate latency by finding total network duration divided by the total packets sent in the network
			latency1 = 0 if total_packet1 == 0 else total_duration1 / total_packet1 * 1000
			latency2 = 0 if total_packet2 == 0 else total_duration2 / total_packet2 * 1000

			output.write(str(clock) + tab + str(latency1) + tab + str(latency2) + newline)
			# Clear counter
			clock += granularity
			start_time1 = {}
			start_time2 = {}
			
			end_time1 = {}
			end_time2 = {}
			
			total_duration1 = total_duration2 = 0.0
			total_packet1 = total_packet2 = 0

	output.write(str(clock) + tab + str(latency1) + tab + str(latency2) + newline)
	output.close()

#Generate the trace files
for tcpvar in TCP_Variant:
	for queue in QUEUE_Variant:
		os.system(ns_cmd + "Experiment3.tcl " + tcpvar + " " + queue)

#To Calculate the Throughput and Latency
for tcpvar in TCP_Variant:
	for queuevar in QUEUE_Variant:
		fetchThroughput(tcpvar, queuevar)
		fetchLatency(tcpvar, queuevar)

os.system('rm *.tr')

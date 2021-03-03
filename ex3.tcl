#Creating a new Simulator object
set ns [new Simulator]

#TCP variant Reno or SACK parsed for queuing experiment
set tcp_var [lindex $argv 0]
# Queue algorithm type is fetched 
set q_var [lindex $argv 1]

#Provide hint to the user
if {$argc != 2} {
	puts "\n\nExpected arguments are the TCP type and the Queuing Algorithm chosen between each node"
	exit 1
}
#if {$q_var != "RED" || $q_var != "Droptail"} {
#	puts "\n\nOnly supports Queuing Algorithms RED and Droptail"
#	exit 1
#}
#if {$tcp_var != "Reno" || $tcp_var != "SACK"} {
#	puts "\n\nOnly supports TCP variants Reno and SACK"
#	exit 1
#}
        
#Open the trace file
set tf [open ${tcp_var}-${q_var}_output.tr w]
set nf [open ${tcp_var}-${q_var}_output.nam w]
$ns trace-all $tf
$ns namtrace-all $nf

#Define a 'finish' procedure
proc finish {} {
	global ns tf nf
	$ns flush-trace
	puts "Simulation created"
	close $nf
	close $tf
	exit 0
}

#Creating the 6 nodes
set n1 [$ns node]
set n2 [$ns node]
set n3 [$ns node]
set n4 [$ns node]
set n5 [$ns node]
set n6 [$ns node]

#creating the links between the nodes for topology
$ns duplex-link $n1 $n2 10Mb 10ms $q_var
$ns duplex-link $n2 $n3 10Mb 10ms $q_var
$ns duplex-link $n5 $n2 10Mb 10ms $q_var
$ns duplex-link $n4 $n3 10Mb 10ms $q_var
$ns duplex-link $n6 $n3 10Mb 10ms $q_var	


#Setting the queue size
$ns queue-limit $n1 $n2 10
$ns queue-limit $n5 $n2 10
$ns queue-limit $n2 $n3 10
$ns queue-limit $n4 $n3 10
$ns queue-limit $n6 $n3 10

#Setup of a UDP connection
set udp [new Agent/UDP]
$ns attach-agent $n5 $udp
set null [new Agent/Null]
$ns attach-agent $n6 $null
$ns connect $udp $null

#Setup of a CBR over UDP connection
set cbr [new Application/Traffic/CBR]
$cbr attach-agent $udp
$cbr set type_ CBR
$cbr set rate_ 7mb

#Setup of a TCP conncection
if {$tcp_var eq "Reno"} {
	set tcp [new Agent/TCP/Reno]
	set sink [new Agent/TCPSink]
} elseif {$tcp_var eq "SACK"} {
	set tcp [new Agent/TCP/Sack1]
	set sink [new Agent/TCPSink/Sack1]
}
$tcp set class_ 1
$ns attach-agent $n1 $tcp
$ns attach-agent $n4 $sink
$ns connect $tcp $sink

#Setup of a FTP Application
set ftp [new Application/FTP]
$ftp attach-agent $tcp

#Schedule events for the CBR and FTP agents
$ns at 0.0 "$ftp start"
$ns at 3.0 "$cbr start"
$ns at 10.0 "$ftp stop"
$ns at 10.0 "$cbr stop"

#Callind the finish procedure after 10s of simulation time
$ns at 10.0 "finish"

#Run the simulation
$ns run

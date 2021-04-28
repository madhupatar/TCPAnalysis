# Create a Simulator object
set ns [new Simulator]
# TCP variant
set variant [lindex $argv 0]
# CBR rate
set rate [lindex $argv 1]

# Open the trace file
set tf [open ${variant}_op${rate}.tr w]
set nf [open ${variant}_op${rate}.nam w]
$ns trace-all $tf
$ns namtrace-all $nf

# Define a 'finish' procedure
proc finish {} {
	global ns tf nf
	$ns flush-trace
	puts "Simulation created"
	close $nf
	close $tf
	#exec nam ${variant}_op{rate}.nam &
	exit 0
}

# create 6 nodes
set n1 [$ns node]
set n2 [$ns node]
set n3 [$ns node]
set n4 [$ns node]
set n5 [$ns node]
set n6 [$ns node]

# define different colors for nam data flows
$ns color 1 Green
$ns color 2 Blue
$ns color 3 Red
$ns color 4 Yellow
$ns color 5 Coral
$ns color 6 Gold


#create links between the nodes
$ns duplex-link $n1 $n2 10Mb 10ms DropTail
$ns duplex-link $n5 $n2 10Mb 10ms DropTail
$ns duplex-link $n2 $n3 10Mb 10ms DropTail
$ns duplex-link $n4 $n3 10Mb 10ms DropTail
$ns duplex-link $n6 $n3 10Mb 10ms DropTail

#Setup a UDP connection
set udp [new Agent/UDP]
$ns attach-agent $n2 $udp
set null [new Agent/Null]
$ns attach-agent $n3 $null
$ns connect $udp $null

#Setup a CBR over UDP connection
set cbr [new Application/Traffic/CBR]
$cbr attach-agent $udp
$cbr set type_ CBR
$cbr set rate_ ${rate}mb

#Setup a TCP conncection
if {$variant eq "Tahoe"} {
	set tcp [new Agent/TCP]
} elseif {$variant eq "Reno"} {
	set tcp [new Agent/TCP/Reno]
} elseif {$variant eq "NewReno"} {
	set tcp [new Agent/TCP/Newreno]
} elseif {$variant eq "Vegas"} {
	set tcp [new Agent/TCP/Vegas]
}

$tcp set class_ 1
$ns attach-agent $n1 $tcp
set sink [new Agent/TCPSink]
$ns attach-agent $n4 $sink
$ns connect $tcp $sink

#setup FTP Application
set ftp [new Application/FTP]
$ftp attach-agent $tcp

#Schedule events for agents
$ns at 0.0 "$cbr start"
$ns at 0.0 "$ftp start"
$ns at 10.0 "$ftp stop"
$ns at 10.0 "$cbr stop"

#Call the finish procedure after  seconds of simulation time
$ns at 10.0 "finish"

#Run the simulation
$ns run

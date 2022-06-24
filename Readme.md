# pcapPlay

## A utility to replay multicast packets saved within a pcap file. 

This tool was born out of frustration in not having any luck in using other "packet player" type tools (like tcpReplay) for
replaying multicast packets. See this [link](https://stackoverflow.com/questions/72722144/replaying-multicast-udp-packet-capture-via-tcpreplay-not-being-seen-by-client) for a description of that specific issue.

The specific purpose of this tool is to replay a UDP multicast packet stream captured from the flight simulator DCS with the **DCS-Bios** mod installed. The **DCS-Bios** mod broadcasts cockpit state over the network allowing clients to monitor/control certain aspects of the virtual cockpit with ancillary ("game") controllers. In order to facilitate easier development of the parsing and operating on the decoded packets, I wanted a utility like this to allow that work without having to keep the flight simulator running in the background.
However, there is nothing about this tool that is specific to this use-case, other than some _clarg_ defaults that are tailored to the **DCS-Bios** multicast configuration.
### The workflow is as follows

(assuming **DCS-Bios** has been installed)
1. Start a packet capture tool like Wireshark.
2. Configure that tool to only capture multicast packets with a capture filter:
`dst host 239.255.50.10 and ip multicast` (Note: this is Wireshark vernacular. The multicast address is specified by **DCS-Bios**)
3. Start the capture process. At this point, no packets should be seen as the DCS program is not running
4. Run DCS and select "Instant Action" from the main screen. Choose the specific aircraft you are interested in and chose a relevant starting off point.
5. Once the aircraft loads, you will be presented a briefing screen - the multicast stream will start as soon as you dismiss that screen and "climb into the cockpit"
6. Capture as much data as you think appropriate - or break into different groups for certain actions. 
7. Save the captured data in `pcap` format
8. Exit DCS
9. Run this tool (pcapPlay) using your newly created pcap file as the input.
10. Your UDP client should see the input stream as if coming straight from DCS.

### Usage:

python pcapPlay <pcap filename> -d <delay>, -i <addr>, -p <port>
<delay> = time between sending packets in microseconds, default: 50
<addr> = multicast address, default = 239.255.50.10
<port> = multicast port, default = 5010

### Build notes:

As of June 24, 2022 - the scapy library installed via `pip install` direct from PyPI contains a known [bug](https://stackoverflow.com/questions/67947076/problems-reading-a-pcap-file-in-python-using-scapy) which prevents this tool from running. To circumvent that the requirements.txt file within this repo specifies installing the scapy library via a git repo. In the future, I hope the installation at PyPI will be sufficient.



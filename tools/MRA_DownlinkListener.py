#
# MRA_DownlinkListener.py
#
# Sample code which listens for "downlink" Meteor Remote API message.
# These are messages sent (unprompted) from MetPrint to the Remove API client, when
# there are changes in the job state - e.g. when job sets are added to the print
# queue.
#
# Note that although it is possible for the "uplink" and "downlink" TCP/IP ports
# to be the same, this is not recommended.  It is better to have separate ports
# so that the command/response handshakes for the uplink and downlink messages
# can't get interleaved.
#
# By default, downlink messages use port 5556, and uplink messages use port 5555.
# The ports can be changed in the MetPrint settings.
#
import argparse
import json
import socket
import sys

#
# Text encoding used for encoding and decoding the Meteor Remote API (MRA) messages.
# This should match the value set in the MetPrint setup window (default is UTF-8).
#
MetPrintMsgEncoding = 'utf-8'

#
# Connect to the Meteor Remote API (MRA) server port
#
# 'addr'
#   To run this sample application on the same PC as MetPrint, set 'localhost' or '127.0.0.1' as the IP address
#   To connect over the network, either the target PC "device name" (as shown in Windows | Settings | System | About), or its IP address, can be used
# 'port'
#   The default port number is 5555, which can be changed in the MetPrint setup window
#
def ConnectToMetPrint(addr, port):
    print(F"### Attempting to connect to MetPrint at address={addr} port={port}")
    try:
        global metPrintSocket
        metPrintSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        metPrintSocket.connect((addr, port))
        # N.B. Don't set a timeout on the socket, so it will block indefinitely until a message is received
        print("### MetPrint socket connected OK")
    except:
        print("*** MetPrint socket connect Failed !!")
        sys.exit()

#
# Convert 'msg' to JSON, send to the Meteor Remote API, wait for a response message, and print it
# to the console
#
def SendMsg(msg):
    data = json.JSONEncoder().encode(msg)
    print(F"### MRA Send: {data}")
    
    try:
        metPrintSocket.send(data.encode(MetPrintMsgEncoding))
    except:
        print("*** MetPrint socket send Failed !!")
        sys.exit()

    try:
        responseBytes = metPrintSocket.recv(4096)
    except:
        print("*** MetPrint socket receive timed out !!")
        sys.exit()

    responseString = responseBytes.decode(MetPrintMsgEncoding);
    responseJson = json.JSONDecoder().decode(responseString);
    print(F"### MRA Resp: {responseJson}")


#####################################################################################################

#
# Set up the sample application command line options, e.g. displayed by calling 'python MRA_PrintMode.py --help' on the command line
#
parser = argparse.ArgumentParser()
parser.description = 'Listens for Meteor Remote API downlink messages.'
parser.add_argument('-p',   '--port',       help='TCP/IP port, default=5556', type=int, default=5556)
parser.add_argument('-a',   '--address',    help='TCP/IP address, default=localhost', type=str, default='localhost')
args = parser.parse_args()

#
# Connect to the MetPrint Remote API server (aka "ERP Server", enabled in 
# the 'System Configuration' tab of the MetPrint setup window)
#
ConnectToMetPrint(args.address, args.port)

#
# Loop endlessly, logging messages to the console.
#
while True:
    try:
        responseBytes = metPrintSocket.recv(4096)
    except:
        print("*** MetPrint socket disconnected !!")
        sys.exit()

    rxString = responseBytes.decode(MetPrintMsgEncoding);

    rxPos = 0
    while rxPos < len(rxString):
        rxJson, offset = json.JSONDecoder().raw_decode(rxString[rxPos:])
        rxPos = rxPos + offset

        print(F"### MRA Message: {rxJson}")

        #
        # Acknowledge the message.
        #
        if rxJson['cmd'] == 'JobStateChanged':
            ack = dict()
            ack['cmd'] = 'JobStateChangedAck' 
            ack['sn'] = rxJson['sn']
            txData = json.JSONEncoder().encode(ack)
            metPrintSocket.send(txData.encode(MetPrintMsgEncoding))
        elif rxJson['cmd'] == 'PrintEngineError':
            ack = dict()
            ack['cmd'] = 'PrintEngineErrorAck' 
            ack['sn'] = rxJson['sn']
            txData = json.JSONEncoder().encode(ack)
            metPrintSocket.send(txData.encode(MetPrintMsgEncoding))


#####################################################################################################

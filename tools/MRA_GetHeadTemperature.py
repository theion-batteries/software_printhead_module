#
# MRA_GetHeadTemperature.py
#
# Sample code demonstrating how to request a head temperature from the MetPrint Remote API
# using the HeadTemperatureReq message.  Optionally writes the temperatures to a log file.
#
#
import argparse
import json
import socket
import sys
import time
from datetime import datetime

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
        metPrintSocket.settimeout(5)
        print("### MetPrint socket connected OK")
    except:
        print("*** MetPrint socket connect Failed !!")
        sys.exit()


#
# Convert 'msg' to JSON, send to the Meteor Remote API, wait for a response message, and print it
# to the console.
#
# Logs the temperature from a HeadTemperatureAck response to a file, if a file path is specified 
# on the command line
#
def SendMsg(msg, filename):
    data = json.JSONEncoder().encode(msg)
    print(F"### MRA Send: {data}")
    
    try:
        metPrintSocket.send(data.encode(MetPrintMsgEncoding))
    except:
        print("*** MetPrint socket send Failed !!")
        sys.exit()


    while True:
        try:
            responseBytes = metPrintSocket.recv(4096)
        except:
            print("*** MetPrint socket receive timed out !!")
            sys.exit()
        
        responseString = responseBytes.decode(MetPrintMsgEncoding);
        responseJson = json.JSONDecoder().decode(responseString);
        print(F"### MRA Resp: {responseJson}")

        if responseJson['cmd'] == 'HeadTemperatureAck':
            #
            # If we get an error we just exit the sample script.  
            # A production application should handle this situation more gracefully.
            #
            if responseJson['result'] != "Success":
                print(F"*** HeadTemperatureReq failed: result={responseJson['result']}")
                sys.exit()
            if filename != "":
                with open(filename, "a") as logFile:
                    temp = responseJson['headTemperature']
                    logFile.write(F"{datetime.now()}: TEMP={temp/10}\n")

            return




#####################################################################################################

#
# Set up the sample application command line options, e.g. displayed by calling 'python MRA_PrintMode.py --help' on the command line
#
parser = argparse.ArgumentParser()
parser.description = 'Request a head temperature using the Meteor Remote API.'
parser.add_argument("pccid", nargs=1, type=int, help="The Print Controller Card index, 1-N")
parser.add_argument("hdcid", nargs=1, type=int, help="Index of the Head Driver Card index on the PCC, 1-8")
parser.add_argument("headid", nargs=1, type=int, help="Index of the Print Head on the HDC, 1-4")
parser.add_argument('-p',   '--port',       help='TCP/IP port, default=5555', type=int, default=5555)
parser.add_argument('-a',   '--address',    help='TCP/IP address, default=localhost', type=str, default='localhost')
parser.add_argument('-f',   '--filename',   help='Full path to a log file, the temperature is written once per second', type=str, default='')
args = parser.parse_args()

#
# Connect to the MetPrint Remote API server (aka "ERP Server", enabled in 
# the 'System Configuration' tab of the MetPrint setup window)
#
ConnectToMetPrint(args.address, args.port)

#
# Create a dictionary for the command.
# All Meteor Remote API messages include a 'cmd' and a 'sn' parameter.
# Other parameters are command specific
#
msg = dict()

#
# Each message which is sent to MetPrint should have a unique sequence number, which can be
# used to check that the command and response messages match.
#
sn = 10

#
# Add the parameters which have been sent on the command line
#

msg['cmd'] = "HeadTemperatureReq"
msg['sn'] = sn
msg['pccid'] = args.pccid[0]
msg['hdcid'] = args.hdcid[0]
msg['headid'] = args.headid[0]

if args.filename != "":

    while True:
        msg['sn'] = sn
        sn = sn + 1
        SendMsg(msg, args.filename)
        time.sleep(1)

else:
    #
    # Send the TCP/IP message and wait for a response (for the socket timeout period of 5 seconds)
    #
    SendMsg(msg, "")

#
# This sample application connects to MetPrint, sends a single message, and then disconnects / exits.
# A production application should normally keep running and maintain the socket connection, to avoid
# the overhead of repeated connect and disconnects
#
print("### MRA_GetHeadTemperature.py finished")

#####################################################################################################

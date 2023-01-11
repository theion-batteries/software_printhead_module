#
# MRA_SetSignal.py
#
# Sample code demonstrating how to send a MetPrint Remote API message to MetPrint
# for setting an arbitrary Meteor signal.  
# This is the equivalent of calling the PrinterInterface API function PiSetSignal;
# see documentation for the details of individual signals.
#
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
        metPrintSocket.settimeout(5)
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

#
# Convert a string to an integer; using type=auto_int in add_argument below (instead of type=int) allows
# either decimal or hexadecimal parameters to be used: a hex value should be prefixed with 0x
#
def auto_int(x):
    return int(x, 0)

#####################################################################################################

#
# Set up the sample application command line options, e.g. displayed by calling 'python MRA_SetSignal.py --help' on the command line
#
parser = argparse.ArgumentParser()
parser.description = 'Sends a Meteor Remote API command to set a Meteor signal.  e.g. MRA_SetSignal.py 0x00020003 1 uses SIG_OUT4 to set general purpose output 4 on PCC2'
parser.add_argument('-p',       '--port',           help='TCP/IP port, default=5555', type=int, default=5555)
parser.add_argument('-a',       '--address',        help='TCP/IP address, default=localhost', type=str, default='localhost')
parser.add_argument('signalid',     type=auto_int,  help="The formatted Meteor signal: Xaddr[31:24]|PccNum[23:16]|HdcNum[15:8]|SIG_xxx[7:0]")
parser.add_argument('signalstate',  type=auto_int,  help='The signal state')
parser.add_argument('-s',       '--sn',         type=str, default="1",  help='Sequence number for the outgoing command')
parser.add_argument('-b',       '--blocking',   type=int, default=1,    help='0: MRA sets the signal asynchronously; 1 (default): MRA blocks until the signal is set')
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
# Add the parameters which have been sent on the command line
#

msg['cmd'] = "SetSignalReq"
msg['sn'] = args.sn
msg['signalid'] = args.signalid
msg['signalstate'] = args.signalstate
msg['async'] = not args.blocking

#
# Send the TCP/IP message and wait for a response (for the socket timeout period of 5 seconds)
#
SendMsg(msg)

#
# This sample application connects to MetPrint, sends a single message, and then disconnects / exits.
# A production application should normally keep running and maintain the socket connection, to avoid
# the overhead of repeated connect and disconnects
#
print("### MRA_SetSignal.py finished")

#####################################################################################################

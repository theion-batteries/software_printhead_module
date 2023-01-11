#
# MRA_PrintOnDemandRotation.py
#
# Sample code demonstrating how to send a MetPrint Remote API message to MetPrint.
# The command fields are all set using command line parameters.
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


#####################################################################################################

#
# Set up the sample application command line options, e.g. displayed by calling 'python MRA_PrintMode.py --help' on the command line
#
parser = argparse.ArgumentParser()
parser.description = 'Sends a generic Meteor Remote API command .'
parser.add_argument('-p',   '--port',       help='TCP/IP port, default=5555', type=int, default=5555)
parser.add_argument('-a',   '--address',    help='TCP/IP address, default=localhost', type=str, default='localhost')
parser.add_argument('--sn', type=str, default="1")
parser.add_argument('--angleDeg', type=str, default="0.0")
parser.add_argument('--xoffset', type=str, default="0")
parser.add_argument('--yoffset', type=str, default="0")
parser.add_argument('--xscale', type=str, default="0")
parser.add_argument('--yscale', type=str, default="0")
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

msg['cmd'] = "PrintOnDemandRotateReq"
msg['sn'] = args.sn
msg['angle'] = str(int(round(float(args.angleDeg) * 1e7))) # Scale of int sent to Meteor is 10^7
msg['xoffset'] = args.xoffset
msg['yoffset'] = args.yoffset
msg['xscale'] = args.xscale
msg['yscale'] = args.yscale

#
# Send the TCP/IP message and wait for a response (for the socket timeout period of 5 seconds)
#
SendMsg(msg)

#
# This sample application connects to MetPrint, sends a single message, and then disconnects / exits.
# A production application should normally keep running and maintain the socket connection, to avoid
# the overhead of repeated connect and disconnects
#
print("### MRA_PrintOnDemandRotation.py finished")

#####################################################################################################

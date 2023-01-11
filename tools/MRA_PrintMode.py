#
# MRA_PrintJob.py
#
# Sample code demonstrating how to send a MetPrint Remote API message to MetPrint
# to define, select or remove a print mode.
#
# Print modes can be used in multiple master systems to define how many copies of
# each document are printed on each master PCC
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
# Convert 'msg' to JSON, send to the Meteor Remote API, and wait for a response message.
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
    # For specific response processing we can look in the dictionary, for example, here we're
    # checking for one of the PrintMode 'ACK' messages, and checking the result.
    #
    if responseJson['cmd'] == 'DefinePrintModeAck' or responseJson['cmd'] == 'SelectPrintModeAck' or responseJson['cmd'] == 'RemovePrintModeAck' or responseJson['cmd'] == 'GetPrintModeAck':
        if responseJson['result'] == 'WrongParam':
            print("*** MRA returned 'WrongParam': check that the print mode name is set")
        else:
            print(F"### MRA returned {responseJson['result']}")
    else:
        # This will happen if we send any command other than DefinePrintModeReq, SelectPrintModeReq, RemovePrintModeReq
        # or GetPrintModeReq.  It will happen if there is no command selected on the command line (-d, -r, -s or -g).
        print(F"### MRA Unexpected print mode response: {responseJson['cmd']}")


#####################################################################################################

#
# Set up the sample application command line options, e.g. displayed by calling 'python MRA_PrintMode.py --help' on the command line
#
parser = argparse.ArgumentParser()
parser.description = 'Sends a Meteor Remote API command to define (DefinePrintModeReq), select (SelectPrintModeReq), remove (RemovePrintModeReq) or get (GetPrintModeReq) a MetPrint print mode.'
parser.add_argument('-d',   '--define',     help='send DefinePrintModeReq to define (or redefine) a print mode', action='store_true')
parser.add_argument('-s',   '--select',     help='send SelectPrintModeReq to select a print mode: if used with -d the mode is selected as part of the DefinePrintModeReq command', action='store_true')
parser.add_argument('-r',   '--remove',     help='send RemovePrintModeReq to remove a print mode', action='store_true')
parser.add_argument('-g',   '--get',        help='send GetPrintModeReq to get the name of the current print mode', action='store_true')
parser.add_argument('-n',   '--name',       help='the print mode name', type=str)
parser.add_argument('-c',   '--copies',     help='list of integers (separated by spaces) defining the number of document copies per PCC', nargs='+', type=int)
parser.add_argument('-p',   '--port',       help='TCP/IP port, default=5555', type=int, default=5555)
parser.add_argument('-a',   '--address',    help='TCP/IP address, default=localhost', type=str, default='localhost')
args = parser.parse_args()

#
# Connect to the MetPrint Remote API server (aka "ERP Server", enabled in 
# the 'System Configuration' tab of the MetPrint setup window)
#
ConnectToMetPrint(args.address, args.port)

#
# Start the command sequence number at an arbitrary value.  Every command that is
# created by the client application should have a unique 'sn'.
#
sn = 4500

#
# Create a dictionary for the command.
# All Meteor Remote API messages include a 'cmd' and a 'sn' parameter.
# Other parameters are command specific
#
msg = dict()

if args.define:
    
    # The -d command line option selects the DefinePrintModeReq command
    msg['cmd'] = 'DefinePrintModeReq'
    # Unique sequence number for this command
    msg['sn'] = sn
    # The print mode name
    msg['name'] = args.name
    # The number of copies of each document to print on a per-PCC basis
    # The number of elements in the array should match the number of PCCs in the system
    # e.g. setting -c 1 0 3 0 on the command line means print 1 copy of each document on PCC1, no copies on
    #      PCC2, 3 copies on PCC3 and no copies on PCC4.
    msg['copiesperpcc'] = args.copies
    # The mode can either be selected immediately, or selected later with the 'SelectPrintModeReq' command
    if args.select:
        msg['selectnow'] = True

elif args.remove:
    
    # The -r command line option selects the RemovePrintModeReq command
    msg['cmd'] = 'RemovePrintModeReq'
    # Unique sequence number for this command
    msg['sn'] = sn
    # The print mode name
    msg['name'] = args.name;

elif args.select:

    # The -s command line option selects the SelectPrintModeReq command
    msg['cmd'] = 'SelectPrintModeReq'
    # Unique sequence number for this command
    msg['sn'] = sn
    # The print mode name
    msg['name'] = args.name;

elif args.get:

    # The -g command line option selects the GetPrintModeReq command
    msg['cmd'] = 'GetPrintModeReq'
    # Unique sequence number for this command
    msg['sn'] = sn

else:

    # No command has been selected on the command line: send a dummy command to 
    # demonstrate the MetPrint error response
    msg['cmd'] = 'DummyCommand'

#
# The 'sn' field is used as a unique ID, which is reflected back in the response from MetPrint,
# and allows the client application to unambiguously match commands with their response.
# The easiest way to achieve this is to increment sn after each message is created.
#
sn = sn + 1

#
# Send the TCP/IP message and wait for a response (for the socket timeout period of 5 seconds)
#
SendMsg(msg)

#
# This sample application connects to MetPrint, sends a single message, and then disconnects / exits.
# A production application should normally keep running and maintain the socket connection, to avoid
# the overhead of repeated connect and disconnects
#
print("### MRA_PrintMode.py finished")

#####################################################################################################

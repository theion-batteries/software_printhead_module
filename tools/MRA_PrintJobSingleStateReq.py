#
# MRA_PrintJobSingleStateReq.py
#
# Sample code demonstrating how to send a MetPrint Remote API message to MetPrint
# to query the state of a specific document in a print job.
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

    print("### Meteor Remote Api Response:\n")
    for key in responseJson:
        print(key, '=', responseJson[key])


#####################################################################################################

#
# Set up the sample application command line options, e.g. displayed by calling 'python MRA_CurrentPrintJobStateReq.py --help' on the command line
#
parser = argparse.ArgumentParser()
parser.description = 'Sends a Meteor Remote API PrintJobSingleStateReq message and displays the response.'
parser.add_argument('-j',   '--jobid',          help="Remote Job Id assigned by the remote client", default='UnsetJobId')
parser.add_argument('-d',   '--docid',          help="Zero-based index of the document within the job", default=0)
parser.add_argument('-p',   '--port',           help='TCP/IP port, default=5555', type=int, default=5555)
parser.add_argument('-a',   '--address',        help='TCP/IP address, default=localhost', type=str, default='localhost')
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
sn = 7000

#
# Create a dictionary for the command.
# All Meteor Remote API messages include a 'cmd' and a 'sn' parameter.
# Other parameters are command specific
#
msg = dict()

#
# The command
#
msg['cmd'] = 'PrintJobSingleStateReq'
    
#
# Unique sequence number for this command
#
msg['sn'] = sn

#
# Remote Job Id.  This is the Id which is assigned by the remote system (e.g. the ERP system)
# when it creates a job
#
msg['jobid'] = args.jobid

#
# Index of the document within the job, the first document is docid = 0 etc.
#
msg['docid'] = args.docid

#
# The 'sn' field is used as a unique ID, which is reflected back in the response from MetPrint,
# and allows the client application to unambiguously match commands with their response.
# The easiest way to achieve this is to increment sn after each message is created.
#
sn = sn + 1

#
# Send the TCP/IP message and display the response, or timeout after 5 seconds if there's no
# response.
#
print(F"\n### Sending PrintJobSingleStateReq sn={sn} jobId={args.jobid} docId={args.docid}\n")
SendMsg(msg)
print("\n### MRA_PrintJobSingleStateReq.py exiting")

#####################################################################################################

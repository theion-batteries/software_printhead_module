#
# MRA_AddPrintJobReq.py
#
# Sample code demonstrating how to send a MetPrint Remote API message to MetPrint
# to add one or more print jobs.
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
        #
        # A longer timeout is set here than most of the other samples, because creating a
        # print job - which involves translating the image data, and then writing it to
        # the image store - can take quite a long time.  The 'AddPrintJobAck' response
        # message is not sent from MetPrint until the job set has been fully created
        # (or an error has occurred).
        #
        metPrintSocket.settimeout(60)
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
#
parser.add_argument('-j',   '--jobid',          nargs="+", required=True, help="Remote Job Id assigned by the remote client")
parser.add_argument('-f',   '--filename',       nargs="+", required=True, help="Full path to the local source file (group) in the hotfolder")
parser.add_argument('-r',   '--repeatnum',      nargs="+", required=True, help="The number of copies of the image to print")
#
parser.add_argument('-p',   '--port',           help='TCP/IP port, default=5555', type=int, default=5555)
parser.add_argument('-a',   '--address',        help='TCP/IP address, default=localhost', type=str, default='localhost')
args = parser.parse_args()


#
# Check that the command lines has the same number of jobids, filenames and repeat numbers
#
if len(args.jobid) != len(args.filename):
    print("*** The number of --jobid, --filename and --repeatnum arguments must be identical !!")
    sys.exit()


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
# The command
#
msg['cmd'] = 'AddPrintJobReq'
    
#
# Unique sequence number for this command.
# In a real application, 'sn' should be made unique for every message to protect against out of step
# REQ/ACK handshakes; in this sample we're just sending one message before exiting so it doesn't
# really matter.
#
msg['sn'] = 8888

#
# Create a list for the job requests
#
data = list()

for i in range(len(args.jobid)):

    #
    # Dictionary for this job request
    #
    job = dict()

    #
    # Remote Job Id.  This is the Id which is assigned by the remote system (e.g. the ERP system)
    # when it creates a job
    #
    job['jobid'] = args.jobid[i]
    
    #
    # The file name, stripped of the file extension and channel suffix.
    # e.g. if we have a group of files called FileName_Clr1.tif, FileName_Clr2.tif, etc. then we 
    # set "FileName" here.
    # The file path is not needed because it is assumed to be in the MetPrint hotfolder.
    #
    job['filename'] = args.filename[i]
    
    #
    # The number of copies of the file to print
    #
    job['repeatnum'] = args.repeatnum[i]

    #
    # There are various other parameters that can be added here, but none of them are
    # mandatory.  
    # 
    # e.g. ERP specific display data - which MetPrint displays but doesn't use - such as 
    #      'sheetheight', 'sheetlength', 'sheettype' and 'sheetwidth'
    #
    # There is also an optional integer 'yoffset' and 'yoffsetmode': the mode should be
    # 'centre' or 'top'
    #
    # 'jobname' can also be set: if left unset the job name will be the same as the 
    # filename
    #

    #
    # Add the 'AddPrintJobReqData' to the list which will be sent in the JSON message
    #
    data.append(job)

#
# The data for each new print job request
#
msg['data'] = data

#
# Send the TCP/IP message and display the response, or timeout after 60 seconds if there's no
# response.
#
# A relatively large timeout is used: for a large file it can take several seconds to translate 
# the print data and write it to the image store 
#
print(F"\n### Sending AddPrintJobReq {msg}\n")
SendMsg(msg)
print("\n### MRA_PrintJobSingleStateReq.py exiting")

#####################################################################################################

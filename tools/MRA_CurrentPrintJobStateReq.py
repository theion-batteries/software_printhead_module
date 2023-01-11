#
# MRA_CurrentPrintJobStateReq.py
#
# Sample code demonstrating how to send a MetPrint Remote API message to MetPrint
# to query the state of the current print job (if any).
#
# This script assume that the "Send Job State Changes" setting is **off** in MetPrint.

import argparse
import json
import socket
import sys
import time

#
# Text encoding used for encoding and decoding the Meteor Remote API (MRA) messages.
# This should match the value set in the MetPrint setup window (default is UTF-8).
#
MetPrintMsgEncoding = 'utf-8'

__jobId = "Unset"
__fileName = "Unset"
__jobState = "Unset"
__printedNum = 0
__startedNum = 0
__printingStarted = False;
__printingFinished = False;
__jobIdList = list()

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
def SendMsg(msg, verbose):
    data = json.JSONEncoder().encode(msg)
    if verbose:
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
    if verbose:
        print(F"### MRA Resp: {responseJson}")

    #
    # Handle the 'CurrentPrintJobStateAck' response.
    #
    # The current job is the job which has most recently started to print a document: it is possible that
    # previous jobs are still printing.  If the MetPrint print queue is stopped, or if the queue is running 
    # but no documents have started to print yet, we will get a 'JobNotExist' response in the 'jobState' field.
    #
    if responseJson['cmd'] == 'CurrentPrintJobStateAck':
        global __jobId, __fileName, __jobState, __printedNum, __startedNum
        global __printingStarted, __printingFinished, __jobIdList

        #    
        # Only do anything here if the information in the CurrentPrintJobStateAck message has changed
        #
        if __jobId != responseJson['jobId'] or __fileName != responseJson['fileName'] or __jobState != responseJson['jobState'] \
        or __printedNum != responseJson['printedNum'] or __startedNum != responseJson['startedNum']:

            #
            # Make a copy of the new details
            #
            __jobId = responseJson['jobId']
            __fileName = responseJson['fileName']
            __jobState = responseJson['jobState']
            __printedNum = responseJson['printedNum']
            __startedNum = responseJson['startedNum']

            #
            # Printing has started the first time we see a 'Printing' state
            #
            if __jobState == 'Printing':

                if not __printingStarted:
                    __printingStarted = True
                    print("=== Printing Started")

                if not __jobId in __jobIdList:
                    __jobIdList.append(__jobId)

            #
            # Log the updated job information
            #
            print(F"!!! jobId={__jobId}   fileName={__fileName}   jobState={__jobState}   printedNum={__printedNum}   startedNum={__startedNum}")

            #
            # Printing has stopped when the state goes back to 'JobNotExist' - i.e. the print queue has
            # emptied or printing has been stopped by the user
            #
            if __printingStarted and __jobState == 'JobNotExist':
                if not __printingFinished:
                    print("=== Printing Complete")
                    __printingFinished = True;

    #
    # Handle the 'PrintJobStateAck' response, this is used to report to final state of each job
    # at the end of the script
    #
    elif responseJson['cmd'] == 'PrintJobStateAck':

        print(F"=== JobId={responseJson['jobId']}   printedNum={responseJson['printedNum']}")

    #
    # We don't expect any other messages.
    # N.B. We will get 'JobStateChanged' messages if the "Send Job State Changes" setting is enabled in MetPrint, so it should be
    #      turned off when using this script.
    #
    else:
        print(F"### MRA Unexpected MetPrint response: {responseJson['cmd']}")


#####################################################################################################

#
# Set up the sample application command line options, e.g. displayed by calling 'python MRA_CurrentPrintJobStateReq.py --help' on the command line
#
parser = argparse.ArgumentParser()
parser.description = 'Sends a set of Meteor Remote API CurrentPrintJobStateReq commands.'
parser.add_argument('-s',   '--sleepms',        help='the number of milliseconds the script should sleep between CurrentPrintJobStateReq messages, default=1000', type=int, default=1000)
parser.add_argument('-c',   '--count',          help='the number of times the script should ask for the print job state before exiting, default=5', type=int, default=5)
parser.add_argument('-p',   '--port',           help='TCP/IP port, default=5555', type=int, default=5555)
parser.add_argument('-a',   '--address',        help='TCP/IP address, default=localhost', type=str, default='localhost')
parser.add_argument('-v',   '--verbose',        help='enable verbose logging', action='store_true')
parser.add_argument('-e',   '--exitAfterStop',  help='exit the script as soon as the job queue stops', action='store_true')
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
sn = 5000


#
# The number of times we send the CurrentPrintJobStateReq command is set by the -c option on the command line
#
for i in range(0, args.count):

    #
    # Create a dictionary for the command.
    # All Meteor Remote API messages include a 'cmd' and a 'sn' parameter.
    # Other parameters are command specific
    #
    msg = dict()

    #
    # The command
    #
    msg['cmd'] = 'CurrentPrintJobStateReq'
    
    #
    # Unique sequence number for this command
    #
    msg['sn'] = sn

    #
    # The 'sn' field is used as a unique ID, which is reflected back in the response from MetPrint,
    # and allows the client application to unambiguously match commands with their response.
    # The easiest way to achieve this is to increment sn after each message is created.
    #
    sn = sn + 1

    #
    # Send the TCP/IP message and wait for a response (for the socket timeout period of 5 seconds)
    #
    SendMsg(msg, args.verbose)

    #
    # We've (1) seen at least one document start to print, and (2) we've also has a subsequent
    # 'JobNotExist' response, meaning that either the user has pressed the Stop button in
    # MetPrint, or all job sets in the queue have finished printing
    #
    if __printingStarted and __printingFinished:
        #
        # Report the final state for every job ID that we've seen while MetPrint was printing
        #
        for jobId in __jobIdList:
            msg = dict()
            msg['cmd'] = 'PrintJobStateReq'
            msg['sn'] = sn
            sn = sn + 1
            msg['jobid'] = jobId
            SendMsg(msg, args.verbose)    

        #
        # Optionally finish after we've seen printing finish, or go round again for the next
        # set of jobs
        #        
        if args.exitAfterStop:
            break
        else:
            __printingStarted = False
            __printingFinished = False
            __jobIdList.clear()

    #
    # Sleep for the given number of seconds before sending the next command
    #
    time.sleep(args.sleepms / 1000.0)

print("### MRA_CurrentPrintJobStateReq.py exiting")

#####################################################################################################

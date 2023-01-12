/* SamplePrint.cpp
*
* Copyright (c) 2007-2022, Meteor Inkjet Ltd.
*/

// Simple example program for printing using Meteor
// 
// For instructions on usage, run the programme with no arguments.
// PrinterInterface.dll must be present in the same directory as SamplePrint.exe
//
// This code demonstrates printing a single document using the FIFO or
// Preload path. It can also print two swaths with scanning printing.
//
// By default, this program will print a single image on the Preload path.
// The user can specify the file to be printed, and override the default options,
// from the command line.
//
// Many of the commands in this file are followed by explanations of what to look 
// for in the Monitor debug window, when the command executes
#pragma once

#include "stdafx.h"

// Utility functions for handling bitmaps and generating image commands in the correct format
#include "Bitmaps.h"

// Function declarations
void InitialisePrinter(int scanning);
bool StartJob(DWORD jobid, DWORD jobtype, DWORD res, DWORD docwidth);
void Start(int scanning, DWORD jobtype, DWORD ncopies, DWORD docid);
void SendImage(uint32* buffer);
void ScanSendSecondDoc(uint32* SecondBuffer);
void EndDoc(void);
void EndJob(void);
void SendAbort(void);

//void ParseArguments(int argc, _TCHAR* argv[], DWORD* jobtype,
//                    DWORD* ncopies, int* scanning, _TCHAR** bitmap2);

int CheckScan(int scanning, DWORD jobtype, const _TCHAR* bitmap2, uint32** SecondBuffer);
void PrintUsage(void);

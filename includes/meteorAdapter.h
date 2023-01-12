#pragma once

#include <iostream>
//#include "PrinterInterface.h"
#include "hardware_feedback.h"
#include "SamplePrint.h"

struct PrintingParameters
{
    DWORD jobid = 0;					// Default to 0
    DWORD jobtype = JT_PRELOAD;			// Default to Preload path
    DWORD res = RES_HIGH;				// Default to high resolution
    DWORD docwidth = 3508;				// Default to A4 length @ 300dpi
    DWORD ncopies = 1;					// Default to 1 copy of the document
    DWORD docid = 1;					// Default to a document ID of 1
    int scanning = 0;					// Default to not scanning
};
class meteorAdapter
{
public:

    wgm_feedbacks::enum_hw_feedback connect();
    wgm_feedbacks::enum_hw_feedback disconnect();
    wgm_feedbacks::enum_hw_feedback turnOnPh();
    wgm_feedbacks::enum_hw_feedback turnOffPh();
    void setImgPath(_TCHAR* ImgPath);
    wgm_feedbacks::enum_hw_feedback startPrinting();
    wgm_feedbacks::enum_hw_feedback endPrinting();


private:
    bool connected = false;
    bool headPowered = false;
    _TCHAR* bitmap1 = NULL;
    PrintingParameters PrinterParams;

};
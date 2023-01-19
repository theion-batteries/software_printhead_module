#pragma once

#include <iostream>
//#include "PrinterInterface.h"
#include "hardware_feedback.h"
#include "SamplePrint.h"

struct cooling_config_yaml_params
{
    double distance_to_center = 50; // after homing = go to center position where cnt dispenser will vibrate
    double ph_rotate_to_center= 10; // after homing: rotate the ph x angle to be centered
    int number_of_rotation_per_direction = 10; // frequency for dispensing
    bool reverse_direction = false; // duration of vibration 100 ms
    std::string path_to_upload_img = ""; //optional path for img direct load
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
    meteorAdapter(cooling_config_yaml_params& configPtr);
    wgm_feedbacks::enum_hw_feedback connect();
    wgm_feedbacks::enum_hw_feedback disconnect();
    wgm_feedbacks::enum_hw_feedback turnOnPh();
    wgm_feedbacks::enum_hw_feedback turnOffPh();
    void setImgPath(_TCHAR* ImgPath);
    wgm_feedbacks::enum_hw_feedback startPrinting();
    wgm_feedbacks::enum_hw_feedback endPrinting();
    bool getStatus();


private:
    bool connected = false;
    bool headPowered = false;
    _TCHAR* bitmap1 = NULL;
    cooling_config_yaml_params PrinterParams;

};
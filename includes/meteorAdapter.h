#pragma once

#include <iostream>
//#include "PrinterInterface.h"
#include "hardware_feedback.h"
#include "SamplePrint.h"

struct cooling_config_yaml_params
{
    double distance_to_center = 150; // after homing = go to center position where cnt dispenser will vibrate
    double ph_rotate_to_center = 90; // after homing: rotate the ph x angle to be centered
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
    uint16_t timeout =10;
    std::string ph_motion_server_ip = "192.168.0.205"; //# 192.168.0.209 "127.0.0.1"
    uint16 ph_motion_server_port = 8882;
    std::string ph_rotation_server_ip = "192.168.0.205"; //# 192.168.0.209 "127.0.0.1" # rotation / trigger
    uint16 ph_rotation_server_port = 8882;
    std::string ph_trigger_server_ip = "192.168.0.205"; //# 192.168.0.209 "127.0.0.1" # trigger / trigger
    uint16 ph_trigger_server_port = 8881;
    uint16 timeout = 10;
    double phead_travel = 150;
    double phead_max_travel = 220;
    double phead_rotations = 5;
    double phead_max_rotations = 50;
    double phead_max_linear_speed = 400;
    double phead_max_rot_speed = 100;
    double phead_intermediate_stop = 50;    //                        # so printhead will stop here, rotate the angle defined by the following parameter, and keep going.
    double phead_start_angle = 90; //                       # before moving the printhead to the cooling surface, it needs to be rotated.
};
class meteorAdapter
{
public:
    meteorAdapter(cooling_config_yaml_params& configPtr);
    wgm_feedbacks::enum_hw_feedback connect();
    wgm_feedbacks::enum_hw_feedback disconnect();
    wgm_feedbacks::enum_hw_feedback turnOnPh();
    wgm_feedbacks::enum_hw_feedback turnOffPh();
    wgm_feedbacks::enum_hw_feedback  setImgPath(_TCHAR* ImgPath);
    wgm_feedbacks::enum_hw_feedback startPrinting();
    wgm_feedbacks::enum_hw_feedback endPrinting();
    bool getStatus();


private:
    bool connected = false;
    bool headPowered = false;
    _TCHAR* bitmap1 = NULL;
    cooling_config_yaml_params PrinterParams;

};
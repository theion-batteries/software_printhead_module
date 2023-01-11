#pragma once

#include <iostream>
#include "PrinterInterface.h"
#include "hardware_feedback.h"

class meteorAdapter
{
    public:

    wgm_feedbacks::enum_hw_feedback connect();
    wgm_feedbacks::enum_hw_feedback disconnect();
    wgm_feedbacks::enum_hw_feedback turnOnPh();
    wgm_feedbacks::enum_hw_feedback turnOffPh();

    
    private:
    bool connected = false;
    bool headPowered = false;


};
/**
 * @file feedback_management.h
 * @author sami dhiab (sami@theion.de)
 * @brief feedback managment file
 * @version 0.1
 * @date 2022-07-07
 *
 * @copyright Copyright (c) 2022
 *
 */
#pragma once
#ifndef _HARDWARE_FEEDBACK
#define _HARDWARE_FEEDBACK
#include <iostream>

namespace wgm_feedbacks
{
    /********* enumeration classes ***********/

     enum class enum_hw_feedback
    {
        hw_success = 4,
        hw_error = -3
    };
    /*********** feedback classes *************/
     class hw_feedback
    {
        private:
            enum_hw_feedback hw_feed_val;
    
        public:
            inline void report_feedback (enum_hw_feedback& feedback);
    };
 

}


 void wgm_feedbacks::hw_feedback::report_feedback(enum_hw_feedback& feedback)
{
  if (feedback == enum_hw_feedback::hw_success) hw_feed_val = enum_hw_feedback::hw_success;
  else hw_feed_val = enum_hw_feedback::hw_error;
}

#endif
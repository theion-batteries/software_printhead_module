#include "meteorAdapter.h"


wgm_feedbacks::enum_hw_feedback meteorAdapter::connect()
{

    std::cout << "connecting to PRINT ENGINE SERVER" << std::endl;
    eRET open = PiOpenPrinter();

    if (open != eRET::RVAL_OK)
    {
        std::cout << "error connection, see code: " << open << std::endl;
        return wgm_feedbacks::enum_hw_feedback::hw_error;
    }
    connected = true;

    std::cout << "Print Engine connection success" << std::endl;
    return wgm_feedbacks::enum_hw_feedback::hw_success;
}
wgm_feedbacks::enum_hw_feedback meteorAdapter::disconnect()
{

    std::cout << "disconnecting.." << std::endl;
    eRET close = PiClosePrinter();

    if (close != eRET::RVAL_OK)
    {
        std::cout << "error disconnection, see code: " << close << std::endl;
        return wgm_feedbacks::enum_hw_feedback::hw_error;
    }

    std::cout << "Print Engine disconnection success" << std::endl;
    connected = false;
    return wgm_feedbacks::enum_hw_feedback::hw_success;
}

wgm_feedbacks::enum_hw_feedback meteorAdapter::turnOnPh()
{
    std::cout << "powering print head on" << std::endl;

    eRET poweron = PiSetHeadPower(1);
    if (poweron != eRET::RVAL_OK)
    {
        std::cout << "error power on, see code: " << poweron << std::endl;
        return wgm_feedbacks::enum_hw_feedback::hw_error;
    }

    std::cout << "head Power on success" << std::endl;
    headPowered = true;
    return wgm_feedbacks::enum_hw_feedback::hw_success;

}
wgm_feedbacks::enum_hw_feedback meteorAdapter::turnOffPh()
{
    std::cout << "powering  print head off" << std::endl;

    eRET poweroff = PiSetHeadPower(0);
    if (poweroff != eRET::RVAL_OK)
    {
        std::cout << "error power off, see code: " << poweroff << std::endl;
        return wgm_feedbacks::enum_hw_feedback::hw_error;
    }

    std::cout << "head Power off success" << std::endl;
    headPowered = false;
    return wgm_feedbacks::enum_hw_feedback::hw_success;

}
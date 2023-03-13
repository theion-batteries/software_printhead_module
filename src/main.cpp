#include "meteorAdapter.h"
#include <chrono>
#include <thread>

void testApi1(meteorAdapter* phIntptr);
void testApi2(meteorAdapter* phIntptr);
_TCHAR img[] = "C:/Users/PrintHead/Desktop/dev_sami/software_printhead_module/docs/dots.bmp";
cooling_config_yaml_params configPtr;
int main()
{
    //testApi1(new meteorAdapter);
    testApi2(new meteorAdapter(configPtr));
}

void testApi1(meteorAdapter* phIntptr)
{
     std::cout << "***************************  testing meteor sdk apis *****************************" << "\n";
    std::cout << "eret functions tests" << "\n";
    std::cout << "test succes return code: 0 " << "\n";
    std::cout << "test error return code: see docs " << "\n";

    std::cout << "test1: open connection to print engine (print engine must be running !)" << "\n";
    phIntptr->connect();
    std::cout << "test2: set head power on" << "\n";
 
    phIntptr->turnOnPh();

    std::this_thread::sleep_for(std::chrono::seconds(20));

    std::cout << "test3: set head power off" << "\n";
    phIntptr->turnOffPh();

    std::cout << "test4: close connection to print engine (print engine must be running !)" << "\n";
    phIntptr->disconnect();

    std::cout << "bool functions tests" << "\n";
    std::cout << "test4: is printer busy" << "\n";
    bool status = PiIsBusy();
    std::cout << "return code: " << status << "\n";
    delete phIntptr;
}

void testApi2(meteorAdapter* phIntptr)
{
phIntptr->connect();
phIntptr->setImgPath(img);
phIntptr->startPrinting();
phIntptr->disconnect();
}

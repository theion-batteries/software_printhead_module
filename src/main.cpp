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
     std::cout << "***************************  testing meteor sdk apis *****************************" << std::endl;
    std::cout << "eret functions tests" << std::endl;
    std::cout << "test succes return code: 0 " << std::endl;
    std::cout << "test error return code: see docs " << std::endl;

    std::cout << "test1: open connection to print engine (print engine must be running !)" << std::endl;
    phIntptr->connect();
    std::cout << "test2: set head power on" << std::endl;
 
    phIntptr->turnOnPh();

    std::this_thread::sleep_for(std::chrono::seconds(20));

    std::cout << "test3: set head power off" << std::endl;
    phIntptr->turnOffPh();

    std::cout << "test4: close connection to print engine (print engine must be running !)" << std::endl;
    phIntptr->disconnect();

    std::cout << "bool functions tests" << std::endl;
    std::cout << "test4: is printer busy" << std::endl;
    bool status = PiIsBusy();
    std::cout << "return code: " << status << std::endl;
    delete phIntptr;
}

void testApi2(meteorAdapter* phIntptr)
{
phIntptr->connect();
phIntptr->setImgPath(img);
phIntptr->startPrinting();
phIntptr->disconnect();
}

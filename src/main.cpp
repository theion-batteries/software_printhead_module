#include "meteorAdapter.h"
#include <chrono>
#include <thread>

meteorAdapter phInterface;

int main()
{
    std::cout << "***************************  testing meteor sdk apis *****************************" << std::endl;
    std::cout << "eret functions tests" << std::endl;
    std::cout << "test succes return code: 0 " << std::endl;
    std::cout << "test error return code: see docs " << std::endl;

    std::cout << "test1: open connection to print engine (print engine must be running !)" << std::endl;
    phInterface.connect();
    std::cout << "test2: set head power on" << std::endl;
 
    phInterface.turnOnPh();

    std::this_thread::sleep_for(std::chrono::seconds(20));

    std::cout << "test3: set head power off" << std::endl;
    phInterface.turnOffPh();

    std::cout << "test4: close connection to print engine (print engine must be running !)" << std::endl;
    phInterface.disconnect();

    std::cout << "bool functions tests" << std::endl;
    std::cout << "test4: is printer busy" << std::endl;
    bool status = PiIsBusy();
    std::cout << "return code: " << status << std::endl;

}


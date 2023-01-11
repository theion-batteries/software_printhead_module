

#include "meteorAdapter.h"
int main()
{
    eRET open = PiOpenPrinter();
    //uint32 buffer[4] = { PCMD_STARTJOB, 4, 1, JT_SCAN };
    //auto cmd = PiSendCommand(buffer);
    std::cout << open << std::endl;
    eRET power = PiSetHeadPower(1);
    std::cout << power << std::endl;
    bool status = PiIsBusy();
    std::cout << status << std::endl;
    /*for (const auto& b : buffer) {
        std::cout << power << std::endl;
        std::cout << b << std::endl;
    }*/
    


}


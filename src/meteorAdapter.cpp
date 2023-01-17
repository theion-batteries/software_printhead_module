#include "meteorAdapter.h"

meteorAdapter::meteorAdapter(cooling_config_yaml_params& configPtr)
{
PrinterParams=configPtr;
}

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

void meteorAdapter::setImgPath(_TCHAR* ImgPath)
{
    bitmap1 = ImgPath;
}
wgm_feedbacks::enum_hw_feedback meteorAdapter::startPrinting()
{
    if (bitmap1 == NULL) // we couldn'T loaded the img
    {
        puts("no image loaded");
        return wgm_feedbacks::enum_hw_feedback::hw_error;
    }

    auto ImageBuffer = MakeBitmap(bitmap1);

    // redo same img in opposite direction
    if (CheckScan(PrinterParams.scanning, PrinterParams.jobtype, bitmap1, &ImageBuffer)) {
        // Everything ok, so start printing now

        // Reset the printer
        InitialisePrinter(PrinterParams.scanning);

        // Specify the parameters of the job
        if (StartJob(PrinterParams.jobid, PrinterParams.jobtype, PrinterParams.res, PrinterParams.docwidth)) {

            //
            // Number of documents to send.  For FIFO, each copy of the
            // document is sent by the application; FIFO is typically used for
            // variable data, although in this example all documents are identical.  
            // For preload, the document is repeated from PCC memory, so only
            // needs to be sent once
            //
            int cycle = (JT_PRELOAD == PrinterParams.jobtype) ? 1 : PrinterParams.ncopies;

            for (int i = 0; i < cycle; i++) {

                // Start the document
                Start(PrinterParams.scanning, PrinterParams.jobtype, PrinterParams.ncopies, PrinterParams.docid);

                // Send the image.  We already created the header when we generated the ImageBuffer,
                // so all we need to do here is send the ImageBuffer
                puts("Sending Image");
                SendImage(ImageBuffer);

                // Finished sending images, send the end doc command
                EndDoc();

                // If using PrinterParams.scanning printing, send the second document
                if (PrinterParams.scanning) {
                    ScanSendSecondDoc(ImageBuffer);
                }

            }

            // Finished sending the document, send the end job command
            EndJob();

        }


    }

    free(ImageBuffer);
    return wgm_feedbacks::enum_hw_feedback::hw_success;

}


wgm_feedbacks::enum_hw_feedback meteorAdapter::endPrinting()
{
    EndJob();
    return wgm_feedbacks::enum_hw_feedback::hw_success;

}


bool meteorAdapter::getStatus()
{
    return connected;
}

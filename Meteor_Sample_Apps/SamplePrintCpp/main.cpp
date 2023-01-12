#include "SamplePrint.h"

//---------------------------------------------------------------------------
int main(int argc, _TCHAR* argv[]) {

    _TCHAR* bitmap1 = NULL; _TCHAR* bitmap2 = NULL;
    uint32* ImageBuffer = NULL; uint32* SecondBuffer = NULL;

    eRET retval; // For return values from function calls

    DWORD jobid = 0;					// Default to 0
    DWORD jobtype = JT_PRELOAD;			// Default to Preload path
    DWORD res = RES_HIGH;				// Default to high resolution
    DWORD docwidth = 3508;				// Default to A4 length @ 300dpi
    DWORD ncopies = 1;					// Default to 1 copy of the document
    DWORD docid = 1;					// Default to a document ID of 1
    int scanning = 0;					// Default to not scanning

    // Parse the input arguments

    // The first argument is the filename of the bitmap to print
    if(argc < 2) {
        PrintUsage();
    } else {
        bitmap1 = argv[1];

        ParseArguments(argc, argv, &jobtype, &ncopies, &scanning, &bitmap2);

        // Connect to the printer first
        retval = PiOpenPrinter();	// Open the printer interface
        // Look out for Monitor log message:  "Application Attached"

        if(RVAL_OK != retval) {
            puts("Error, unable to open printer interface...is Monitor.exe running?");
        } else {

            // Printer interface opened ok
            puts("Printer interface opened");

            // Attempt to open the file and create the image command, for later use.
            ImageBuffer = MakeBitmap(bitmap1);

            if (ImageBuffer != NULL) {

                if(CheckScan(scanning,jobtype,bitmap2,&SecondBuffer)) {
                    // Everything ok, so start printing now

                    // Reset the printer
                    InitialisePrinter(scanning);

                    // Specify the parameters of the job
                    if ( StartJob(jobid, jobtype, res, docwidth) ) {

                        //
                        // Number of documents to send.  For FIFO, each copy of the
                        // document is sent by the application; FIFO is typically used for
                        // variable data, although in this example all documents are identical.  
                        // For preload, the document is repeated from PCC memory, so only
                        // needs to be sent once
                        //
                        int cycle = (JT_PRELOAD == jobtype) ? 1 : ncopies;

                        for (int i = 0; i < cycle; i++ ) {

                            // Start the document
                            Start(scanning,jobtype,ncopies, docid);

                            // Send the image.  We already created the header when we generated the ImageBuffer,
                            // so all we need to do here is send the ImageBuffer
                            puts("Sending Image");
                            SendImage(ImageBuffer);			

                            // Finished sending images, send the end doc command
                            EndDoc();

                            // If using scanning printing, send the second document
                            if(scanning) {
                                ScanSendSecondDoc(SecondBuffer);
                            }

                        }

                        // Finished sending the document, send the end job command
                        EndJob();

                    }

                    if(SecondBuffer) {
                        free(SecondBuffer);
                    }
                }
                free(ImageBuffer);
            }

            // All done now, close the printer interface, by calling PiClosePrinter until the interface closes
            puts("Closing Printer Interface");
            while ( !PiCanClosePrinter() ) { 
                Sleep(100);
            }
            while (RVAL_OK != PiClosePrinter()) {}
            // Look out for Monitor log message: "Application Detached"
        }
    }
    puts("Press Enter to continue...");
    getchar();
    return 0;
}

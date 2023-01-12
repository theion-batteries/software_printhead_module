#pragma once
#include "stdafx.h"

// ----------------------------------------------------------------------------------------------------------------------------------------------- //
/**
    Looks in the registry to find the install location of the Meteor PrintEngine / PrinterInterface,
    and sets this as the DLL load directory (SetDllDirectory).

    @param abAdd32BitRuntime        true:   add the 32 bit runtime to SetDllDirectory (available in both a 32 bit and 64 bit install)
                                    false:  add the 64 bit runtime to SetDllDirectory (only available in a 64 bit install)
*/
void AddMeteorPath(bool abAdd32BitRuntime); 
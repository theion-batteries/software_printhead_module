// stdafx.h : include file for standard system include files,
// or project specific include files that are used frequently, but
// are changed infrequently
//

#pragma once

#define WIN32_LEAN_AND_MEAN		// Exclude rarely-used stuff from Windows headers
#include <stdio.h>
#include <tchar.h>

#include <windows.h>
#include <time.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <assert.h>

// TODO: reference additional headers your program requires here


// Standard libraries

// Image handling libraries
#include <atlimage.h>			// For bitmap handling

// Meteor specific includes
#include "PrinterInterface.h"	// Contains definitions for all the Meteor library functions
#include "Meteor.h"				// Definition of common datatypes and constants
#include "typedef.h"


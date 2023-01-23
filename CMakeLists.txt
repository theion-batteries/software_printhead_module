############################
###### Cmake template ######
############################

# author: sami dhiab
# email: sami@theion.de

# only for cmake --version >= 3.5.1
cmake_minimum_required(VERSION 3.1.0)
# project name
project(meteorSDK VERSION "1.0")
# set the C++20 standard
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
#This is necessary for MSVC to create a symbol file, .lib, besides a shared library, .dll
if (MSVC)
    set(CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS ON)
endif()
add_subdirectory(Dep/meteor)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/$<CONFIG>) 

###################### Build Library ############################
file(GLOB lib_SRCS
		"${CMAKE_CURRENT_SOURCE_DIR}/src/meteorAdapter.cpp"
    "${CMAKE_CURRENT_SOURCE_DIR}/src/Bitmaps.cpp"
    "${CMAKE_CURRENT_SOURCE_DIR}/src/MeteorPath.cpp"
    "${CMAKE_CURRENT_SOURCE_DIR}/src/SamplePrint.cpp"
    "${CMAKE_CURRENT_SOURCE_DIR}/src/stdafx.cpp"
)
add_library(ph_interface_lib STATIC ${lib_SRCS})
target_link_libraries(ph_interface_lib PUBLIC ${PrinterInterfaceLib} )
target_include_directories(ph_interface_lib 
PUBLIC  ${CMAKE_CURRENT_SOURCE_DIR}/includes/
PUBLIC  ${METEOR_INC}
)
set_target_properties(
    ph_interface_lib
    PROPERTIES
      INTERFACE_INCLUDE_DIRECTORIES ${METEOR_INC}
      IMPORTED_LOCATION ${METEOR_LIBS}
)
copy_dlls_meteor_target_destination(ph_interface_lib)

############################# build executable  ###################################
file(GLOB exe_SRCS
"${CMAKE_CURRENT_SOURCE_DIR}/src/*.cpp"
)
add_executable(ph_interface_exe ${exe_SRCS})
target_link_libraries(ph_interface_exe PUBLIC ${PrinterInterfaceLib} )#${PrinterInterfaceDll} ${PrintEngine} ${MeteorCLSdll} ${PrinterInterfaceCLSdll})
target_include_directories(ph_interface_exe 
PUBLIC  ${CMAKE_CURRENT_SOURCE_DIR}/includes/
PUBLIC  ${METEOR_INC}
)
set_target_properties(
    ph_interface_exe
    PROPERTIES
      INTERFACE_INCLUDE_DIRECTORIES ${METEOR_INC}
      IMPORTED_LOCATION ${METEOR_LIBS}
)
copy_dlls_meteor_target_destination(ph_interface_exe)
############################# install targets ########################################
FILE(GLOB files "${CMAKE_CURRENT_SOURCE_DIR}/includes/*.h"  "${METEOR_INC}/*.h"
)
install(FILES ${files} DESTINATION include/ph_interface_lib/)
FILE(GLOB meteor_dlls  "${CMAKE_CURRENT_SOURCE_DIR}/Dep/meteor/lib/*.dll"  )
install(FILES ${meteor_dlls} 
RUNTIME DESTINATION bin/Debug
)
install(TARGETS ph_interface_exe ph_interface_lib
RUNTIME DESTINATION bin/Debug
)

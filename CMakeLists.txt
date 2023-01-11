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
###################### find libraries #############################
find_library( PrinterInterfaceLib 
	NAMES "PrinterInterface.lib"
	PATHS "${CMAKE_CURRENT_SOURCE_DIR}/Dep/meteor/lib/PrinterInterface.lib"
	NO_DEFAULT_PATH
  REQUIRED
)
find_library( PrinterInterfaceDll 
	NAMES "PrinterInterface.dll"
	PATHS "${CMAKE_CURRENT_SOURCE_DIR}/Dep/meteor/lib/PrinterInterface.dll"
	NO_DEFAULT_PATH
  REQUIRED
)
find_library( PrintEngine 
	NAMES "PrintEngine.dll"
	PATHS "${CMAKE_CURRENT_SOURCE_DIR}/Dep/meteor/lib/PrintEngine.dll"
	NO_DEFAULT_PATH
  REQUIRED
)
find_library( MeteorCLSdll 
	NAMES "MeteorCLS.dll"
	PATHS "${CMAKE_CURRENT_SOURCE_DIR}/Dep/meteor/lib/MeteorCLS.dll"
	NO_DEFAULT_PATH
  REQUIRED
)
find_library( PrinterInterfaceCLSdll 
	NAMES "PrinterInterfaceCLS.dll"
	PATHS "${CMAKE_CURRENT_SOURCE_DIR}/Dep/meteor/lib/PrinterInterfaceCLS.dll"
	NO_DEFAULT_PATH
  REQUIRED
)

find_path(
  METEOR_INC
  NAMES Meteor.h PrinterInterface.h typedef.h
  NO_DEFAULT_PATH
  HINTS "${CMAKE_CURRENT_SOURCE_DIR}/Dep/meteor/include"
)

message("found meteor libs ${PrinterInterfaceLib}")
message("found meteor includes ${METEOR_INC}")

add_library( PrinterInterfaceLib STATIC IMPORTED  GLOBAL)
set_target_properties( PrinterInterfaceLib PROPERTIES IMPORTED_LOCATION "${CMAKE_CURRENT_SOURCE_DIR}/Dep/meteor/lib/PrinterInterface.lib")

add_library( PrinterInterfaceDll SHARED IMPORTED  GLOBAL)
set_target_properties( PrinterInterfaceDll PROPERTIES IMPORTED_LOCATION "${CMAKE_CURRENT_SOURCE_DIR}/Dep/meteor/lib/PrinterInterface.dll")

add_library( PrintEngine SHARED IMPORTED  GLOBAL)
set_target_properties( PrintEngine PROPERTIES IMPORTED_LOCATION "${CMAKE_CURRENT_SOURCE_DIR}/Dep/meteor/lib/PrintEngine.dll")

add_library( MeteorCLSdll SHARED IMPORTED  GLOBAL)
set_target_properties( MeteorCLSdll PROPERTIES IMPORTED_LOCATION "${CMAKE_CURRENT_SOURCE_DIR}/Dep/meteor/lib/MeteorCLS.dll")

add_library( PrinterInterfaceCLSdll SHARED IMPORTED  GLOBAL)
set_target_properties( PrinterInterfaceCLSdll PROPERTIES IMPORTED_LOCATION "${CMAKE_CURRENT_SOURCE_DIR}/Dep/meteor/lib/PrinterInterfaceCLS.dll")

###################### Build Library ############################

file(GLOB lib_SRCS
		"${CMAKE_CURRENT_SOURCE_DIR}/src/meteorAdapter.cpp"
)
add_library(ph_interface_lib STATIC ${lib_SRCS})

target_link_libraries(ph_interface_lib ${PrinterInterfaceLib} ${PrinterInterfaceDll} ${PrintEngine} ${MeteorCLSdll} ${PrinterInterfaceCLSdll} )

target_include_directories(ph_interface_lib 
PUBLIC  ${CMAKE_CURRENT_SOURCE_DIR}/includes/
PUBLIC  ${CMAKE_CURRENT_SOURCE_DIR}/Dep/meteor/include/
)
set_target_properties(
    ph_interface_lib
    PROPERTIES
      INTERFACE_INCLUDE_DIRECTORIES ${METEOR_INC}
      IMPORTED_LOCATION ${PrinterInterfaceLib}
)
# copy dlls one by one 
function(copy_dlls_target_dir target_exe)
add_custom_command(TARGET ${target_exe} POST_BUILD
COMMAND ${CMAKE_COMMAND} -E copy_if_different  $<TARGET_FILE:PrinterInterfaceDll> ${CMAKE_RUNTIME_OUTPUT_DIRECTORY} 
COMMAND ${CMAKE_COMMAND} -E copy_if_different  $<TARGET_FILE:PrintEngine> ${CMAKE_RUNTIME_OUTPUT_DIRECTORY} 
COMMAND ${CMAKE_COMMAND} -E copy_if_different  $<TARGET_FILE:MeteorCLSdll> ${CMAKE_RUNTIME_OUTPUT_DIRECTORY} 
COMMAND ${CMAKE_COMMAND} -E copy_if_different  $<TARGET_FILE:PrinterInterfaceCLSdll> ${CMAKE_RUNTIME_OUTPUT_DIRECTORY} 
COMMAND_EXPAND_LISTS)
endfunction()


############################# install target lib ########################################
install(TARGETS ph_interface_lib DESTINATION lib
RUNTIME DESTINATION bin

)

copy_dlls_target_dir(ph_interface_lib)

FILE(GLOB files "${CMAKE_CURRENT_SOURCE_DIR}/includes/*.h"  "${METEOR_INC}/*.h"
)
install(FILES ${files} DESTINATION include/ph_interface_lib/)
FILE(GLOB meteor_dlls  "${CMAKE_CURRENT_SOURCE_DIR}/Dep/meteor/lib/*.dll"  )
install(FILES ${meteor_dlls} DESTINATION ${CMAKE_RUNTIME_OUTPUT_DIRECTORY})



############################# build executable  ###################################


file(GLOB exe_SRCS
		"${CMAKE_CURRENT_SOURCE_DIR}/Dep/meteor/*.cpp"
		"${CMAKE_CURRENT_SOURCE_DIR}/src/*.cpp"
)
add_executable(ph_interface_exe ${exe_SRCS})

target_link_libraries(ph_interface_exe ${PrinterInterfaceLib} ${PrinterInterfaceDll} ${PrintEngine} ${MeteorCLSdll} ${PrinterInterfaceCLSdll})

target_include_directories(ph_interface_exe 
PUBLIC  ${CMAKE_CURRENT_SOURCE_DIR}/includes/
PUBLIC  ${CMAKE_CURRENT_SOURCE_DIR}/Dep/meteor/include/
)

set_target_properties(
    ph_interface_exe
    PROPERTIES
      INTERFACE_INCLUDE_DIRECTORIES ${METEOR_INC}
      IMPORTED_LOCATION ${PrinterInterfaceLib}
)




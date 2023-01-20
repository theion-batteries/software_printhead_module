
find_library( PrinterInterfaceLib 
NAMES PrinterInterface PrintEngine MeteorCLS PrinterInterfaceCLS
PATHS "${CMAKE_CURRENT_SOURCE_DIR}/lib/"
NO_DEFAULT_PATH
REQUIRED
)

find_path(
METEOR_INC
NAMES Meteor.h PrinterInterface.h typedef.h
NO_DEFAULT_PATH
HINTS "${CMAKE_CURRENT_SOURCE_DIR}/include/"
REQUIRED
)
find_file(
METEOR_LIBS
NAMES PrinterInterface.lib PrinterInterface.dll PrintEngine.dll MeteorCLS.dll PrinterInterfaceCLS.dll  
NO_DEFAULT_PATH
HINTS "${CMAKE_CURRENT_SOURCE_DIR}/lib/"
REQUIRED
)

message("found meteor libs ${PrinterInterfaceLib}")
message("found meteor includes ${METEOR_INC}")

add_library( PrinterInterfaceLib STATIC IMPORTED  GLOBAL)
set_target_properties( PrinterInterfaceLib PROPERTIES IMPORTED_LOCATION ${CMAKE_CURRENT_SOURCE_DIR}/lib/PrinterInterface.lib)

add_library( PrinterInterfaceDll SHARED IMPORTED  GLOBAL)
set_target_properties( PrinterInterfaceDll PROPERTIES IMPORTED_LOCATION ${CMAKE_CURRENT_SOURCE_DIR}/lib/PrinterInterface.dll)

add_library( PrintEngine SHARED IMPORTED  GLOBAL)
set_target_properties( PrintEngine PROPERTIES IMPORTED_LOCATION ${CMAKE_CURRENT_SOURCE_DIR}/lib/PrintEngine.dll)

add_library( MeteorCLSdll SHARED IMPORTED  GLOBAL)
set_target_properties( MeteorCLSdll PROPERTIES IMPORTED_LOCATION ${CMAKE_CURRENT_SOURCE_DIR}/lib/MeteorCLS.dll)

add_library( PrinterInterfaceCLSdll SHARED IMPORTED  GLOBAL)
set_target_properties( PrinterInterfaceCLSdll PROPERTIES IMPORTED_LOCATION ${CMAKE_CURRENT_SOURCE_DIR}/lib/PrinterInterfaceCLS.dll)

# copy dlls one by one 
function(copy_dlls_target_dir target_exe)
add_custom_command(TARGET ${target_exe} POST_BUILD
COMMAND ${CMAKE_COMMAND} -E copy_if_different  $<TARGET_FILE:PrinterInterfaceDll> $<TARGET_FILE_DIR:${target_exe}> 
COMMAND ${CMAKE_COMMAND} -E copy_if_different  $<TARGET_FILE:PrintEngine> $<TARGET_FILE_DIR:${target_exe}> 
COMMAND ${CMAKE_COMMAND} -E copy_if_different  $<TARGET_FILE:MeteorCLSdll> $<TARGET_FILE_DIR:${target_exe}> 
COMMAND ${CMAKE_COMMAND} -E copy_if_different  $<TARGET_FILE:PrinterInterfaceCLSdll> $<TARGET_FILE_DIR:${target_exe}> 
COMMAND_EXPAND_LISTS)
endfunction()
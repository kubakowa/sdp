# Install script for directory: /afs/inf.ed.ac.uk/user/s12/s1263586/sdp/Polygon2-2.0.6/argparse-1.2.1/opencv-2.4.8.1/include

# Set the install prefix
IF(NOT DEFINED CMAKE_INSTALL_PREFIX)
  SET(CMAKE_INSTALL_PREFIX "/afs/inf.ed.ac.uk/user/s12/s1263586/.local")
ENDIF(NOT DEFINED CMAKE_INSTALL_PREFIX)
STRING(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
IF(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  IF(BUILD_TYPE)
    STRING(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  ELSE(BUILD_TYPE)
    SET(CMAKE_INSTALL_CONFIG_NAME "Release")
  ENDIF(BUILD_TYPE)
  MESSAGE(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
ENDIF(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)

# Set the component getting installed.
IF(NOT CMAKE_INSTALL_COMPONENT)
  IF(COMPONENT)
    MESSAGE(STATUS "Install component: \"${COMPONENT}\"")
    SET(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  ELSE(COMPONENT)
    SET(CMAKE_INSTALL_COMPONENT)
  ENDIF(COMPONENT)
ENDIF(NOT CMAKE_INSTALL_COMPONENT)

# Install shared libraries without execute permission?
IF(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  SET(CMAKE_INSTALL_SO_NO_EXE "0")
ENDIF(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)

IF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "dev")
  FILE(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/opencv" TYPE FILE FILES
    "/afs/inf.ed.ac.uk/user/s12/s1263586/sdp/Polygon2-2.0.6/argparse-1.2.1/opencv-2.4.8.1/include/opencv/cv.h"
    "/afs/inf.ed.ac.uk/user/s12/s1263586/sdp/Polygon2-2.0.6/argparse-1.2.1/opencv-2.4.8.1/include/opencv/cv.hpp"
    "/afs/inf.ed.ac.uk/user/s12/s1263586/sdp/Polygon2-2.0.6/argparse-1.2.1/opencv-2.4.8.1/include/opencv/cvaux.h"
    "/afs/inf.ed.ac.uk/user/s12/s1263586/sdp/Polygon2-2.0.6/argparse-1.2.1/opencv-2.4.8.1/include/opencv/cvaux.hpp"
    "/afs/inf.ed.ac.uk/user/s12/s1263586/sdp/Polygon2-2.0.6/argparse-1.2.1/opencv-2.4.8.1/include/opencv/cvwimage.h"
    "/afs/inf.ed.ac.uk/user/s12/s1263586/sdp/Polygon2-2.0.6/argparse-1.2.1/opencv-2.4.8.1/include/opencv/cxcore.h"
    "/afs/inf.ed.ac.uk/user/s12/s1263586/sdp/Polygon2-2.0.6/argparse-1.2.1/opencv-2.4.8.1/include/opencv/cxcore.hpp"
    "/afs/inf.ed.ac.uk/user/s12/s1263586/sdp/Polygon2-2.0.6/argparse-1.2.1/opencv-2.4.8.1/include/opencv/cxeigen.hpp"
    "/afs/inf.ed.ac.uk/user/s12/s1263586/sdp/Polygon2-2.0.6/argparse-1.2.1/opencv-2.4.8.1/include/opencv/cxmisc.h"
    "/afs/inf.ed.ac.uk/user/s12/s1263586/sdp/Polygon2-2.0.6/argparse-1.2.1/opencv-2.4.8.1/include/opencv/highgui.h"
    "/afs/inf.ed.ac.uk/user/s12/s1263586/sdp/Polygon2-2.0.6/argparse-1.2.1/opencv-2.4.8.1/include/opencv/ml.h"
    )
ENDIF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "dev")

IF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "dev")
  FILE(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/opencv2" TYPE FILE FILES "/afs/inf.ed.ac.uk/user/s12/s1263586/sdp/Polygon2-2.0.6/argparse-1.2.1/opencv-2.4.8.1/include/opencv2/opencv.hpp")
ENDIF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "dev")


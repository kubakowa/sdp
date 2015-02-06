# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 2.8

#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canoncical targets will work.
.SUFFIXES:

# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list

# Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:
.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E remove -f

# The program to use to edit the cache.
CMAKE_EDIT_COMMAND = /usr/bin/ccmake

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /afs/inf.ed.ac.uk/user/s12/s1263586/sdp/Polygon2-2.0.6/argparse-1.2.1/opencv-2.4.8.1

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /afs/inf.ed.ac.uk/user/s12/s1263586/sdp/Polygon2-2.0.6/argparse-1.2.1/opencv-2.4.8.1/build

# Utility rule file for pch_Generate_opencv_stitching.

modules/stitching/CMakeFiles/pch_Generate_opencv_stitching: modules/stitching/precomp.hpp.gch/opencv_stitching_Release.gch

modules/stitching/precomp.hpp.gch/opencv_stitching_Release.gch: ../modules/stitching/src/precomp.hpp
modules/stitching/precomp.hpp.gch/opencv_stitching_Release.gch: modules/stitching/precomp.hpp
modules/stitching/precomp.hpp.gch/opencv_stitching_Release.gch: lib/libopencv_stitching_pch_dephelp.a
	$(CMAKE_COMMAND) -E cmake_progress_report /afs/inf.ed.ac.uk/user/s12/s1263586/sdp/Polygon2-2.0.6/argparse-1.2.1/opencv-2.4.8.1/build/CMakeFiles $(CMAKE_PROGRESS_1)
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --blue --bold "Generating precomp.hpp.gch/opencv_stitching_Release.gch"
	cd /afs/inf.ed.ac.uk/user/s12/s1263586/sdp/Polygon2-2.0.6/argparse-1.2.1/opencv-2.4.8.1/build/modules/stitching && /usr/bin/cmake -E make_directory /afs/inf.ed.ac.uk/user/s12/s1263586/sdp/Polygon2-2.0.6/argparse-1.2.1/opencv-2.4.8.1/build/modules/stitching/precomp.hpp.gch
	cd /afs/inf.ed.ac.uk/user/s12/s1263586/sdp/Polygon2-2.0.6/argparse-1.2.1/opencv-2.4.8.1/build/modules/stitching && /usr/bin/c++ -O3 -DNDEBUG -DNDEBUG -fPIC -I"/afs/inf.ed.ac.uk/user/s12/s1263586/sdp/Polygon2-2.0.6/argparse-1.2.1/opencv-2.4.8.1/modules/nonfree/include" -I"/afs/inf.ed.ac.uk/user/s12/s1263586/sdp/Polygon2-2.0.6/argparse-1.2.1/opencv-2.4.8.1/modules/ocl/include" -I"/afs/inf.ed.ac.uk/user/s12/s1263586/sdp/Polygon2-2.0.6/argparse-1.2.1/opencv-2.4.8.1/modules/gpu/include" -I"/afs/inf.ed.ac.uk/user/s12/s1263586/sdp/Polygon2-2.0.6/argparse-1.2.1/opencv-2.4.8.1/modules/photo/include" -I"/afs/inf.ed.ac.uk/user/s12/s1263586/sdp/Polygon2-2.0.6/argparse-1.2.1/opencv-2.4.8.1/modules/objdetect/include" -I"/afs/inf.ed.ac.uk/user/s12/s1263586/sdp/Polygon2-2.0.6/argparse-1.2.1/opencv-2.4.8.1/modules/legacy/include" -I"/afs/inf.ed.ac.uk/user/s12/s1263586/sdp/Polygon2-2.0.6/argparse-1.2.1/opencv-2.4.8.1/modules/video/include" -I"/afs/inf.ed.ac.uk/user/s12/s1263586/sdp/Polygon2-2.0.6/argparse-1.2.1/opencv-2.4.8.1/modules/ml/include" -I"/afs/inf.ed.ac.uk/user/s12/s1263586/sdp/Polygon2-2.0.6/argparse-1.2.1/opencv-2.4.8.1/modules/calib3d/include" -I"/afs/inf.ed.ac.uk/user/s12/s1263586/sdp/Polygon2-2.0.6/argparse-1.2.1/opencv-2.4.8.1/modules/features2d/include" -I"/afs/inf.ed.ac.uk/user/s12/s1263586/sdp/Polygon2-2.0.6/argparse-1.2.1/opencv-2.4.8.1/modules/highgui/include" -I"/afs/inf.ed.ac.uk/user/s12/s1263586/sdp/Polygon2-2.0.6/argparse-1.2.1/opencv-2.4.8.1/modules/imgproc/include" -I"/afs/inf.ed.ac.uk/user/s12/s1263586/sdp/Polygon2-2.0.6/argparse-1.2.1/opencv-2.4.8.1/modules/flann/include" -I"/afs/inf.ed.ac.uk/user/s12/s1263586/sdp/Polygon2-2.0.6/argparse-1.2.1/opencv-2.4.8.1/modules/core/include" -isystem"/afs/inf.ed.ac.uk/user/s12/s1263586/sdp/Polygon2-2.0.6/argparse-1.2.1/opencv-2.4.8.1/build/modules/stitching" -I"/afs/inf.ed.ac.uk/user/s12/s1263586/sdp/Polygon2-2.0.6/argparse-1.2.1/opencv-2.4.8.1/modules/stitching/src" -I"/afs/inf.ed.ac.uk/user/s12/s1263586/sdp/Polygon2-2.0.6/argparse-1.2.1/opencv-2.4.8.1/modules/stitching/include" -isystem"/afs/inf.ed.ac.uk/user/s12/s1263586/sdp/Polygon2-2.0.6/argparse-1.2.1/opencv-2.4.8.1/build" -isystem"/usr/include/eigen3" -fsigned-char -W -Wall -Werror=return-type -Werror=address -Werror=sequence-point -Wformat -Werror=format-security -Wmissing-declarations -Wundef -Winit-self -Wpointer-arith -Wshadow -Wsign-promo -fdiagnostics-show-option -Wno-long-long -pthread -fomit-frame-pointer -msse -msse2 -msse3 -ffunction-sections -DCVAPI_EXPORTS -x c++-header -o /afs/inf.ed.ac.uk/user/s12/s1263586/sdp/Polygon2-2.0.6/argparse-1.2.1/opencv-2.4.8.1/build/modules/stitching/precomp.hpp.gch/opencv_stitching_Release.gch /afs/inf.ed.ac.uk/user/s12/s1263586/sdp/Polygon2-2.0.6/argparse-1.2.1/opencv-2.4.8.1/build/modules/stitching/precomp.hpp

modules/stitching/precomp.hpp: ../modules/stitching/src/precomp.hpp
	$(CMAKE_COMMAND) -E cmake_progress_report /afs/inf.ed.ac.uk/user/s12/s1263586/sdp/Polygon2-2.0.6/argparse-1.2.1/opencv-2.4.8.1/build/CMakeFiles $(CMAKE_PROGRESS_2)
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --blue --bold "Generating precomp.hpp"
	cd /afs/inf.ed.ac.uk/user/s12/s1263586/sdp/Polygon2-2.0.6/argparse-1.2.1/opencv-2.4.8.1/build/modules/stitching && /usr/bin/cmake -E copy /afs/inf.ed.ac.uk/user/s12/s1263586/sdp/Polygon2-2.0.6/argparse-1.2.1/opencv-2.4.8.1/modules/stitching/src/precomp.hpp /afs/inf.ed.ac.uk/user/s12/s1263586/sdp/Polygon2-2.0.6/argparse-1.2.1/opencv-2.4.8.1/build/modules/stitching/precomp.hpp

pch_Generate_opencv_stitching: modules/stitching/CMakeFiles/pch_Generate_opencv_stitching
pch_Generate_opencv_stitching: modules/stitching/precomp.hpp.gch/opencv_stitching_Release.gch
pch_Generate_opencv_stitching: modules/stitching/precomp.hpp
pch_Generate_opencv_stitching: modules/stitching/CMakeFiles/pch_Generate_opencv_stitching.dir/build.make
.PHONY : pch_Generate_opencv_stitching

# Rule to build all files generated by this target.
modules/stitching/CMakeFiles/pch_Generate_opencv_stitching.dir/build: pch_Generate_opencv_stitching
.PHONY : modules/stitching/CMakeFiles/pch_Generate_opencv_stitching.dir/build

modules/stitching/CMakeFiles/pch_Generate_opencv_stitching.dir/clean:
	cd /afs/inf.ed.ac.uk/user/s12/s1263586/sdp/Polygon2-2.0.6/argparse-1.2.1/opencv-2.4.8.1/build/modules/stitching && $(CMAKE_COMMAND) -P CMakeFiles/pch_Generate_opencv_stitching.dir/cmake_clean.cmake
.PHONY : modules/stitching/CMakeFiles/pch_Generate_opencv_stitching.dir/clean

modules/stitching/CMakeFiles/pch_Generate_opencv_stitching.dir/depend:
	cd /afs/inf.ed.ac.uk/user/s12/s1263586/sdp/Polygon2-2.0.6/argparse-1.2.1/opencv-2.4.8.1/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /afs/inf.ed.ac.uk/user/s12/s1263586/sdp/Polygon2-2.0.6/argparse-1.2.1/opencv-2.4.8.1 /afs/inf.ed.ac.uk/user/s12/s1263586/sdp/Polygon2-2.0.6/argparse-1.2.1/opencv-2.4.8.1/modules/stitching /afs/inf.ed.ac.uk/user/s12/s1263586/sdp/Polygon2-2.0.6/argparse-1.2.1/opencv-2.4.8.1/build /afs/inf.ed.ac.uk/user/s12/s1263586/sdp/Polygon2-2.0.6/argparse-1.2.1/opencv-2.4.8.1/build/modules/stitching /afs/inf.ed.ac.uk/user/s12/s1263586/sdp/Polygon2-2.0.6/argparse-1.2.1/opencv-2.4.8.1/build/modules/stitching/CMakeFiles/pch_Generate_opencv_stitching.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : modules/stitching/CMakeFiles/pch_Generate_opencv_stitching.dir/depend


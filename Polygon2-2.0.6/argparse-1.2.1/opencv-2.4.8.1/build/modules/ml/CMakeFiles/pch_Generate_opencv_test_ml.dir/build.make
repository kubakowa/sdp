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

# Utility rule file for pch_Generate_opencv_test_ml.

modules/ml/CMakeFiles/pch_Generate_opencv_test_ml: modules/ml/test_precomp.hpp.gch/opencv_test_ml_Release.gch

modules/ml/test_precomp.hpp.gch/opencv_test_ml_Release.gch: ../modules/ml/test/test_precomp.hpp
modules/ml/test_precomp.hpp.gch/opencv_test_ml_Release.gch: modules/ml/test_precomp.hpp
modules/ml/test_precomp.hpp.gch/opencv_test_ml_Release.gch: lib/libopencv_test_ml_pch_dephelp.a
	$(CMAKE_COMMAND) -E cmake_progress_report /afs/inf.ed.ac.uk/user/s12/s1263586/sdp/Polygon2-2.0.6/argparse-1.2.1/opencv-2.4.8.1/build/CMakeFiles $(CMAKE_PROGRESS_1)
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --blue --bold "Generating test_precomp.hpp.gch/opencv_test_ml_Release.gch"
	cd /afs/inf.ed.ac.uk/user/s12/s1263586/sdp/Polygon2-2.0.6/argparse-1.2.1/opencv-2.4.8.1/build/modules/ml && /usr/bin/cmake -E make_directory /afs/inf.ed.ac.uk/user/s12/s1263586/sdp/Polygon2-2.0.6/argparse-1.2.1/opencv-2.4.8.1/build/modules/ml/test_precomp.hpp.gch
	cd /afs/inf.ed.ac.uk/user/s12/s1263586/sdp/Polygon2-2.0.6/argparse-1.2.1/opencv-2.4.8.1/build/modules/ml && /usr/bin/c++ -O3 -DNDEBUG -DNDEBUG -I"/afs/inf.ed.ac.uk/user/s12/s1263586/sdp/Polygon2-2.0.6/argparse-1.2.1/opencv-2.4.8.1/modules/ml/test" -I"/afs/inf.ed.ac.uk/user/s12/s1263586/sdp/Polygon2-2.0.6/argparse-1.2.1/opencv-2.4.8.1/modules/features2d/include" -I"/afs/inf.ed.ac.uk/user/s12/s1263586/sdp/Polygon2-2.0.6/argparse-1.2.1/opencv-2.4.8.1/modules/highgui/include" -I"/afs/inf.ed.ac.uk/user/s12/s1263586/sdp/Polygon2-2.0.6/argparse-1.2.1/opencv-2.4.8.1/modules/imgproc/include" -I"/afs/inf.ed.ac.uk/user/s12/s1263586/sdp/Polygon2-2.0.6/argparse-1.2.1/opencv-2.4.8.1/modules/flann/include" -I"/afs/inf.ed.ac.uk/user/s12/s1263586/sdp/Polygon2-2.0.6/argparse-1.2.1/opencv-2.4.8.1/modules/core/include" -I"/afs/inf.ed.ac.uk/user/s12/s1263586/sdp/Polygon2-2.0.6/argparse-1.2.1/opencv-2.4.8.1/modules/ts/include" -I"/afs/inf.ed.ac.uk/user/s12/s1263586/sdp/Polygon2-2.0.6/argparse-1.2.1/opencv-2.4.8.1/modules/ml/include" -isystem"/afs/inf.ed.ac.uk/user/s12/s1263586/sdp/Polygon2-2.0.6/argparse-1.2.1/opencv-2.4.8.1/build/modules/ml" -I"/afs/inf.ed.ac.uk/user/s12/s1263586/sdp/Polygon2-2.0.6/argparse-1.2.1/opencv-2.4.8.1/modules/ml/src" -isystem"/afs/inf.ed.ac.uk/user/s12/s1263586/sdp/Polygon2-2.0.6/argparse-1.2.1/opencv-2.4.8.1/build" -isystem"/usr/include/eigen3" -fsigned-char -W -Wall -Werror=return-type -Werror=address -Werror=sequence-point -Wformat -Werror=format-security -Wmissing-declarations -Wundef -Winit-self -Wpointer-arith -Wshadow -Wsign-promo -fdiagnostics-show-option -Wno-long-long -pthread -fomit-frame-pointer -msse -msse2 -msse3 -ffunction-sections -x c++-header -o /afs/inf.ed.ac.uk/user/s12/s1263586/sdp/Polygon2-2.0.6/argparse-1.2.1/opencv-2.4.8.1/build/modules/ml/test_precomp.hpp.gch/opencv_test_ml_Release.gch /afs/inf.ed.ac.uk/user/s12/s1263586/sdp/Polygon2-2.0.6/argparse-1.2.1/opencv-2.4.8.1/build/modules/ml/test_precomp.hpp

modules/ml/test_precomp.hpp: ../modules/ml/test/test_precomp.hpp
	$(CMAKE_COMMAND) -E cmake_progress_report /afs/inf.ed.ac.uk/user/s12/s1263586/sdp/Polygon2-2.0.6/argparse-1.2.1/opencv-2.4.8.1/build/CMakeFiles $(CMAKE_PROGRESS_2)
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --blue --bold "Generating test_precomp.hpp"
	cd /afs/inf.ed.ac.uk/user/s12/s1263586/sdp/Polygon2-2.0.6/argparse-1.2.1/opencv-2.4.8.1/build/modules/ml && /usr/bin/cmake -E copy /afs/inf.ed.ac.uk/user/s12/s1263586/sdp/Polygon2-2.0.6/argparse-1.2.1/opencv-2.4.8.1/modules/ml/test/test_precomp.hpp /afs/inf.ed.ac.uk/user/s12/s1263586/sdp/Polygon2-2.0.6/argparse-1.2.1/opencv-2.4.8.1/build/modules/ml/test_precomp.hpp

pch_Generate_opencv_test_ml: modules/ml/CMakeFiles/pch_Generate_opencv_test_ml
pch_Generate_opencv_test_ml: modules/ml/test_precomp.hpp.gch/opencv_test_ml_Release.gch
pch_Generate_opencv_test_ml: modules/ml/test_precomp.hpp
pch_Generate_opencv_test_ml: modules/ml/CMakeFiles/pch_Generate_opencv_test_ml.dir/build.make
.PHONY : pch_Generate_opencv_test_ml

# Rule to build all files generated by this target.
modules/ml/CMakeFiles/pch_Generate_opencv_test_ml.dir/build: pch_Generate_opencv_test_ml
.PHONY : modules/ml/CMakeFiles/pch_Generate_opencv_test_ml.dir/build

modules/ml/CMakeFiles/pch_Generate_opencv_test_ml.dir/clean:
	cd /afs/inf.ed.ac.uk/user/s12/s1263586/sdp/Polygon2-2.0.6/argparse-1.2.1/opencv-2.4.8.1/build/modules/ml && $(CMAKE_COMMAND) -P CMakeFiles/pch_Generate_opencv_test_ml.dir/cmake_clean.cmake
.PHONY : modules/ml/CMakeFiles/pch_Generate_opencv_test_ml.dir/clean

modules/ml/CMakeFiles/pch_Generate_opencv_test_ml.dir/depend:
	cd /afs/inf.ed.ac.uk/user/s12/s1263586/sdp/Polygon2-2.0.6/argparse-1.2.1/opencv-2.4.8.1/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /afs/inf.ed.ac.uk/user/s12/s1263586/sdp/Polygon2-2.0.6/argparse-1.2.1/opencv-2.4.8.1 /afs/inf.ed.ac.uk/user/s12/s1263586/sdp/Polygon2-2.0.6/argparse-1.2.1/opencv-2.4.8.1/modules/ml /afs/inf.ed.ac.uk/user/s12/s1263586/sdp/Polygon2-2.0.6/argparse-1.2.1/opencv-2.4.8.1/build /afs/inf.ed.ac.uk/user/s12/s1263586/sdp/Polygon2-2.0.6/argparse-1.2.1/opencv-2.4.8.1/build/modules/ml /afs/inf.ed.ac.uk/user/s12/s1263586/sdp/Polygon2-2.0.6/argparse-1.2.1/opencv-2.4.8.1/build/modules/ml/CMakeFiles/pch_Generate_opencv_test_ml.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : modules/ml/CMakeFiles/pch_Generate_opencv_test_ml.dir/depend


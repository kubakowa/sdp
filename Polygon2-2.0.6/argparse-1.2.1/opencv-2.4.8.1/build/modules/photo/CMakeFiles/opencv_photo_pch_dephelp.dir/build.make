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

# Include any dependencies generated for this target.
include modules/photo/CMakeFiles/opencv_photo_pch_dephelp.dir/depend.make

# Include the progress variables for this target.
include modules/photo/CMakeFiles/opencv_photo_pch_dephelp.dir/progress.make

# Include the compile flags for this target's objects.
include modules/photo/CMakeFiles/opencv_photo_pch_dephelp.dir/flags.make

modules/photo/CMakeFiles/opencv_photo_pch_dephelp.dir/opencv_photo_pch_dephelp.cxx.o: modules/photo/CMakeFiles/opencv_photo_pch_dephelp.dir/flags.make
modules/photo/CMakeFiles/opencv_photo_pch_dephelp.dir/opencv_photo_pch_dephelp.cxx.o: modules/photo/opencv_photo_pch_dephelp.cxx
	$(CMAKE_COMMAND) -E cmake_progress_report /afs/inf.ed.ac.uk/user/s12/s1263586/sdp/Polygon2-2.0.6/argparse-1.2.1/opencv-2.4.8.1/build/CMakeFiles $(CMAKE_PROGRESS_1)
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Building CXX object modules/photo/CMakeFiles/opencv_photo_pch_dephelp.dir/opencv_photo_pch_dephelp.cxx.o"
	cd /afs/inf.ed.ac.uk/user/s12/s1263586/sdp/Polygon2-2.0.6/argparse-1.2.1/opencv-2.4.8.1/build/modules/photo && /usr/bin/c++   $(CXX_DEFINES) $(CXX_FLAGS) -o CMakeFiles/opencv_photo_pch_dephelp.dir/opencv_photo_pch_dephelp.cxx.o -c /afs/inf.ed.ac.uk/user/s12/s1263586/sdp/Polygon2-2.0.6/argparse-1.2.1/opencv-2.4.8.1/build/modules/photo/opencv_photo_pch_dephelp.cxx

modules/photo/CMakeFiles/opencv_photo_pch_dephelp.dir/opencv_photo_pch_dephelp.cxx.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/opencv_photo_pch_dephelp.dir/opencv_photo_pch_dephelp.cxx.i"
	cd /afs/inf.ed.ac.uk/user/s12/s1263586/sdp/Polygon2-2.0.6/argparse-1.2.1/opencv-2.4.8.1/build/modules/photo && /usr/bin/c++  $(CXX_DEFINES) $(CXX_FLAGS) -E /afs/inf.ed.ac.uk/user/s12/s1263586/sdp/Polygon2-2.0.6/argparse-1.2.1/opencv-2.4.8.1/build/modules/photo/opencv_photo_pch_dephelp.cxx > CMakeFiles/opencv_photo_pch_dephelp.dir/opencv_photo_pch_dephelp.cxx.i

modules/photo/CMakeFiles/opencv_photo_pch_dephelp.dir/opencv_photo_pch_dephelp.cxx.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/opencv_photo_pch_dephelp.dir/opencv_photo_pch_dephelp.cxx.s"
	cd /afs/inf.ed.ac.uk/user/s12/s1263586/sdp/Polygon2-2.0.6/argparse-1.2.1/opencv-2.4.8.1/build/modules/photo && /usr/bin/c++  $(CXX_DEFINES) $(CXX_FLAGS) -S /afs/inf.ed.ac.uk/user/s12/s1263586/sdp/Polygon2-2.0.6/argparse-1.2.1/opencv-2.4.8.1/build/modules/photo/opencv_photo_pch_dephelp.cxx -o CMakeFiles/opencv_photo_pch_dephelp.dir/opencv_photo_pch_dephelp.cxx.s

modules/photo/CMakeFiles/opencv_photo_pch_dephelp.dir/opencv_photo_pch_dephelp.cxx.o.requires:
.PHONY : modules/photo/CMakeFiles/opencv_photo_pch_dephelp.dir/opencv_photo_pch_dephelp.cxx.o.requires

modules/photo/CMakeFiles/opencv_photo_pch_dephelp.dir/opencv_photo_pch_dephelp.cxx.o.provides: modules/photo/CMakeFiles/opencv_photo_pch_dephelp.dir/opencv_photo_pch_dephelp.cxx.o.requires
	$(MAKE) -f modules/photo/CMakeFiles/opencv_photo_pch_dephelp.dir/build.make modules/photo/CMakeFiles/opencv_photo_pch_dephelp.dir/opencv_photo_pch_dephelp.cxx.o.provides.build
.PHONY : modules/photo/CMakeFiles/opencv_photo_pch_dephelp.dir/opencv_photo_pch_dephelp.cxx.o.provides

modules/photo/CMakeFiles/opencv_photo_pch_dephelp.dir/opencv_photo_pch_dephelp.cxx.o.provides.build: modules/photo/CMakeFiles/opencv_photo_pch_dephelp.dir/opencv_photo_pch_dephelp.cxx.o

modules/photo/opencv_photo_pch_dephelp.cxx: ../modules/photo/src/precomp.hpp
	$(CMAKE_COMMAND) -E cmake_progress_report /afs/inf.ed.ac.uk/user/s12/s1263586/sdp/Polygon2-2.0.6/argparse-1.2.1/opencv-2.4.8.1/build/CMakeFiles $(CMAKE_PROGRESS_2)
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --blue --bold "Generating opencv_photo_pch_dephelp.cxx"
	cd /afs/inf.ed.ac.uk/user/s12/s1263586/sdp/Polygon2-2.0.6/argparse-1.2.1/opencv-2.4.8.1/build/modules/photo && /usr/bin/cmake -E echo \#include\ \"/afs/inf.ed.ac.uk/user/s12/s1263586/sdp/Polygon2-2.0.6/argparse-1.2.1/opencv-2.4.8.1/modules/photo/src/precomp.hpp\" > /afs/inf.ed.ac.uk/user/s12/s1263586/sdp/Polygon2-2.0.6/argparse-1.2.1/opencv-2.4.8.1/build/modules/photo/opencv_photo_pch_dephelp.cxx
	cd /afs/inf.ed.ac.uk/user/s12/s1263586/sdp/Polygon2-2.0.6/argparse-1.2.1/opencv-2.4.8.1/build/modules/photo && /usr/bin/cmake -E echo int\ testfunction\(\)\; >> /afs/inf.ed.ac.uk/user/s12/s1263586/sdp/Polygon2-2.0.6/argparse-1.2.1/opencv-2.4.8.1/build/modules/photo/opencv_photo_pch_dephelp.cxx
	cd /afs/inf.ed.ac.uk/user/s12/s1263586/sdp/Polygon2-2.0.6/argparse-1.2.1/opencv-2.4.8.1/build/modules/photo && /usr/bin/cmake -E echo int\ testfunction\(\) >> /afs/inf.ed.ac.uk/user/s12/s1263586/sdp/Polygon2-2.0.6/argparse-1.2.1/opencv-2.4.8.1/build/modules/photo/opencv_photo_pch_dephelp.cxx
	cd /afs/inf.ed.ac.uk/user/s12/s1263586/sdp/Polygon2-2.0.6/argparse-1.2.1/opencv-2.4.8.1/build/modules/photo && /usr/bin/cmake -E echo { >> /afs/inf.ed.ac.uk/user/s12/s1263586/sdp/Polygon2-2.0.6/argparse-1.2.1/opencv-2.4.8.1/build/modules/photo/opencv_photo_pch_dephelp.cxx
	cd /afs/inf.ed.ac.uk/user/s12/s1263586/sdp/Polygon2-2.0.6/argparse-1.2.1/opencv-2.4.8.1/build/modules/photo && /usr/bin/cmake -E echo \ \ \ \ \return\ 0\; >> /afs/inf.ed.ac.uk/user/s12/s1263586/sdp/Polygon2-2.0.6/argparse-1.2.1/opencv-2.4.8.1/build/modules/photo/opencv_photo_pch_dephelp.cxx
	cd /afs/inf.ed.ac.uk/user/s12/s1263586/sdp/Polygon2-2.0.6/argparse-1.2.1/opencv-2.4.8.1/build/modules/photo && /usr/bin/cmake -E echo } >> /afs/inf.ed.ac.uk/user/s12/s1263586/sdp/Polygon2-2.0.6/argparse-1.2.1/opencv-2.4.8.1/build/modules/photo/opencv_photo_pch_dephelp.cxx

# Object files for target opencv_photo_pch_dephelp
opencv_photo_pch_dephelp_OBJECTS = \
"CMakeFiles/opencv_photo_pch_dephelp.dir/opencv_photo_pch_dephelp.cxx.o"

# External object files for target opencv_photo_pch_dephelp
opencv_photo_pch_dephelp_EXTERNAL_OBJECTS =

lib/libopencv_photo_pch_dephelp.a: modules/photo/CMakeFiles/opencv_photo_pch_dephelp.dir/opencv_photo_pch_dephelp.cxx.o
lib/libopencv_photo_pch_dephelp.a: modules/photo/CMakeFiles/opencv_photo_pch_dephelp.dir/build.make
lib/libopencv_photo_pch_dephelp.a: modules/photo/CMakeFiles/opencv_photo_pch_dephelp.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --red --bold "Linking CXX static library ../../lib/libopencv_photo_pch_dephelp.a"
	cd /afs/inf.ed.ac.uk/user/s12/s1263586/sdp/Polygon2-2.0.6/argparse-1.2.1/opencv-2.4.8.1/build/modules/photo && $(CMAKE_COMMAND) -P CMakeFiles/opencv_photo_pch_dephelp.dir/cmake_clean_target.cmake
	cd /afs/inf.ed.ac.uk/user/s12/s1263586/sdp/Polygon2-2.0.6/argparse-1.2.1/opencv-2.4.8.1/build/modules/photo && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/opencv_photo_pch_dephelp.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
modules/photo/CMakeFiles/opencv_photo_pch_dephelp.dir/build: lib/libopencv_photo_pch_dephelp.a
.PHONY : modules/photo/CMakeFiles/opencv_photo_pch_dephelp.dir/build

modules/photo/CMakeFiles/opencv_photo_pch_dephelp.dir/requires: modules/photo/CMakeFiles/opencv_photo_pch_dephelp.dir/opencv_photo_pch_dephelp.cxx.o.requires
.PHONY : modules/photo/CMakeFiles/opencv_photo_pch_dephelp.dir/requires

modules/photo/CMakeFiles/opencv_photo_pch_dephelp.dir/clean:
	cd /afs/inf.ed.ac.uk/user/s12/s1263586/sdp/Polygon2-2.0.6/argparse-1.2.1/opencv-2.4.8.1/build/modules/photo && $(CMAKE_COMMAND) -P CMakeFiles/opencv_photo_pch_dephelp.dir/cmake_clean.cmake
.PHONY : modules/photo/CMakeFiles/opencv_photo_pch_dephelp.dir/clean

modules/photo/CMakeFiles/opencv_photo_pch_dephelp.dir/depend: modules/photo/opencv_photo_pch_dephelp.cxx
	cd /afs/inf.ed.ac.uk/user/s12/s1263586/sdp/Polygon2-2.0.6/argparse-1.2.1/opencv-2.4.8.1/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /afs/inf.ed.ac.uk/user/s12/s1263586/sdp/Polygon2-2.0.6/argparse-1.2.1/opencv-2.4.8.1 /afs/inf.ed.ac.uk/user/s12/s1263586/sdp/Polygon2-2.0.6/argparse-1.2.1/opencv-2.4.8.1/modules/photo /afs/inf.ed.ac.uk/user/s12/s1263586/sdp/Polygon2-2.0.6/argparse-1.2.1/opencv-2.4.8.1/build /afs/inf.ed.ac.uk/user/s12/s1263586/sdp/Polygon2-2.0.6/argparse-1.2.1/opencv-2.4.8.1/build/modules/photo /afs/inf.ed.ac.uk/user/s12/s1263586/sdp/Polygon2-2.0.6/argparse-1.2.1/opencv-2.4.8.1/build/modules/photo/CMakeFiles/opencv_photo_pch_dephelp.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : modules/photo/CMakeFiles/opencv_photo_pch_dephelp.dir/depend


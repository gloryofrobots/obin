# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 2.8

#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
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

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/gloryofrobots/develop/languages/obin/obin/src

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/gloryofrobots/develop/languages/obin/obin

# Include any dependencies generated for this target.
include test/CMakeFiles/obin-tests.dir/depend.make

# Include the progress variables for this target.
include test/CMakeFiles/obin-tests.dir/progress.make

# Include the compile flags for this target's objects.
include test/CMakeFiles/obin-tests.dir/flags.make

test/CMakeFiles/obin-tests.dir/main.c.o: test/CMakeFiles/obin-tests.dir/flags.make
test/CMakeFiles/obin-tests.dir/main.c.o: src/test/main.c
	$(CMAKE_COMMAND) -E cmake_progress_report /home/gloryofrobots/develop/languages/obin/obin/CMakeFiles $(CMAKE_PROGRESS_1)
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Building C object test/CMakeFiles/obin-tests.dir/main.c.o"
	cd /home/gloryofrobots/develop/languages/obin/obin/test && /usr/bin/cc  $(C_DEFINES) $(C_FLAGS) -o CMakeFiles/obin-tests.dir/main.c.o   -c /home/gloryofrobots/develop/languages/obin/obin/src/test/main.c

test/CMakeFiles/obin-tests.dir/main.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/obin-tests.dir/main.c.i"
	cd /home/gloryofrobots/develop/languages/obin/obin/test && /usr/bin/cc  $(C_DEFINES) $(C_FLAGS) -E /home/gloryofrobots/develop/languages/obin/obin/src/test/main.c > CMakeFiles/obin-tests.dir/main.c.i

test/CMakeFiles/obin-tests.dir/main.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/obin-tests.dir/main.c.s"
	cd /home/gloryofrobots/develop/languages/obin/obin/test && /usr/bin/cc  $(C_DEFINES) $(C_FLAGS) -S /home/gloryofrobots/develop/languages/obin/obin/src/test/main.c -o CMakeFiles/obin-tests.dir/main.c.s

test/CMakeFiles/obin-tests.dir/main.c.o.requires:
.PHONY : test/CMakeFiles/obin-tests.dir/main.c.o.requires

test/CMakeFiles/obin-tests.dir/main.c.o.provides: test/CMakeFiles/obin-tests.dir/main.c.o.requires
	$(MAKE) -f test/CMakeFiles/obin-tests.dir/build.make test/CMakeFiles/obin-tests.dir/main.c.o.provides.build
.PHONY : test/CMakeFiles/obin-tests.dir/main.c.o.provides

test/CMakeFiles/obin-tests.dir/main.c.o.provides.build: test/CMakeFiles/obin-tests.dir/main.c.o

# Object files for target obin-tests
obin__tests_OBJECTS = \
"CMakeFiles/obin-tests.dir/main.c.o"

# External object files for target obin-tests
obin__tests_EXTERNAL_OBJECTS =

test/obin-tests: test/CMakeFiles/obin-tests.dir/main.c.o
test/obin-tests: test/CMakeFiles/obin-tests.dir/build.make
test/obin-tests: libobin.a
test/obin-tests: /usr/lib/libcunit.so
test/obin-tests: test/CMakeFiles/obin-tests.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --red --bold "Linking C executable obin-tests"
	cd /home/gloryofrobots/develop/languages/obin/obin/test && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/obin-tests.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
test/CMakeFiles/obin-tests.dir/build: test/obin-tests
.PHONY : test/CMakeFiles/obin-tests.dir/build

test/CMakeFiles/obin-tests.dir/requires: test/CMakeFiles/obin-tests.dir/main.c.o.requires
.PHONY : test/CMakeFiles/obin-tests.dir/requires

test/CMakeFiles/obin-tests.dir/clean:
	cd /home/gloryofrobots/develop/languages/obin/obin/test && $(CMAKE_COMMAND) -P CMakeFiles/obin-tests.dir/cmake_clean.cmake
.PHONY : test/CMakeFiles/obin-tests.dir/clean

test/CMakeFiles/obin-tests.dir/depend:
	cd /home/gloryofrobots/develop/languages/obin/obin && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/gloryofrobots/develop/languages/obin/obin/src /home/gloryofrobots/develop/languages/obin/obin/src/test /home/gloryofrobots/develop/languages/obin/obin /home/gloryofrobots/develop/languages/obin/obin/test /home/gloryofrobots/develop/languages/obin/obin/test/CMakeFiles/obin-tests.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : test/CMakeFiles/obin-tests.dir/depend


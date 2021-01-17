---
title: "Building a C++ project with Travis continuous integration (CI)"
date: 2021-01-17T18:00:20+01:00
image: /images/domino.jpg
imageQuality: "q65"
imageAnchor: "Center" # Smart, Center, TopLeft, Top, TopRight, Left, Right, BottomLeft, Bottom, BottomRight.
tags: ["C++", "CI"]
categories: "C++" 
summary: "I explain with an example that how a C++ project is automatically built by Travis CI with the push of a commit."
---

## Introduction

I explain with a simple example that how a C++ project is automatically built by [Travis CI](https://travis-ci.com/) with the push of a commit. The operating system (OS) is Ubuntu and the compiler is GCC.

## Why Travis

 Because it has detailed documentation and is free for open-source projects.

## Code 

The code is placed [here](https://GitHub.com/sorush-khajepor/CppExamples). Here, the main focus is on *Example001*.

## Build system (CMake)

Before configuring continuous integration (CI), ensure the project has a build system generator like **CMake** and it is successfully compiled and run on a local machine.

For this example (see the code), I use CMake. We have a *CMakeLists.txt* in the *Example001/Shape* as

```cmake
add_library(Shape Box.cpp)
```

and another in *Example001* folder to create the executable

```cmake
## Example001

cmake_minimum_required(VERSION 3.1.0)
project(example)
set (CMAKE_CXX_STANDARD 20)

# add the Shape library
add_subdirectory(Shape)

# add the executable
add_executable(Example Example.cpp)

target_link_libraries(Example PUBLIC Shape)
```

I compiled *Example001* on my machine with the below *build.sh* commands 

```bash
# build.sh
mkdir -p build
cd build
cmake ..
make
./Example
```

It was successful. Now we can go to the next step.

## Link Travis to GitHub

Login to the [Travis CI website](https://travis-ci.com/) with aid of your GitHub account. Click on your profile picture in Travis then *settings*. Find the desired project and activate continuous integration (CI) as shown below

{{< img "*travis*" "road sections" >}}



## YAML file

Travis builds a project if a new commit is pushed to the repo and it contains `.travis.yml` file. 

So I added the below YAML file to the root of the project:

```yml
language: cpp 
dist: focal
compiler: gcc
os: linux
sudo: true
env:
    - BUILD_TYPE=Debug

# default gcc for Ubuntu Focal is v9, upgraded to v10 here
# It increases build time by ~1 min
addons:
        apt:
              sources:
                  - sourceline: “ppa:ubuntu-toolchain-r/test”
              packages:
                  - gcc-10
                  - g++-10
install:
# /usr/bin/gcc points to an older compiler on Linux.
- if [ "$CXX" = "g++" ]; then export CXX="g++-10" CC="gcc-10"; fi
script: 
  - ./build.sh
```

The first line is to set C++ as the code language. 

The second line is the distribution of Ubuntu. **Focal** is Ubuntu 20.04 which comes with GCC v9.  You can choose *Bionic* 18.04, *Xenial* 16.04 and so on.

The OS is Linux.

`sudo` is true so we can install new packages.

`env` line shows how we can set an environment variable.

`addons` are the packages to be installed before compilation. Here, I added *GCC* v10. Note installing *GCC* took about 25 seconds but the example itself compiled in 2 seconds. If not necessary, stick to default packages that come with the distribution.

The last line *./build.sh* runs CMake commands. 


## Push a commit

Finally, go to your code, make a change, commit and push it to GitHub. Travis should automatically build it for you. You can see the live results in the focused project on the Travis website. 

{{< img "*travis2*" "road sections" >}}

## Build badge

Moreover, you can click on the build badge, shown in the previous picture, which gives a markdown code. It can be pasted in the *readme.md* of the GitHub repo to see the badge there too.

{{< img "*travis3*" "road sections" >}}


## References

[Travis docs](https://docs.travis-ci.com/user/languages/cpp/)


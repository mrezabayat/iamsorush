---
title: "pybind11: call OpenMP function in Python"
date: 2021-05-23T18:10:20+01:00
image: /images/rail.jpg
imageQuality: "q65"
imageAnchor: "bottom" # Smart, Center, TopLeft, Top, TopRight, Left, Right, BottomLeft, Bottom, BottomRight.
tags: ["C++", "Python"]
categories: "C++" 
summary: "I want to use pybind11 to compile an OpenMP parallel code and load and run it in Python. The code is in C++. "
---

## Goal

I want to use pybind11 to compile an OpenMP parallel code, then load and run it in Python. The code is written in *C++*. 

## System

I am using Ubuntu 21.04, *GCC* 10.3, CMake 3.20-rc2.

## Install pybind11

Open a terminal, download pybind11 first:

```sh
git clone https://github.com/pybind/pybind11.git
```

 Go into the downloaded directory and run

```bash
mkdir build
cd build
cmake ..
make check -j 4
```

These commands compile pybind11 and run its tests. You should see all the tests pass, otherwise, there is a problem with your system which needs to be fixed. 

## Set Headers

The compilers like *GCC* and *Clang* look into the environment variable `CPATH` for headers. We add the path of python and pybind11 headers to `CPATH`:

```bash
# Run in a terminal
export CPATH=/home/sorush/workspace/pybind11/include:/usr/include/python3.9/:$CPATH 
```
Change the pybind11 and Python `include` path to yours. If not sure where the Python is placed, run

```bash
sudo find / -iname 'Python.h'
```
The result of this command is where python headers are placed. If nothing found, you need to install `python3-dev`:

```bash
# Ubuntu terminal
sudo apt install python3-dev
```

You can add the export of `CPATH` to `~/.bashrc` file in Ubuntu, so whenever you open a new terminal `CPATH` is updated.

## Code

The C++ code with comments:

```c++
// example.cpp file
#include <pybind11/pybind11.h>
#include <omp.h> // OpenMP header
#include <unistd.h> // sleep() function

namespace py=pybind11;

// Sums the id of all threads
int sum_thread_ids() {
    int sum=0;
    #pragma omp parallel shared(sum)
    {
        sleep(3);
        #pragma omp critical
        sum += omp_get_thread_num();
    }
    return sum;
}

PYBIND11_MODULE(example, m) {
    m.def("get_max_threads", &omp_get_max_threads, "Returns max number of threads");
    m.def("set_num_threads", &omp_set_num_threads, "Set number of threads");
    m.def("sum_thread_ids", &sum_thread_ids, "Adds the id of threads");
}
```

Note that `omp_get_max_threads` and `omp_set_num_threads` are defined in OpenMP library.

## Compile

To compile the code, in a terminal run

```bash
c++ -O3 -Wall -std=c++11 -shared -fPIC example.cpp -o example$(python3-config --extension-suffix) -fopenmp
```

This produces a file like

```
example.cpython-39-x86_64-linux-gnu.so
```

## Python Path

To have the module accessible everywhere, we add the new module address to the Python path, run the below code in a terminal or add it to `~/.bashrc`:

```bash
export PYTHONPATH=/path/to/example/directory/:$PYTHONPATH
```

## Usage

Run Python in a terminal: 

```bash
python3
```
Then step by step run the below commands:

```python
import example
example.get_max_threads()
# My Python shows: 16

# Set number of threads =< max number of threads
example.set_num_threads(4)

# Call the function:
example.sum_thread_ids()
# After 3 seconds, shows: 6
```

`sum_thread_ids()` function put CPUs to sleep for 3 seconds. If you run a CPU intensive function, You can open another terminal and run `htop` to watch the activity of CPUs.

## GIL

Python Global Interpreter Lock (GIL) only allows one thread to run a Python script. I don't think it is a problem for the goal of this post: calling a C++ multi-thread function from Python. However, It can be problematic if a Python code is executed within a C++ multi-thread function.   



## References

[pybind11 GitHub](https://github.com/pybind/pybind11)
[pybind11 Docs](https://pybind11.readthedocs.io/en/latest/basics.html)



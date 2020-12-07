---
title: "Debug MPI program with Visual Studio Code"
date: 2020-12-04T18:10:20+01:00
image: /images/ladybird.jpg
imageQuality: "q65"
imageAnchor: "TopRight" # Smart, Center, TopLeft, Top, TopRight, Left, Right, BottomLeft, Bottom, BottomRight.
tags: ["MPI", "C++"]
categories: "Diverse" 
summary: "Debugging MPI program can be a nightmare. I explain how easily you can  debug a parallel MPI program with visual studio (VS) code."
---

## Introduction

Debugging an MPI program can be a nightmare. I explain how easily you can debug a parallel MPI program with visual studio (VS) code.

## Video

{{< youtube lTt02xuD51w >}}

## Superuser password

To get rid of Linux asking for Superuser password try below command

```bash
echo 0| sudo tee /proc/sys/kernel/yama/ptrace_scope
```
For more info, see [here](https://github.com/Microsoft/MIEngine/wiki/Troubleshoot-attaching-to-processes-using-GDB).

## Settings

VS Code creates folder *.vscode* which contains settings files:


**c_cpp_properties.json ↓**

```json
{
    "configurations": [
        {
            "name": "Linux",
            "includePath": [
                "${workspaceFolder}/**",
                "/usr/lib/x86_64-linux-gnu/openmpi/include"
            ],
            "defines": [],
            "compilerPath": "mpic++",
            "cStandard": "gnu17",
            "cppStandard": "gnu++14",
            "intelliSenseMode": "gcc-x64"
        }
    ],
    "version": 4
}
```

**launch.json ↓**

```json
{
   
    "version": "0.2.0",
    "configurations": [
        {
            "name": "g++ - Build and debug active file",
            "type": "cppdbg",
            "request": "attach",
            "processId": "${command:pickProcess}",
            "program": "${fileDirname}/${fileBasenameNoExtension}",
            "MIMode": "gdb",
            "setupCommands": [
                {
                    "description": "Enable pretty-printing for gdb",
                    "text": "-enable-pretty-printing",
                    "ignoreFailures": true
                }
            ],
            "preLaunchTask": "C/C++: g++ build active file",
            "miDebuggerPath": "/usr/bin/gdb"
        }
    ]
}
```

**tasks.json ↓**

```json
{
    "tasks": [
        {
            "type": "shell",
            "label": "C/C++: g++ build active file",
            "command": "mpic++",
            "args": [
                "-g",
                "${file}",
                "-o",
                "${fileDirname}/${fileBasenameNoExtension}"
            ],
            "options": {
                "cwd": "/usr/bin"
            },
            "problemMatcher": [
                "$gcc"
            ],
            "group": {
                "kind": "build",
                "isDefault": true
            },
            "detail": "Generated task by Debugger"
        }
    ],
    "version": "2.0.0"
}
```

## Code

The content of *hello.cpp* is:

```cpp
#include <mpi.h>
#include <unistd.h>

using namespace std;

int main(){

    {
        int i=0;
        while (0 == i)
            sleep(5);
    }

    MPI_Init(NULL, NULL);
    int rank,size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    char data = 'A';
    
    if (rank==0) {
        data = 'B';
        MPI_Send( &data , 1 , MPI_INT , 1 , 0 , MPI_COMM_WORLD);
    }
    else if (rank==1){
        MPI_Recv( &data , 1 , MPI_INT , 0 , 0 , MPI_COMM_WORLD , MPI_STATUS_IGNORE);
    }

return 0;

} 
```
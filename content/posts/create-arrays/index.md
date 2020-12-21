---
title: "Various ways to create arrays and vectors and their differences in C++"
date: 2020-12-08T18:10:20+01:00
image: /images/pingpong.jpg
imageQuality: "q65"
imageAnchor: "Center" # Smart, Center, TopLeft, Top, TopRight, Left, Right, BottomLeft, Bottom, BottomRight.
tags: ["C++"]
categories: "C++" 
summary: "Summary of this page used in cards, and also in SEO description of the page."
draft: true
---

## Introduction

## C array

A contiguous array can be created by `[]` operator. An array of 5 integers is defined as

```cpp
int a[5];
```
The size of an array needs to be known during compilation. Therefore, a constant number or constant expression can be used to create the array. Note constant expressions are evaluated at compile time.

```cpp
constexpr int GetSize(int n){
    return n*n;
}
int main(){
    int m[GetSize(5)]; // m is array of 25 elements
}

```

Multidimensional arrays are defined with multiple `[]` operators. A two dimenstion array with 3 rows and 2 columns is defined as
```cpp
int x[3][2];
``` 
This array is contiguous in the order that increments the last index:
```
Layout order in memory
x[0][0]
x[0][1]
x[1][0]
x[1][1]
x[2][0]
x[2][1]
```

So for the best performance, the array should be accessed firstly by its last index:
```cpp
for (auto i=0; i<3;i++)
    for (auto j=0; j<2; j++)
        do something with x[i][j]
```

If it is defined within a function, the memory is allocated on the stack which is on nowadays computers is in the order of 1MB. So, this definition should be used for small size arrays.

For memory management no action required by a coder, C++ automatically gets rid of the array when goes out of a scope.


## Pointer

A contiguous array can be created using a pointer on the heap with the keyword `new` and operator `[]`. An array of 5 integers on the heap:
```cpp
int* arr = new int[5];
```

The size of the array can be decided during runtime. 

If this array is defined within a function, the pointer itself, `arr`, is placed on stack but the array memory is allocated on the heap. 


Multidimensional arrays can be defined with pointer to pointers:

```cpp
int** arr2d = new int*[3]; // head of rows
for (auto i=0;i<3;j++)
    arr2d[i] = new int[2];// columns 
```
While columns of each row are contiguous on the memory. The rows are not guaranteed to be one after the other on the memory.

The array's memory needs to be managed by a coder. They can be deleted as:
```cpp
delete[] arr;

for (auto i=0;i<3;j++)
    delete[] arr2d[i]; // delete columns
delete[] arr2d; // delete head of rows
```

## Pointer but contiguous

Multidimensional arrays made with pointer-to-pointers type weren't completely contiguous. One trick to fix this is 

```cpp
int row=3, col=2;
int** arr2d = new int*[row]; // head of rows
arr2d[0] = new int[row*col]; // Allocates all elements
for (auto i=1;i<row;j++)
    arr2d[i] = arr2d[0][i*col];// columns 
```


## std::array

## std::vector
Creates an array of objects on the heap. The array is dynamic: objects can be added or removed during runtime. The memory of a vector is managed by C++, when it goes out of scope all the elements are automatically destructed. Note that if the elements are raw pointers, only raw pointers are removed but their target is untouched. 

## Boost::multiarray

## Custom array nD

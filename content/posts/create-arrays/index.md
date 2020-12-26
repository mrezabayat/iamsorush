---
title: "Various ways to create arrays and vectors and their differences in C++"
date: 2020-12-20T18:10:20+01:00
image: /images/berry.jpg
imageQuality: "q65"
imageAnchor: "Center" # Smart, Center, TopLeft, Top, TopRight, Left, Right, BottomLeft, Bottom, BottomRight.
tags: ["C++"]
categories: "C++" 
summary: "Different methods to create arrays in C++ are overviewed: c-style array, pointer array, std::vector, std::array, and Boost multiarray. How the memory is managed by each style and also their practical usage is discussed."
---

## Introduction

Different methods to create arrays in C++ are overviewed: c-style array, pointer array, std::vector, std::array, and Boost multiarray. How the memory is managed by each style and also their practical usage is discussed. 

Non-contiguous containers like list and deque are not studied here.

## C array

A contiguous array can be created by `[]` operator. An array of five integers is defined as

```cpp
int a[5];
```
The size of an array needs to be known during compilation. Therefore, a constant number or constant expression can be used to create the array.

```cpp
constexpr int GetSize(int n){
    return n*n;
}
int main(){
    int m[GetSize(5)]; // m is array of 25 elements
}
```

Multidimensional arrays are defined with multiple `[]` operators. A two-dimensional (2D) array with 3 rows and 2 columns is defined as

```cpp
int x[3][2];
``` 
This array is contiguous in the order that the last index increments:

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

If the array is defined within a function, the memory is allocated on the stack which is on nowadays computers in the order of 1 MB. So, this definition should be used for small size arrays.

For memory management, no action is required by a coder, C++ automatically gets rid of the array when goes out of scope.

There are assignment situations that a C-style array decays to a pointer type (T*) so it loses the type and size information, see [this stackoverflow discussion](https://stackoverflow.com/questions/1461432/what-is-array-to-pointer-decay). 

## Pointer

A contiguous array can be created using a pointer on the heap with the keyword `new` and operator `[]`. An array of 5 integers on the heap:

```cpp
int* arr = new int[5];
```

The size of the array can be decided during runtime. 

If this array is defined within a function, the pointer itself, `arr`, is placed on the stack but the array memory is allocated on the heap. 


Multidimensional arrays can be defined with pointer to pointers:

```cpp
int** arr2d = new int*[3]; // head of rows
for (auto i=0;i<3;j++)
    arr2d[i] = new int[2];// columns 
```
While columns of each row are contiguous on the memory. The rows are not guaranteed to be one after the other on the memory.

The array's memory needs to be managed by a coder. They can be deleted as:
```cpp
// 1D array
delete[] arr;

// 2D array
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

It is the C++11 adaptation of C-array. It is as fast as C-array, has the features of standard containers, and is not decayed to `T*`. The size of the array needs to be known at compilation. It will be allocated contiguously on the stack if defined within a function. The array's memory is managed by C++, it is destroyed automatically when it goes out of scope. 

```cpp
#include <iostream>
#include <array>
#include <algorithm>

int main(){
std::array<int, 3> x = {3,1,2};
std::cout<< x.size(); // 3
std::sort(x.begin(), x.end()); 
for (auto& item:x)
    std::cout<<item;   // 1 2 3
return 0;
}
```

A multidimensional array is defined by setting  the array's object type as an array. A 2D array is defined as

```cpp
#include <iostream>
#include <array>
using namespace std;

int main(){

typedef array<int,2> Row;
array<Row, 3> y { {{1,2},{3,4},{5,6}} };

cout<< y.size()<<endl; // 3 rows
cout<<y[0].size()<<endl; // 2 columns
cout<<y[2][1]<<endl; // 6, accessing elements 

for (auto i=0; i<3; i++)
    for (auto j=0; j<2; j++)
        cout<< &y[i][j]<<endl; // writing memory addresses
/*
0x7ffdb9d2e480
0x7ffdb9d2e484
0x7ffdb9d2e488
0x7ffdb9d2e48c
0x7ffdb9d2e490
0x7ffdb9d2e494      
*/
return 0;
}
```

Looking at the memory addresses of elements, we see they are contiguously placed in the memory. The addresses are incremented by 4 units in the hex system. When we have an array of arbitrary objects, depending on the type of the object, a compiler may add padding bytes between objects in memory.

## std::vector

Vector is a standard container that can create an array of contiguous objects on the heap. The array is dynamic: objects can be added or removed during runtime. The memory of a vector is managed by C++, when it goes out of scope, all the elements are automatically destructed. Note that if the elements are raw pointers, only raw pointers are removed but their target memory is untouched. 

```cpp
#include <iostream>
#include<vector>
int main(){
std::vector<int> v = {3, 4};
v.push_back(5);
std::cout<<v.size()<<endl; // 3
}
```

A multidimensional vector can be created by creating a vector of vectors. A 2D vector is defined in example below, then it's first row is extended:

```cpp
#include <iostream>
#include<vector>
using namespace std;
int main(){
typedef vector<int> Row;
vector<Row> v = {{1,2},{3, 4},{5,6}};
cout<<v.size()<<endl; // 3 rows
cout<<v[0].size()<<endl; // 2 columns

cout<<"Initial vector:"<<endl;
for (auto& row:v)
    for (auto& item:row)
        cout<< &item<<endl; // writing memory addresses
/*                                                                                                   
0x1230cd0  Row[0]
0x1230cd4
0x1230cf0  Row[1]
0x1230cf4  
0x1230d10  Row[2]
0x1230d14 
*/

v[0].push_back(10);
v[0].push_back(11);

cout<<"Extended vector:"<<endl;
for (auto& row:v)
    for (auto& item:row)
        cout<< &item<<endl; // writing memory addresses
/*
0x1230c20  Row[0]
0x1230c24
0x1230c28
0x1230c2c
0x1230cf0  Row[1]
0x1230cf4
0x1230d10  Row[2]
0x1230d14        
*/

cout<< &v; // 0x7fff650e1ca0 
return 0;
}
```

As shown, the memory is contiguous in each row but there are gaps between rows. Each row is managed independently by its own vector. To clear that up, we added more items to the first row. Subsequently, `Row[0]` is allocated on a new memory location to accommodate the new elements. It happened without a change in memory locations of the other rows.

Here we notice an important difference between a vector of vectors and an std::array of std::arrays. The former can hold data structures which are rows of different sizes.

The memory addresses shown in the example above were elements of the vector, but the vector class contains a pointer to those elements along with other private members such as the capacity for vector management. So, if defined in a function, the vector object is created on the stack (see the output of `&v`) but the elements are allocated on the heap. Moreover, when we create a vector of n vectors, we create n vector objects on the heap each of which containing a pointer and private members.


## Boost::multiarray

Boost multiarray creates a contiguous N-dimensional array which claims to be more efficient than a vector of vectors [see here](https://www.boost.org/doc/libs/1_75_0/libs/multi_array/doc/user.html). To use this, you need Boost library installed.  The data type and dimension (or rank) of the array needs to be known at compile-time,  however, the size of multiarray in each dimension can be changed at runtime. 

```cpp
#include <iostream>
#include "boost/multi_array.hpp"

using namespace std;
int main()
{
  typedef boost::multi_array<double, 3> array_type;

  array_type A(boost::extents[3][4][2]);
  A[0][0][0] = 10;
  cout<<A[0][0][0]; //10

  // reshaping the array
  boost::array<array_type::index,ndims> dims = {{4, 3, 2}};       
  A.reshape(dims);
  
  // Resizing the array
  A.resize(boost::extents[2][3][4]);
}
```


## Custom multidimensional (nD) array 

We can create and customize our array based on the requirement of our program. Let's create a 2D array of points. Each point has a position (x,y), temperature, and velocity (Vx, Vy). The points and their data must be contiguous in memory.  

We add the headers first
```cpp
#include <iostream>
#include <vector>
#include <array>
using namespace std;
```
The point contains the data requested. I used `std::array` instead of `std::vector` for position and velocity to ensure their data stay within the point structure. 

```cpp
struct Point{
    array<double, 2> Position = {0,0};
    array<double, 2> Velocity = {0,0};
    double Temperature = 0;
};
```
Now we can create the custom container, `Grid`:

```cpp
struct Grid{
    Grid(size_t sizeX_, size_t sizeY_)
        :sizeX(sizeX_),sizeY(sizeY_){
            points.resize(sizeX_*sizeY_);
        }
    
    Point& operator() (size_t ix, size_t iy){
        return points[GetIndex(ix,iy)];
    }
    size_t GetIndex(size_t ix, size_t iy){
        return iy + ix*sizeY;
    }
    size_t GetSizeX() {return sizeX;}
    size_t GetSizeY() {return sizeY;}
    
    private:
    
    size_t sizeX;
    size_t sizeY;
    
    vector<Point> points;
};
```

Let's define a function that shows the memory addresses of members of a point

```cpp
void ShowMemory(Point& point){
    double* ptr[3];
    ptr[0] = &point.Position[0];
    ptr[1] = &point.Velocity[0];
    ptr[2] = &point.Temperature;
    for (auto& item:ptr)
        cout<<item<<endl;
};
```

And finally, we test the custom array:

```cpp
int main(){
    
    Grid grid(3,2);
    
    // Accessing elements
    grid(0,0).Temperature = 100;
    grid(0,0).Velocity[0] = 1.0;
    grid(0,0).Velocity[1] = 2.0;
    
    cout<<grid(0,0).Temperature<<endl; //100
    cout<<grid.GetSizeX()<<endl; // 3
    
    // Memory layout
    
    for (auto ix=0;ix<grid.GetSizeX();ix++)
        for (auto iy=0;iy<grid.GetSizeY();iy++){
            cout<<"point "<<ix<<","<<iy<<endl;
            ShowMemory(grid(ix,iy));
        
        }
/*
point 0,0
0xc00c20
0xc00c30
0xc00c40
point 0,1
0xc00c48
0xc00c58
0xc00c68
point 1,0
0xc00c70
0xc00c80
0xc00c90
point 1,1
0xc00c98
0xc00ca8
0xc00cb8
point 2,0
0xc00cc0
0xc00cd0
0xc00ce0
point 2,1
0xc00ce8
0xc00cf8
0xc00d08        
*/    
}
```
Note the memory addresses are contiguous.
                                                                                                           
## Which array is the best?

If you are working with old legacy codes, there is not much flexibility; you are confined to C-style and pointer arrays. However, if you have options, use modern C++ features: 

* **std::vector**: If not sure, this one is the first pick. For any-size contiguous arrays whose size can be changed during runtime. 
* **std::array**: for small and fixed-size arrays and creating objects which contain the array data. 
* **Custom array**: to create multidimensional full contiguous data using std::vector and std::array. 
* **vector of vectors**: for row-column data structures with dynamic contiguous data in each row, but rows are not one after the other in memory. 
* **Boost multiarray**: if Boost library available, this one is preferred than writing a custom multidimensional array. 


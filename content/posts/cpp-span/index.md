---
title: "Span is a new norm in C++ codes"
date: 2021-03-27T18:10:20+01:00
image: /images/trees.jpg
imageQuality: "q65"
imageAnchor: "Center" # Smart, Center, TopLeft, Top, TopRight, Left, Right, BottomLeft, Bottom, BottomRight.
tags: ["C++"]
categories: "C++" 
summary: "Span is a new feature of C++20 for reading and writing a sequence of objects. Here, I mention how to use std::span and its functions including subspan."
---

## Definition

Available in *C++20*, `std::span` is a **view** of a contiguous sequence of objects. It is a struct like:

```cpp
struct span<T>{
    T*  pointer; // start of sequence
    size_t size; // size of sequence
}
```
with many useful functions to access and modify data.

## Compiler
To compile examples here, I use *GCC 10.2* with flag `-std=c++20`.


## Basics

`span` interface can attach to a C-array:

```cpp
#include<span> // remember header

int main(){

int a[2]={4,3};
std::span<int> s = a;
std::cout<< s[0] <<s[1];// 4 3

return 0;}
```
to a dynamic pointer array:

```cpp
int* a = new int[2]{8, 8};
std::span<int> s{a, 2}; // size=2
```

to an array:

```cpp
std::array<int,2> a = {5,6};
std::span<int> s = a;
```

to a vector:

```cpp
std::vector<int> a = {1,1};
std::span<int> s = a;
```

and to a part of array or vector:

```cpp
std::vector<int> v = {1,2,3,4};
std::span<int> s{a.data()+2,2};
std::cout<< s[0]<<s[1]<<'\n'; // 3 4
```

The compiler can automatically deduce the type of a span at initialization, so this is correct:
```cpp
std::vector<int> a = {1,1};
std::span s = a; // span<int>
```



## Functions

Similiar to standard containers, `span` has many useful functions that facilitate working with a sequence.
For a span like:

```cpp
std::vector<int> v = {1,2,3,4};
std::span s = v;
```

We can traverse items with range-base loop:

```cpp
for (auto& item:v)
        std::cout<<item;
```

Read or write elements:

```cpp
auto a = v.front(); // first element of sequence
auto b = v.back(); // last element of sequence
auto c = v[2]; // access via []
auto d = v.data(); // pointer to first element
```

Check the size:

```cpp
auto e = v.size();
bool f = f.empty();
```

Get iterators:

```cpp
auto g = v.begin(); // iterator to begining
auto h = v.end();// iterator to end
```

## Subspan

A subspan is a **span** made of another span. The subspan is shorter or the same size as the primary span. For example, for a span

```cpp
std::vector<int> v = {1,2,3,4,5,6};
std::span s = v;
```

we can get a span for the first 3 items:

```cpp
auto s1 = s.first(3); // {1, 2, 3}
```

last 2 items:

```cpp
auto s2 = s.last(2); // {5,6}
```

or an arbitrary span:

```cpp
// subspan(offset, count)
auto s3 = s.subspan(2, 3); // {3,4,5}
```

If the count is not given, subspan will be from offset to the end:

```cpp
// subspan(offset)
auto s4 = s.subspan(2); // {3,4,5,6}
```


## Don'ts

Do not change the memory of a sequence, while working with a span pointing to it. 

In the example below, a vector is assigned to a span, the vector's memory location changed, then the span reused. This causes undefined behavior:

```cpp
#include <iostream>
#include <vector>
#include <span>
int main(){

std::vector<int> v = {1,2,3,4};
std::cout<< v.capacity() <<'\n'; // 4

// span defined
std::span s = v;

// target memory changed
v.push_back(5);

// undefined behaviour
std::cout<< s[0] <<'\n';

return 0;}
```

Note that when we `push_back(5)`, the vector memory is deleted and a new memory in a different location is allocated to fit in the new item, 5. But span, `s`, is still pointing to the old memory of the vector.

For the same reason, don't do this either:

```cpp
#include <iostream>
#include <span>
int main(){

int* a = new int[4] {1,2,3,4};

// span defined
std::span s {a, 4};

// memory gone
delete a;

// undefined behaviour
std::cout<< s[0]<<'\n';

return 0;
}
```


## Function parameter

It's very common to pass a vector or array to a function, and the function only wants to read/write elements but doesn't add/delete elements or deallocate the memory; that's when span comes in handy.

See this example:
```cpp
int sum(std::span<int> items){
    int s = 0;
    for (auto& item:items)
        s+=item;
    return s;
}
```
`sum` reads the items but doesn't delete any item i.e. it **doesn't own** the memory. The outer scope is responsible to pass valid memory to `sum`.

Now we can pass various contiguous sequences to `sum`:

```cpp
int main(){
    
    std::vector<int> v = {1,1,1};
    std::array<int,4> a = {1,1,1,1};
    int b[5]{1,1,1,1,1};

    std::cout<< sum(v)<<'\n'; // 3
    std::cout<< sum(a)<<'\n'; // 4
    std::cout<< sum(b)<<'\n'; // 5

    return 0;
}
```

## Class member

A span can be a class member. It is an observer of a sequence of objects. The class is not responsible for managing the memory of the sequence.  It can read/write the objects, but cannot delete them. The user of the class is responsible for providing a valid contiguous memory.

## Static span

We can specify the size of a span to be fixed at runtime:

```cpp
std::span<Type, Size>
```

We can directly assign a `std::array` but **not** a `std::vector` to a fixed span, see the example below:

```cpp
#include <iostream>
#include <vector>
#include <array>
#include <span>

int main(){

int a[4] {1,2,3,4};
std::vector<int> v = {1,2,3,4};
std::array<int,4> arr = {1,2,3,4};

// static span
std::span<int,4> s = a;

// reassign
s = arr; // OK

// Error: assign span<int,4> to vector<int>
s = v;

for (auto& item:s)
    std::cout<< item<<'\n';

return 0;
}
```

As it is shown before, if we don't specify the size of a span, it will be dynamic during runtime.


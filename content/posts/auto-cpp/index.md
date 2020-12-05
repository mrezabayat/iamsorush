---
title: "C++ auto makes your life easier"
date: 2020-12-03T18:10:20+01:00
image: /images/pingpong.jpg
imageQuality: "q65"
imageAnchor: "Center" # Smart, Center, TopLeft, Top, TopRight, Left, Right, BottomLeft, Bottom, BottomRight.
tags: ["C++"]
categories: "C++" 
summary: "In C++, *auto* keyword can speed up coding and improve maintainablity of code. Here, I show cases that *auto* can make a difference."
draft: true
---

## Introduction

Frome C++11, a compiler can deduce the type of a variable, being declared, from its initializer. Therefore, the keyword `auto` is enough to declare such a variable. 

## Primitive types

`auto` can figure out the below types 

```cpp
auto i = 1; // int
auto x = 2.0; // double
auto y = 2.0f; // float
auto c = 'A'; // char
auto b = true; // bool
```

From C++14, we can have string-literals, so compiler deduce `std::string`:

```cpp
using namespace std; // This is necessary
auto s = "hellow"s // std::string, note the s operator. 
```

## Test 

You can check the types deduced with `typeid` as below

```cpp
#include <iostream>
#include <typeinfo>

int main()
{
    auto x=1.0;
    std::cout<<typeid(x).name()<<std::endl;

    return 0;
}
```

To ensure the type is correctly inferred, we can implement `static_assert`. It throws a compilation
error if the type is not correct:

```cpp
#include <type_traits>

auto x = true;
static_assert(std::is_same<decltype(x), bool>::value, "x must be bool");
```

## Function


## Template
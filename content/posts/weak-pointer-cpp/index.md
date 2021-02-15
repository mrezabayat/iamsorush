---
title: "What is a C++ weak pointer and where is it used? smart pointers part III"
date: 2021-02-14T22:10:20+01:00
image: /images/binocular.jpg
imageQuality: "q65"
imageAnchor: "Center" # Smart, Center, TopLeft, Top, TopRight, Left, Right, BottomLeft, Bottom, BottomRight.
tags: ["C++", "Pointers"]
categories: "C++" 
summary: "Weak pointers are smart pointers that break the circular dependency of shared pointers. Here, I explain them with examples."
---

## Introduction

Weak pointers are smart pointers that, in contrast to unique and shared pointers, do not take ownership of an object but act as an observer. 


## Prerequisites

This post assumes you are familiar with [raw pointers](https://iamsorush.com/posts/how-use-cpp-raw-pointer/), [unique pointers](https://iamsorush.com/posts/unique-pointers-cpp/), [shared pointers](https://iamsorush.com/posts/shared-pointer-cpp/), and [auto keyword](https://iamsorush.com/posts/auto-cpp/). 

All the examples are compiled with GCC 10.2 with the flag `-std=c++20`.

For brevity, some examples miss the headers and main function:

```cpp
#include <iostream> // For std::cout
#include <memory> // For std::weak_ptr

using namespace std; // dropping std::

// class definitions

int main(){

    // implementations

    return 0;
}
```

## Definition

Consider the example class below 

```cpp
struct Person{
    string Name;
    Person(string n):Name(n){}
};
```

A weak pointer working with an object of `Person` is defined as

```cpp
std::weak_ptr<Person> wp;
```

A weak pointer is used to observe the object of a shared pointer


```cpp
auto teacher = make_shared<Person>("Jack");

wp = teacher; // wp watches the managed object of teacher
```

Somewhere else that we are not sure if the object is still there or not:

``` cpp
if (auto tempSharedPointer = wp.lock()){ // if sp empty
    cout<< tempSharedPointer-> Name;
} else
{
    cout<< "The object is not there.";
}
```

In the above example `lock()` returns a temporary shared pointer pointing to the managed object.


## Change of object

Note that a weak pointer watches the managed object not shared pointers. Let's assume a weak pointer starts observing the object of a shared pointer. Sometime later, the shared pointer changes its object to a new one. The weak pointer is still observing the old object.

```cpp

struct Person{
    string Name;
    Person(string n):Name(n){}
};


int main(){

std::weak_ptr<Person> wp;

  
    auto teacher = make_shared<Person>("Jack");
    wp = teacher;

    if (auto temp = wp.lock())
        cout<< temp-> Name; //  Jack

    teacher.reset(new Person("Rose"));

    if (wp.expired()) // true
        cout<< "The old teacher is not there."; 

}
```

## Why we need shared pointers?


In previous examples, I showed how to use a weak pointer but we don't need them there. They can be replaced by shared pointers. The main reason weak pointers are invented is to **break circular dependency** of shared pointers. Otherwise, they cannot delete their objects:

```cpp
struct Person;

struct Team{
    shared_ptr<Person> goalKeeper;
    ~Team(){cout<<"Team destructed.";}
};
struct Person{
    shared_ptr<Team> team;
    ~Person(){cout<<"Person destructed.";}
};

int main(){
    
    
    auto Barca = make_shared<Team>();
    auto Valdes = make_shared<Person>();
    
    Barca->goalKeeper = Valdes;
    Valdes->team = Barca;
    
    return 0;

}

```

In the example above, the destructors are not called and we have a memory leak. The managed object of a shared pointer is deleted when the reference count reaches zero. If `Barca` goes out of scope, it is not deleted since the managed object is still pointed by `Valdes.team`. When Valdes goes out of scope, its managed object is not deleted either as it is pointed by `Barca.goalKeeper`. 


This case can be solved with a weak pointer:

```cpp
struct Person;

struct Team{
    shared_ptr<Person> goalKeeper;
    ~Team(){cout<<"Team destructed.";}
};
struct Person{
    weak_ptr<Team> team; // This line is changed.
    ~Person(){cout<<"Person destructed.";}
};

int main(){
    
    
    auto Barca = make_shared<Team>();
    auto Valdes = make_shared<Person>();
    
    Barca->goalKeeper = Valdes;
    Valdes->team = Barca;
    
    return 0;

}

```

Both destructors are called. When `Barca` goes out of scope, it will be destructed as it is pointed by a weak pointer (non-owner). `Valdes` is destructed easily as it is not pointed by anything.

One may say what if `Valdes` goes out of scope first? its object is not deleted but its reference count changes to 1. When `Barca` goes out of scope, it destructs its managed object which destructs the `goalKeeper` i.e. `Valdes`. 

## References

[cppreference](https://en.cppreference.com/w/cpp/memory/weak_ptr)
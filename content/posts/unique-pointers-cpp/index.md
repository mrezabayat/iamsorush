---
title: "What is a C++ unique pointer and how is it used? smart pointers part I"
date: 2021-01-31T19:10:20+01:00
image: /images/dolphin.jpg
imageQuality: "q65"
imageAnchor: "Center" # Smart, Center, TopLeft, Top, TopRight, Left, Right, BottomLeft, Bottom, BottomRight.
tags: ["C++", "Pointers"]
categories: "C++" 
summary: "Unique pointers (unique_ptr) manage a pointer's allocated memory. Here, I
define them and explain the operations, passing to / returning from a function, and performance. A factory example is also demonstrated."
---

## Introduction

Unique pointers are smart pointers that help us in memory management. Unique pointers guarantee they delete their object if they are destructed, therefore, one less hassle for programmers. They follow "Resource Acquisition Is Initialization" (RAII) rule.


## Prerequisites

Here, I assume you are aware of [raw pointers](https://iamsorush.com/posts/how-use-cpp-raw-pointer/) and [auto keyword](https://iamsorush.com/posts/auto-cpp/). 

I compiled the examples using GCC 10.2 with flag `-std=c++20`.

To be focused, the headers and `main()` are omitted in some examples:

```cpp
#include <iostream> // For std::cout
#include <memory> // For std::unique_ptr, std::make_unique

using namespace std; // dropping std::

// class definitions

int main(){

    // implementations

    return 0;
}
```

## Unique pointer

A unique pointer is defined as

```cpp
std::unique_ptr<int> p(new int); // p is allocated a new int on the heap
```

{{< img "*definition*" "pointer allocation" >}}

If the unique pointer is destructed, the allocated object on the heap  is destructed too

```cpp
{
  unique_ptr<int> p(new int);
  // make use of p

} // p is destructed, so the int object is destructed.
```
{{< img "*delete*" "pointer allocation" >}}


Compare the above code with [raw pointers](https://iamsorush.com/posts/how-use-cpp-raw-pointer/#memory-leak) which are deleted explicitly by programmers.

A unique pointer can also be created with `std::make_unique`

```cpp
#include <memory>
using namespace std;

struct A{
  A(int a):m(a){}
  int m;
};

int main(){
    auto p = make_unique<A>(8); // A constructor is called.
    return 0;
}
```

## Ownership

A unique pointer is a 1-to-1 relationship between a pointer (`p`) and its allocated object on the heap (`new int`).

```cpp
unique_ptr<int> p(new int);
// p <-------->  object
```

`p` owns the object and the object has only one owner, `p`. So when programming, we can think of them as one entity. 


{{< img "*entity*" "pointer allocation" >}}



A unique pointer cannot be copied or passed by value. However, the ownership of its object can be transferred.  



A unique pointer can be empty too

```cpp
unique_ptr<int> p; // empty pointer, contains null pointer
```


## Operations

A unique pointer supports operations below

```cpp
struct A{ 
       int M;
       A(int m):M(m){}
};

auto p = make_unique<A>(8); // create unique pointer
auto B = *p; // dereference pointer
p->m = 11; // access class members
```

There is a raw pointer inside a unique pointer which can be accessed:

```cpp
auto r = p.get(); // get the raw pointer
```

Use above raw pointer only for calculations and do not delete it as it is managed by a unique pointer. 


The object allocated to the pointer can be changed but remember that it is automatically deleted:

```cpp
#include<iostream>
#include<memory>
using namespace std;

int main(){

    auto q = make_unique<int>();
    cout<< q <<'\n'; // points to 0xb1feb0

    q = make_unique<int>(); // The data in 0xb1feb0 deleted.
    cout<<q; //points to new object in 0xb20ee0

    return 0;
}
```

The pointer can be reset to a new object

```cpp
auto q = make_unique<int>(); // q created with an int object on the heap
q.reset(new int()); // The previouse object deleted, a new one is created.
```

Only one unique pointer owns the object on the heap:

```cpp
auto q = make_unique<int>(); // q associate to a newly created object on the heap
auto p = q; // Error: the object belongs to q and cannot be shared.
```

However, the ownership of the object can be transfered via `std::move()`:

```cpp
auto q = make_unique<int>(); // q created with an int object on the heap
auto p = move(q); // p owns the q's object, q lost it (null pointer).
```

{{< img "*move*" "pointer allocation" >}}


`std::swap` works with unique pointers

```cpp
auto p = make_unique<int>(); 
auto q = make_unique<int>(); 
swap(p,q); // p points to q's object and vice versa.
```


A unique pointer can be checked if it is associated with an object

```cpp
unique_ptr<int> a; // a created but is empty (null pointer)
if (a) // (bool) a returns false as it is not associated.
  cout<<*a; // This is not run.
```

## Pass to a function

The function below takes the ownership of a unique pointer. To pass the pointer `std::move()` must be used:

```cpp
#include<iostream>
#include<memory>
using namespace std;

struct A{
    ~A(){cout<<"Deleted.";}
};

void PassIn(std::unique_ptr<A> a)
{
    cout<< "Pointer received."<<'\n';

} // a and its object are deleted.


int main(){
    
    auto x = make_unique<A>();
    PassIn(move(x)) // Pointer received.
    ; // Deleted.
    
    if (!x) cout<< "x is empty."; // true: x is empty.
    
    return 0;
}

```
## Return from function

A function can return a unique pointer. Consequently, it gives up the ownership of the pointer:

```cpp
#include<iostream>
#include<memory>
using namespace std;

struct A{};

std::unique_ptr<A> PassOut()
{
    auto a =  make_unique<A>();
    return a;
} 


int main(){
    
    auto x = PassOut();

    if (x) cout<< "x has an object."; // true: x has an object.
    
    return 0;
}
```

## Pass to observer function

If the function only works with the pointer's object and doesn't care about the ownership, we can pass the unique pointer by a reference or raw pointer.
If null pointer should be handled, we pass it by a raw pointer:

```cpp
#include<iostream>
#include<memory>
using namespace std;

struct Database{
    double GetAverageSalary(){return 1000;};
};

void ShowSalaryDifference(double salary, Database* db)
{
    if (!db) throw runtime_error("Database is null.");
    cout<< salary - db->GetAverageSalary();
} 

int main(){
    
    auto db = make_unique<Database>();
    ShowSalaryDifference(1200, db.get()); // 200
    
    return 0;
}
```

If we are sure db definitely has an object, we can pass it by reference

```cpp
void ShowSalaryDifference(double salary, Database& db)
{
    cout<< salary - db.GetAverageSalary();
} 


int main(){
    
    auto db = make_unique<Database>();
    ShowSalaryDifference(1200,*db); // 200
    
    return 0;
}

```


## Class member: unique pointer vs raw pointer vs reference

If we design our program based on smart pointers, we can assume below rules for a class member:

* Unique pointer member: the class is the owner of the pointer's object.
* Raw pointer member: the class is an observer and not responsible for deleting the pointer's object. It is deleted by
a smart pointer outside of this class. The pointer can be null.
* Reference member: it is guaranteed that the reference contains valid data while the class object is alive.


## Performance

Accessing unique pointers is as fast as raw pointers. The class of the unique pointer contains only a raw pointer as the data member, so, the size of a unique pointer is the same as a raw pointer. All in all, unique pointers can safely replace raw pointers in high-performance calculations.


## Factory Example

A factory that creates unique pointers is shown below

```cpp
#include<iostream>
#include<memory>
using namespace std;

struct Base{};
struct Derived:Base{};

std::unique_ptr<Base> create(int option)
{   
    if (option == 0)
        return make_unique<Base>();
    else if (option==1)
        return make_unique<Derived>();
    else
        throw runtime_error("Wrong option.");
}
int main(){
    
    auto p = create(1);
    return 0;
}

```



## References

[unique pointer from cppreference](https://en.cppreference.com/w/cpp/memory/unique_ptr)

[isocpp](http://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#r-resource-management)
---
title: "From lvalue, prvalue, and xvalue to move semantics in C++"
date: 2021-02-21T20:12:10+01:00
image: /images/sandy.jpg
imageQuality: "q65"
imageAnchor: "center"
tags: ["C++"]
categories: "C++" 
summary: "With examples, I explain the difference between lvalue, rvalue, prvalue, and xvalue. The rvalue references are defined. Consequently, I describe std::move and its application in creating move constructors and assignments."
---

## Introduction

In C++ values are divided into different categories. Knowing them helps us understand the compiler's behind the scene actions and optimise them to our benefit.

In older than C++11, a value was either **rvalue** or **lvalue**. An lvalue was anything that could be at the left-hand side (LHS) of an assignment, `=`, operator. An rvalue was anything 
that is allowed to be on the right-hand side (RHS) of an assignment but **not** LHS. 

```cpp
int y = 5;
```

So in the example above `y` is an lvalue and `5` is an rvalue. Because a statement like `5 = y` is not allowed.


In modern C++, things got a bit more complex, nowadays we have lvalue, **prvalue** and **xvalue**.


## lvalue

Generally, a named variable that we can have it on the LHS of an assignment:

```cpp
int y = 10;  // y is lvalue
double m = 1.5; // m is lvalue

int* p = new int{5}; // p is lvalue
*p = 4;  // *p is lvalue too

int a[5];
a[1] = 10; // array element is lvalue

int& r = y; // r is lvalue reference
```

In the above example, r is called **lvalue reference**. It is an alias for an lvalue. In other words, it binds to an lvalue. So, the RHS of an lvalue reference must be an lvalue.

```cpp
int& r = 5; // Error, 5 is not an lvalue
```

## prvalue

A prvalue or pure rvalue can only be at the RHS of an assignment.  

For example, literals

```cpp
int x = 2; // 2 is prvalue
string name = "Jack"; // "Jack" is prvalue
bool a = true; // true is prvalue
```
A temporary object is created with a literal, then it is passed to the LHS or lvalue. 

RHS expressions that have an outcome due to some operations are rvalues

```cpp
int x=1,y=1;
int a, b, c;
double d;

a = x+y; // the outcome of x+y is prvalue
b = -x; //  -x is prvalue
c = x+1; // x+1 is prvalue
d = (double) c; // cast is prvalue
```

In the above example, `x+y`, `-x`, `x+1`, and `(double)c` are calculated first which result in temporary objects. 
The objects are then passed to the copy assignments. **The rvalue objects are destructed after assignment** i.e. 
when we reach `;` the rvalues are destructed.

The result of a function returning by value is prvalue:

```cpp
int f(int i){ return i;}

int x = f(5); // the outcome of f(5) is rvalue
```

Objects which are created without names

```cpp
class A{};
A y;
y = A{}; // the object A{} is rvalue
```

The list of prvalues is longer than this but a simple test to know if an RHS is prvalue is to switch LHS with RHS, and seeing whether it makes sense:

```cpp
A{} = y; // doesn't make sense.
```

## rvalue reference

An lvalue reference or simply a reference can bind to another lvalue

```cpp
int x;
int& y =x;
```

We have the same for rvalues. An rvalue reference is defined as `T&&` and it only binds to rvalues

```cpp
int x;

int&& y = x; // Error: cannot bind rvalue reference to lvalue

int&& y = 5; // OK: y binds to rvalue object of 5.

y = 7; // OK: y still refering to the same memory which was 5 
cout<< y; // 7

cout<< is_same<int&&, decltype(y)>::value; // true
```

In the previous section, I mentioned rvalues are destructed when we hit `;`, but we have an exception here.
The lifetime of rvalue `5` is extended to the lifetime of `y` due to the binding.

Note that we wrote `y=7`, therefore, **a named rvalue reference is lvalue**.

We can overload a function based on a parameter being lvalue or rvalue:

```cpp
void f(int& i){
    cout<< "lvalue reference called";
}

void f(int&& i){
    cout<< "rvalue reference called";
}

int x = 10;
int&& y =7;

f(x); //lvalue reference called.
f(5); //rvalue reference called.
f(y); // lvalue reference called
```

So `x` and `y` are lvalues, the first function is called, `5` is an rvalue so the second function is called.



## move constructor: steal rvalue resource

We can improve code efficiency by making use of resources of an rvalue. I explain it with an example. 
We have `Player` class as

```cpp
struct Player{
    string name;
};
```

We have a team class with three constructors

```cpp
struct Team{
    Team(){
        goalKeeper = new Player{.name="Marc"};
    };
    Team(const Team& t){
        goalKeeper = new Player{*t.goalKeeper};
    };
    Team(Team&& t){ // move constructor
        goalKeeper = t.goalKeeper;
        t.goalKeeper = nullptr;
    };
    ~Team(){delete goalKeeper;}

   Player* goalKeeper;    
};
```

The first constructor is the default one. The second one constructs the object with an lvalue reference which reads the argument, `t`. But the third one steals the 
`goalKeeper` object of `t`.  We are allowed to do that because the object is an rvalue, when the constructor finishes its job, `t` will be destructed. The third constructor is called **move constructor**. Similar behaviour can be defined for the assignment which is called move assignment.



Let's implement the code:

```cpp
int main(){
   Team Barca{ Team{} }; 

    return 0;
}
```
So, in the example above, a temporary rvalue object is created by `Team{}` which calls the default constructor. The object is passed to the constructor of `Barca`. Because it is an rvalue, the move constructor is called. The resources of the temporary object are moved to `Barca`. After `Barca` created, the temporary object is destructed. 
Note standard containers have built-in move constructors.

## std::move

There are situations that a programmer knows that an lvalue object will be destructed soon and wants to take its resources using a move constructor/assignment.
`std::move` casts an lvalue to rvalue reference type. Note that `std::move` doesn't move anything it is just a static cast without computational cost.

Let's use assignment operator with rvalue reference (move assignment):

```cpp
#include <iostream> 
using namespace std;

struct Player{
    string name;
};

struct Team{
    Team(){cout<<"default"<<'\n';};
    Team(const Team& t){
        cout<<"ref ctor"<<'\n';
        goalKeeper = new Player{*t.goalKeeper};
    };
    Team& operator=(const Team& t){
        cout<<"ref assign"<<'\n';
        goalKeeper = new Player{*t.goalKeeper};
        return *this;
    };
    Team& operator=(Team&& t){
        cout<<"rval assign"<<'\n';
        goalKeeper = t.goalKeeper;
        t.goalKeeper = nullptr;
        return *this;
    }
    ~Team(){
        cout<<"delete"<<'\n';
        delete goalKeeper;}

   Player* goalKeeper;    
};
```

Now let's define an lvalue object and cast it to be an rvalue:

```cpp
int main(){
    
   Team Barca{}; // default
   Team Real{}; // default

   {
     Team temp{}; // default
     temp.goalKeeper = new Player{.name="Marc"};

     Real = temp; // ref assign
     Barca = move(temp); // rval assign
     
   }
   // delete : temp
    return 0;
} // delete delete: Barca and Real
```

In the above example, `temp` is going out of the scope to be destructed. Before that happens, we cast `temp` to rvalue reference with 
`std::move` then pass it to move assignment of `Barca`.


## xvalue

Graduating `std::move`, now we can define xvalue. An expiring value or xvalue is a value that is about to die so we can steal its resources.
The result of a function like `std::move()` which returns an unnamed rvalue reference, `T&&`, is an xvalue:

```cpp
void f(int& i){
    cout<< "lvalue reference called";
}

void f(int&& i){
    cout<< "rvalue reference called";
}

int x = 10;
f(x); // lvalue reference called
f(std::move(x)); //rvalue reference called.

```


A cast to an rvalue reference is an xvalue:

```cpp
// using previous example functions
f(static_cast<int&&>(x)); //rvalue reference called.
```

An expression to access a member of an rvalue object is an xvalue:

```cpp
struct A{ int i=5;};

int j = A{}.i; // A{}.i is xvalue

```

## Where to use move semantics?

The best place to take advantage of move semantics is move constructors and assignments for classes
that have movable data. In this way, we avoid the deep copy of rvalues.

However, I wouldn't employ them in every class because the speed gain would be in assignment and constructor calls. The improvement in those actions is hardly visible if we are not moving massive objects many times. On my laptop,
the deep-copy of a vector of 1 million doubles takes only 1 millisecond. Moreover, adding move constructors/assignments and `std::move`, `st::forward` and related commands makes the code harder to read and maintain. Furthermore, there are cases that a compiler itself reduces the number of objects created ([Copy elision](https://en.cppreference.com/w/cpp/language/copy_elision)).  So, if the performance gain is negligible move semantics are better to be avoided.

There are, of course, other scenarios. For example, if we write a generic library that is supposed to be used in other projects. It will be more likeable to others if the API of the library supports the move semantics.








## References

[cppreference](https://en.cppreference.com/w/cpp/language/value_category).















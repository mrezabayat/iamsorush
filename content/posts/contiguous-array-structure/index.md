---
title: "Create a contiguous array of a generic class in C++ "
date: 2021-01-10T18:10:20+01:00
image: /images/glasses.jpg
imageQuality: "q65"
imageAnchor: "Center" # Smart, Center, TopLeft, Top, TopRight, Left, Right, BottomLeft, Bottom, BottomRight.
tags: ["C++"]
categories: "C++" 
summary: "I want to create a contiguous array of a class and its derived ones. I make sure the polymorphism behavior is captured too."
---

## Introduction

The performance of a numerical program can be enhanced if the necessary data needed for a calculation are near each other in memory. This may lead to cache optimization. 

## Goal

- Create a contiguous array of  a class.
- The array can be created for derived classes too.
- Polymorphism is available in these generic objects.

## Example

The pseudocode is 
```
struct Base{...}; 
struct Derived:Base{...};
ContiguousArray<Base> a;
ContiguousArray<Derived> b;

A* p = &a[0];
p-> doSomeThing(); // run base method
p = &b[0];
p-> doSomething();// run derived method
```

## Code

The whole code is here, for the explanation see the next section.

```cpp
#include <iostream>
#include <memory>
#include <vector>
using namespace std;

template<size_t dim, class T>
struct Specs{
    static const size_t Dim = dim;
    using Type = T;
};

template<class S>
struct Particle{
    using Specs = S;
    Specs::Type Position[S::Dim];
    virtual void Print(){
        cout<<"Pos:";
        for (auto& p:Position)
            cout<<p<<" ";
        cout<<endl;
    }
};

template<class S>
struct Particle_Radius: Particle<S>{
    typename S::Type Radius;
    virtual void Print() override{
        Particle<typename S::Specs>::Print();
        cout<<"Radius:"<<Radius<<endl;
    }
};

template<class S>
struct Particle_MassVelocity: Particle<S>{
    typename S::Type Mass;
    typename S::Type Velocity[S::Dim];
    virtual void Print() override{
        Particle<typename S::Specs>::Print();
        cout<<"Mass: "<<Mass<<endl;
        cout<<"Velocity:";
        for (auto& v:Velocity)
            cout<<v<<" ";
        cout<<endl;
    }
};

template <class T, class U>
concept Derived = std::is_base_of<U, T>::value;

template<class P> 
requires Derived<P,Particle<typename P::Specs> >
struct Block{
    vector<P> particles;
    
    //returns particle base class reference
    Particle<typename P::Specs>& Get(size_t i){return particles[i];}

    void print(){
        for (size_t i=0;i<particles.size();i++)
            Get(i).Print(); // polymorphic Print
    }
};


int main()
{
  Particle_Radius<Specs<3,double> > p1;
  p1.Position[0]=4.1; 
  p1.Position[1]=5.1;
  p1.Position[2]=6.1;
  p1.Radius = 7.1;
  Block<decltype(p1)> block;  
  block.particles.push_back(p1);
  block.print();
     /* Pos:4.1 5.1 6.1 
        Radius:7.1  */ 
   
  Particle_MassVelocity<Specs<2,int>> p2;
  p2.Position[0]=4.1; 
  p2.Position[1]=5.1;
  p2.Mass = 6.1;
  p2.Velocity[0]=7.1;
  p2.Velocity[1]=8.1;
  Block<decltype(p2)> block2;  
  block2.particles.push_back(p2);
  block2.print();
    /* Pos:4 5 
       Mass: 6
       Velocity:7 8 */
}

```

## Specs

This class holds the datatypes used for numbers in `Type` like `float`, `double`, `int` and dimensions of the system, `Dim` to be 1D, 2D or 3D. `Dim` is `static const` because we have one Specs class for each `Dim` and it must be available at compile time to allocate arrays.


```cpp
template<size_t dim, class T>
struct Specs{
    static const size_t Dim = dim;
    using Type = T;
};
```

## Particle

`Particle` is the base class, it gets the specs as template type, allocates `Position` array, contains a `virtual` method which prints its content on screen.
```cpp
template<class S>
struct Particle{
    using Specs = S;
    Specs::Type Position[S::Dim];
    virtual void Print(){/*code*/}
};
```

## Derived Particles

The `Particle` class is derived to contain more data members

```cpp
template<class S>
struct Particle_Radius: Particle<S>{/*...*/};

template<class S>
struct Particle_MassVelocity: Particle<S>{/*...*/};
```

The `Particle_Radius` has an additional radius data member. `Particle_MassVelocity` has mass scalar and velocity array in addition to position. Both of them overwrite `Print` method.


## Concept

I created a `Derived` concept to be used for particle classes:
```cpp
template <class T, class U>
concept Derived = std::is_base_of<U, T>::value;
```

## Generic implementation

The `Block` class is there to create a contiguous array of the particle family. It prints their content by requesting it from the base `Particle` class which redirects the request to the right derived class: 

```cpp
template<class P> 
requires Derived<P,Particle<typename P::Specs>> // the concept
struct Block{
    vector<P> particles;
    
    //returns particle base class reference
    Particle<typename P::Specs>& Get(size_t i){return particles[i];}

    void print(){
        for (size_t i=0;i<particles.size();i++)
            Get(i).Print(); // polymorphic Print
    }
};
```

If `P<Specs>` is not derived from `Particle<Specs>`, the concept throws an error.


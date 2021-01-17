---
title: "How to use C++ namespace"
date: 2021-01-13T22:10:20+01:00
image: /images/island.jpg
imageQuality: "q65"
imageAnchor: "Center" # Smart, Center, TopLeft, Top, TopRight, Left, Right, BottomLeft, Bottom, BottomRight.
tags: ["C++"]
categories: "C++" 
summary: "I exaplain how namespaces can organize a large project and prevent name conflicts. "
---

## Introduction

With `namespace`, blocks of codes can be isolated in big projects, therefore name conflicts can be avoided.

## Basics

A namespace block can be defined as

```cpp
namespace A{
    class X{};
    class Y{};
} 
```
We can refer to `X` outside of namespace `A` with `::` operator

```cpp
namespace A{
    class X{};
    class Y{};
} 

A::X x; // Note :: operator
```
## Reveal content

We can reveal all the content to a scope with `using` directive:

```cpp
namespace People{
    class Employee{};
    class Manager{};
}
namespace Building{
    class Department{};
    class Room{};
} 

using namespace People; // all content of People are visible in the code below
using Building::Department; // only Department is visible in the code below

int main(){
  Employee e; // OK 
  Manager m; // OK

  Department d;
  // Room r; //Error: directly not accessible.

  return 0;
}
```


Names can be categorized to avoid conflicts

```cpp
namespace A{class Base{};} 
namespace B{class Base{};} 

int main(){

  A::Base baseA; // OK
  B::Base baseB; // OK

  // But they conflict if thrown out.
  using namespace A;
  using namespace B;
  Base base;// Error: which one, A::Base or B::Base?

  return 0;
}
```

## Namespace extension

A namespace can be **extended** with separated blocks, even in different files:

```cpp
// car.h
namespace Shop{class Car{};}  // Car class added to Shop namespace

// client.h
namespace Shop{class Client{};} // Client class also added to Shop namespace

// app.cpp
int main(){
    Shop::Car car;
    Shop::Client client;
    return 0;
}
```
## The global namespace

Any declaration outside of explicitly defined namespaces belong to the global namespace. To specifically access global namespace use `::SomeClass`. 

```cpp
namespace MyProject {
  class Person{public: double height;};
}
class Person{public: int age;};

using namespace MyProject; 

int main(){
    ::Person p; // OK, global Person is used. 
    p.age=30;
  return 0;
}
```

## Nested namespaces

We can have nested namespaces

```cpp
namespace App{
    namespace Shape{
        class Box{};
    }
} 
```

It is easier to write the above code as:

```cpp
namespace App::Shape{
    class Box{};
}

int main(){
    App::Shape::Box box; // Access nested parameter 
    return 0;
}
```
## Namespace aliases

```cpp
namespace Zoo::Animal::Birds{ class Penguin{};}

namespace ZAB = Zoo::Animal::Birds;
int main(){    
  ZAB::Penguin p;
  return 0;
}
```

## Namespace content

Everything, except the `main` function, can be declared/defined in a namespace: 

```cpp
namespace A{
  int x; 
  using mint = int;
  class person{};
  struct data{};
  void func(){};
  namespace B{/*more definitions*/};
} 

int main(){
  A::x = 10;
  A::mint j;
  A::person p;
  A::data d;
  A::func();
  return 0;
}
```


## How to use

The concept of the namespace is very similar to directories in the operating system. On our computer, we organize our files in folders: photos, videos, documents, and so forth. So, we quickly find them and also avoid file name collisions.

So my conventions are:


* For a new project, create a namespace with the name of the project. Everything is written in this namespace (except `main()`). So our project become portable, it can be included in other projects without the fear of name conflicts.

```cpp
namespace MyProject{
 class Particle{};
 class Motion{};
 class WriteOutput{};
}
```
* Each class is saved into two files: the header and implementation. Each class is contained in a namespace.

```cpp
// Particle.h
namespace MyProject {
  class Particle{
    public:void Move();
  };
}
// Particle.cpp
#include "Particle.h"
namespace MyProject{
  void Particle::Move (){
    std::cout<<"Particle is moving...";
  };
}
```
* Do not use `using` statement in headers, *.h* files. As they are added to different files, they inject their names which defeats the namespace purpose. But feel free to use them in *.cpp* files.

* If there are a few classes in a namespace, probably they don't need to be divided in new namespaces.

* However, sometimes, the name of classes make us to separate their namespace from start.

```cpp
namespace MyProject::Particle{
    class Base{};
    class Base2D{};
    class Base3D{};
}
namespace MyProject::Box{
    class Base{};
    class Base2D{};
    class Base3D{};
}
```

* The  namespaces hierarchy are the same as project directories. So the directories of previous examples are:

```
MyProject
|
|__Particle
|       |_Base.h
|       |_Base.cpp
|       |_ ...
|
|__Box
|   |_Base.h
|   |_Base.cpp
|   |_ ...
```

* When the number of classes in a namespace hits 10 or 20, maybe that's the time for creating new sub-namespaces.

```cpp
namespace MyProject{
    class Particle2D_Base{};
    class Particle2D_Point{};
    class Particle2D_Volume{};
    class Particle2D_Multi{};
    class Particle2D_variableRadius{};

    class Particle3D_Base{};
    class Particle3D_Point{};
    class Particle3D_Volume{};
    class Particle3D_Multi{};
    class Particle3D_variableRadius{};
}
```
The above design is changed to the below one:

```cpp
namespace MyProject::Particle2D{
    class Base{};
    class Point{};
    class Volume{};
    class Multi{};
    class variableRadius{};
}
namespace MyProject::Particle3D{
    class Base{};
    class Point{};
    class Volume{};
    class Multi{};
    class variableRadius{};
}
```


## References

[Isocpp](http://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rs-using-directive)
[microsoft docs](https://docs.microsoft.com/en-us/cpp/cpp/namespaces-cpp?view=msvc-160)
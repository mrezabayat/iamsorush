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
    int x;
    int y;
} 
```
We can refer to `x` outside of namespace `A`:

```cpp
namespace A{
    int x;
    int y;
} 

A::x = 5; // note :: operator
```

We can reveal all the content with `using` statement:

```cpp
namespace A{
    int x;
    int y;
} 

using namespace A; // all names of A passed to the code below
int main(){
  x = 5; 
  y = 7;
  return 0;
}
```


Names can be categorized to avoid conflicts

```cpp
namespace A{int x;} 
namespace B{int x;} 

int main(){

  B::x=10; // OK
  A::x=15; // OK

  // But they conflict if thrown out.
  using namespace A;
  using namespace B;
  x=98;// Error: which one, A::x or B::x?

  return 0;
}
```

A namespace can be **extended** with separated blocks

```cpp
namespace A{int x;} 

// some other codes

namespace A{int y;} // y also added to A, in addition to x

int main(){
    A::x = 10;
    A::y = 20;
    return 0;
}
```

We can have nested namespaces

```cpp
namespace A{
    namespace T{
        int m;
    }
} 
```

It is easier to write above code as:

```cpp
namespace A::T{
    int m;
}

int main(){
A::U::y = 5; // Access nested parameter 
return 0;
}
```
## What can goes into namespace

Everything except the `main` function: 

```cpp
namespace A{
  int x; 
  using mint = int;
  class person{};
  struct data{};
  void func(){};
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

The concept of namespace is very similar to directories in operating system. In our computer we organize our files to photos, videos, documents and so on. So, we quickly find them and also avoid file name conflicts.

So my conventions are:


0. For a new project, create a namespace with the name of the project. Everything is written in this namespace (except `main()`). So our project become portable, it can be included in other projects without the fear of name conflicts.

```cpp
namespace MyProject{
 class Particle{};
 class Motion{};
 class WriteOutput{};
}
```
1. Each class is saved into two files: the header and implementation. Each class is contained in a namespace.

```cpp
// Particle.h
namespace MyProject {
  class Particle{
    public:void Move();
  };
}
// Particle.cpp
namespace MyProject{
  void Particle::Move (){
    std::cout<<"Particle is moving...";
  };
}
```

2. If there are a few classes in a namespace, probably they don't need to be divided in new namespaces.

3. However, sometimes, the name of classes make us to separate their namespace from start.

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

4. The  namespaces hierarchy are the same as project directories. So the directories of previous examples are:

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

5. When the number of classes in a namespace hits 10 or 20, maybe that's the time for creating new sub-namespaces.

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




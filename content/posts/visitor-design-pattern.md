---
title: 'How visitor design pattern is useful for numerical programming?'
date: 2020-03-09T23:05:39Z
draft: false
image: /images/weopen.webp
thumbnail: /images/weopen_tn.webp
tags: ['Design Pattern']
categories: "Design"
---

## Introduction  

Visitor design pattern is separating operations from data storage. When the efficiency and memory consumption is not of concern this design pattern is not common. However, in numerical programming
it can be a game-changer.   

## Numerical Example

In most of numerical programs, we face a huge amount of data stored in arrays. For example, on a Cartesian grid we have 10⁶ points where each point contains below properties:

```cpp
class Point{
    public:
    double Density;
    double VelocityX;
    double VelocityY;
}
```

and we consume it in a vector

```cpp
vector<Point>(1e6)
```
so far so good. However, this data is supposed to be modified through some solvers or equations like

```cpp
Update Density => {
    Density = Alpha *(VelocityX+VelocityY)/2;
}
```
or an initializer

```cpp
Initialize Density ==> {
    Density = Beta*(x+y); // dependent to location
}
```

We cannot simply make this modifiers class members for three reasons: first we negate *single responsibility principle* for point class, second we cannot extend modifiers separately, and last but most important here, the point class needs to accommodate alpha and beta. So we would have 10⁶ of alpha and beta. As we add more modifiers they need more fields (properties).

## Solution

We keep point class the same. It is extended only based on its initial concept, e.g., `Point3d` would be a derived class with field `veclocityZ`.

`Point` implements just a method called `Accept`:

```cpp
class Point
{
    public:
    double Density;
    double VelocityX;
    double VelocityY;
    void Accept(IVisitor& visitor){
        visitor.Visit(this);
    }
}
```

A modifier needs to implement `IVisitor` abstract class (or interface):

```cpp
class IVisitor {
    public:
    void Visit(Point& point) =0
}
```

Now we can define modifiers:

```cpp
class DensityUpdater: public IVisitor
{
    public:
    double Alpha;
    void Visit(Point& point){
        point.Density = Alpha * (point.VelocityX + point.VelocityY) / 2;
    }
}
```

And another one

```cpp
class DensityInitializer: public IVisitor {
    public:
    double Beta;
    void Visit(Point& point){
        point.Density = Beta * (point.x + point.y);
    }
}
```

Now somewhere in a the code we can have

```cpp
DensityInitializer densityInitializer;
DensityInitializer.Beta = 1000.0;

DensityUpdater densityUpdater;
densityUpdater.Alpha = 0.5;

for(auto& point:points){
    point.Accept(densityInitializer);
}

// and somewhere else
for(auto& point:points){
    point.Accept(densityUpdater);
}
```

## Benefits

* Storage class (Point) is concerning itself not new modifiers,
* Modifiers not store data in storage class to be repeated numerously,
* Modifiers can have any shape and extend in any way independent of storage class (loosely coupled).

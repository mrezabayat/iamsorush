---
title: 'How Inversion of Control improves flexebility of numerical codes?'
date: 2020-03-14T22:00:00Z
draft: false
image: /images/ball.webp
thumbnail: /images/ball_tn.webp
tags: ['Design Pattern', 'Numerical Code', 'C Sharp']
categories: "Design"
---

## Introduction  

When programming it's very convenient to create `class A` which has a concrete member `class B`. However, this creates a tightly-coupled system since any change in B should be reflected in A. Inversion of control forces `class A` only uses abstract class/ interface of `B`, so we have a loosely-coupled system.

language: C#

## Numerical Example

Finding roots of functions are very common in numerical applications. In the below code, `Analysis` needs to find the pressure of a system using *Bisection* method:

```c#
class Bisection{
    public double Error;
    public double FindRoot(){ ... }
}

class Analysis{
    Analysis(){
        _bisection = new Bisection();
    }
    private Bisection _bisection;
    public void FindPressure(){
        return _bisection.FindRoot();
    }
    public void GetPressurePrecision(){
        return _bisection.Error;
    }
}
```

After some runs you notice *Bisection* is slow for some systems and you want to have a second option of *Secant* method. However, *Bisection* method is hard-coded in `Analysis` class. `FindRoot()` must be a member of `class Bisection` and `Error` is directly accessed.

 Probably, the first thing comes to mind is to create `SecantAnalysis` class which copies everything of `Analysis` class except Bisection member. Don't do that! do not deviate from *OOP* design to procedural programming.


## Solution

To make the classes loosely coupled we use an interface that *one implements and the other has as member*. We find the members and methods of `Bisection` that `Analysis` uses: `FindRoot()` and `Error`. We extract an interface for it:

```c#
interface IRootFinder{
    double Error {get; set;}
    double FindRoot();
}
```
We expect any root-finder algorithm provide these two features.  Please note, `Error` is now a property, i.e. wrapped in a getter and setter. Therefore, its accessibility can be modified in a concrete class.

Now lets re-write our classes

```c#
class Bisection : IRootFinder{
    public double Error {get{...} set{...}};
    public double FindRoot(){ ... }
}

class Analysis{
    Analysis(IRootFinder rootFinder){
        _rootFinder = rootFinder;
    }
    private IRootFinder _rootFinder;
    public void FindPressure(){
        return _rootFinder.FindRoot();
    }
    public void GetPressurePrecision(){
        return _rootFinder.Error;
    }
}
```

Now `class Analysis` is only dependent on an interface and doesn't know about concrete implementation of that interface. So we can say `Analysis` and `Bisection` are loosely coupled. The usage of `Analysis` is changed as a concrete root-finder needs to be injected in its constructor.

To show the flexibilities better let's create `Secant` class

```c#
class Secant : IRootFinder{
    public double Error {get{...} set{...}};
    public double FindRoot(){ ... }
}
```

For example, we know high pressure systems converge better with `Bisection` and low pressure systems work better with `Secant`:

```c#
HighPressureSystem = new Analysis(new Bisection);
var p = HighPressureSystem.FindPressure();
var err = HighPressureSystem.GetPressurePrecision();

LowPressureSystem = new Analysis(new Secant);
var p = LowPressureSystem.FindPressure();
var err = LowPressureSystem.GetPressurePrecision();
```

We have the same class of `Analysis` but injected different root-finders. We can define any number of root-finders without touching `class Analysis`.

## Conclusion

The idea keeps codes clean, extendable, and maintainable. Inversion of control can be used along with a factory class which creates the desired instance of RootFinder.

These are simplified examples, but the idea is easily applicable to more complex cases.

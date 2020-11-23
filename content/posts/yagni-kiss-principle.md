---
title: "Implementing YAGNI and KISS principle to have maintainable code"
date: 2020-05-03T21:04:57+01:00
draft: false
image: /images/chair.jpg
tags: ['Design Pattern']
categories: "Design"
---

After reading a lot of design patterns, loose-coupling ideas, and so, you cannot wait to implement all of them in the first program you are making. However, there must be a limit on usage of them. That’s when YAGNI and KISS principles shine.

## YAGNI

YAGNI stands for You Aren’t Gonna Need It. It is very tempting to keep commented codes or write methods which are not asked but we predict we will need them. For example, the total mass of particles in a system calculated like  

```c#
double totalMass = n * particle[0].Mass;
```
But later on you think it is better to be calculated like

```c#
double totalMass = 0.0;
for (int i=0;i<n;i++)
{
  totalMass += particle[i].Mass;
}
```

You are probably thinking "I comment the old line, I may need it later" but we know 99%  of times you don’t need it. You have seen commented codes which have been there for years and nobody dares to touch them. As a developer you must use a version control like Git, so you always have a copy of old code in the history of Git.  

There are times that you know the class you are designing needs to have specific properties and methods but you add more because there is a chance they will be useful. For example, you need to write a one-dimensional particle class like

```c#
public class Particle
{
    public double Mass {get; set;}
    public double Position {get; set;}
    public double  CalculateForce(Particle other)
    {
      return 6.673 * 10e-11 * Mass* other.Mass / Math.Abs(Position - other.Position);
    }
}
```

And that is job done. But you think “it is good to have a method that calculates acceleration from the interaction force, I probably use that later”, nope, you don’t need it. The job done, go to the next step, time is gold.

## KISS

KISS stands for “Keep It Simple, Stupid”. Simple is opposite to complex and entangled. The code you write should be easy to understand by others and yourself. You might work with other developers in a project, or at some point in future you hand over the code, in either case you don’t want to bother others much. Moreover, you may be busy on another project for a few months and you come back to your code and say “what the hell did I do here”. Being simple is subjective and relative to situations. However, there are few points that help you to keep a code simple.

1-	Do not purposefully make the design complex to show you are smart i.e. do not create puzzles. For example, instead of

```c#
for (int i=0;i<n;i++)
{
  totalMass += particle[i].Mass;
}
```

Do not write

```c#
for (int i=0;i<n;i=i+2)
{
  totalMass+=particle[i].Mass;
}
for (int i=1;i<n;i=i+2)
{
  totalMass+=particle[i].Mass;
}
```

2-	Avoid mega classes that do many unrelated tasks. Keep them focused using single responsibility principle (SRP).

3-	If possible keep methods less than 20 lines with a particular goal for SRP. For example, we have a big method like

```c#
public Void Run()
{
  // More code here

  for (int i=0;i<n;i++)
  {
    particle[i].Position += 0.5 * acceleration * time * time ;
  }

  double totalMass =0;
  for (int i=0;i<n;i++)
  {
    totalMass += particle[i].Mass;
  }

  // More codes here
}
```

We can change it to

```c#
public Void Run()
{
  // More code here

  UpdatePositions()
  var totalMass = CalculateTotalMass();

  // More codes here
}
```

But do not hide the mixup in another method like

```c#
public Void Run()
{
  // More code here
  var totalMass = UpdatePositionsAndCalculateTotalMass();
  // More codes here
}
```

The complexity is not solved in the above example, it is just swept under the carpet.

4-	Use interfaces and abstracts when needed. Design patterns recommend use of abstracts and interfaces but remember they came to existence to solve common problems of programming. If there is no problem, then YAGNI. For example, you have the below class

```c#
class Point
{
  private double X{get; set;}
  private double Y{get; set;}
  private double Z{get; set;}

  public double GetMagnitude()
  {
  	return Math.Sqrt(X*X + Y*Y + Z*Z);
  }
}
```

Let's assume that is all about it, and there is not any plan to extend Point class so why should you bother creating an interface for it where it adds complexity to the code. However, if from beginning we know there is a hierarchy of derived classes, then we would consider an interface.

5-	Try to inject/initialise an object’s dependencies, properties and fields when its constructor called.  Therefore, when you debug them, you know where to start.

6-	Avoid global variables (it's a C/C++ feature). They can be changed anywhere in the software and hard to track.

7-	Avoid as much as possible nested *if statements*. Each *if statement* creates different path for the application to run through, so it becomes harder for readers to follow. The exception to this is when there are several conditions in a method but all serve the same purpose, for example, when you check whether different parameters are null.

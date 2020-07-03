---
title: "Yagni Kiss Principle"
date: 2020-07-03T21:04:57+01:00
draft: true
---

You need to know YAGNI and KISS principle before numerical coding
After reading a lot of design patterns, loose-coupling ideas, and so, you cannot wait to implement all of them in the first program you are making. However, there must be a limit on usage of them. That’s when YAGNI and KISS principles shine.

YAGNI
YAGNI stands for You Aren’t Gonna Need It. It is very tempting to keep commented codes or write methods which are not asked but we predict we will need them. For example, the total mass of particles in a system calculated like
totalMass = n*p[0].Mass;
But later on you think it is better to be calculated like
totalMass =0.0;
For (int i=0;i<n;i++) { totalMass = n*p[0].Mass ; }
You probably thinking I comment the old line, I may need it later but we know 99%  of times you don’t need it. You have seen commented codes which have been there for years and nobody dares to touch them. As a developer you must use a version control like Git, so you always have a copy of old code in the history of Git.
There times that you know the class you are designing needs to have specific properties and methods but you add more because there is a chance they will be useful. For example, you need to write a one dimensional particle class like
Public Class Particle{
      Public double Mass {get; set;}
      Public double Position {get; set;}
      public   double  CalculateForce(Particle other){
      return 6.673 x 10-11 *Mass*other.Mass/Math.Abs(Position-other.Position)
}

And that is job done. But you think “it is good to have a method that calculates acceleration from the interaction force, I probably use that later”, nope, you don’t need it. The job done, go to the next step, time is gold.
KISS 
KISS stands for “Keep It Simple, Stupid”. Simple is opposite to complex and entangled. The code you write should be easy to understand by others and yourself. You might work with other developers in a project, or at some point in future you hand over the code, in either case you don’t want to bother others much. Moreover, you may be busy on another project for a few months and you come back to your code and say “what the hell I did here”. Being simple is subjective and relative to situations. But there are a few points that help you to keep a code simple.
1-	Do not purposefully make the design complex to show you are smart i.e. do not create puzzles. For example, instead of 
For (i=0;n<100;i++){
 totalMass+=particle[i].Mass;
}
Do not write
For (i=0;n<100;i=i+2){
totalMass+=particle[i].Mass;
}
For (i=1;n<100;i=i+2){
totalMass+=particle[i].Mass;
}
2-	Avoid mega classes that do many unrelated tasks. Keep them focused using single responsibility principle (SRP). 

3-	If possible keep methods less than 20 lines with a particular goal (single responsibility principle). For example, we have a big method like

Public Void Run(){
// More code here
For (i=0;n<100;i++){
particle[i].Position += 0.5*acceleration*time*time ;
}
TotalMass =0;
For (i=0;n<100;i++){
totalMass+=particle[i].Mass;
}
// More codes here
}

We can change it to

Public Void Run(){
// More code here
UpdatePositions()
totalMass = CalculateTotalMass();
}
// More codes here
}

But Do Not make another mixup like
Public Void Run(){
// More code here
TotalMass = UpdatePositionsAndCalculateTotalMass();
// More codes here
}
The complexity is not solved in the above example, it is just swept under the carpet.

4-	Use interfaces and abstracts when needed. Design patterns recommend use of abstracts and interfaces but remember they came to existence to solve common problems of programming. If there is no problem, then YAGNI. For example, you have the below class

Class Point{
private double X{get; set;}
private double Y{get; set;}
private double Z{get; set;}

Public double GetMagnitude{
	Return Math.Sqrt(X*X+Y*Y+Z*Z);
}
}

And that is all about it, and there is not any plan to extend it so why should you bother creating an interface for it where it adds complexity to the code. However, if from beginning we know there is a hierarchy of derived classes, then we would consider an Interface.

5-	Try to inject/initialize an object’s dependencies, properties and fields when its constructor called.  So, when you debug them, you know where to start.

6-	Avoid public variables. They can be changed anywhere in the software and hard to track.

7-	Avoid as much as possible nested IF conditions. Each IF condition means create different path for the application to run through, so becomes harder for a reader to follow. The exception to this is when there are several conditions in a method but all serve the same purpose, for example, when you check different parameters are not null and moreover 



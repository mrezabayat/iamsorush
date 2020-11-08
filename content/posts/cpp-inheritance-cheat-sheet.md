---
title: "C++ inheritance crash course"
date: 2020-10-03T19:37:36+01:00
image: /images/gold.webp
thumbnail: /images/gold_tn.webp
tags: ["C++"]
categories: "C++"
summary: "Inheritance is the mechanism that the attributes and methods of a base class are passed to a derived class. Here, all useful details of C++ inheritance are mentioned with examples. "
---
## Inheritance 

Inheritance is the mechanism that the attributes and methods of a base class are passed to a derived class. Here, all useful details of C++ inheritance are mentioned with examples. 

```cpp
class Base{
public:
    int i;
    void doSomething(){};
}
class Derived: public Base{}

Derived d;
d.i =10;
d.doSomething();
```

In the above example, `Derived` inherits `i` and `doSomething` from base class; 

## Public, protected and private inheritance

These specifiers modify the accessibility of inherited members as below


<table style="width:100%">
  <tr style="background-color:black; color:white">
    <th>Base member specifier</th>
    <th>Inheritance modifier</th>
    <th>Inherited member specifier</th>
  </tr>
  <tr style="background-color:#00C4CB">
    <td>public</td>
    <td rowspan=3>public</td>
    <td>public</td>
  </tr>
  <tr style="background-color:#00C4CB">
    <td>protected</td>
    <td>protected</td>
  </tr>
  <tr style="background-color:#00C4CB">
    <td>private</td>    
    <td>no access</td>
  </tr>
  <tr style="background-color:#FFFDD0">
    <td >public</td>
    <td rowspan=3>protected</td>
    <td>protected</td>
  </tr>
  <tr style="background-color:#FFFDD0">
    <td>protected</td>
    <td>protected</td>
  </tr>
  <tr style="background-color:#FFFDD0">
    <td>private</td>    
    <td>no access</td>
  </tr>
  <tr style="background-color:#486A47">
    <td>public</td>
    <td rowspan=3>private</td>
    <td>private</td>
  </tr>
  <tr style="background-color:#486A47">
    <td>protected</td>
    <td>private</td>
  </tr>
  <tr style="background-color:#486A47">
    <td>private</td>    
    <td>no access</td>
  </tr>
</table>

**Example**
```c++
class Base{
public:
  int x;
protected:
  int y;
private:
  int z;
};
class A: public Base{
  // Base members are accessible as
  // public x
  // protected y
  // no access to z
};
class B: protected Base{
  // Base members are accessible as
  // protected x
  // protected y
  // no access to z
};
class C: private Base{
  // Base members are accessible as
  // private x
  // private y
  // no access to z
};
```

- Access specifiers can be relaxer or more restricted when a method overridden in the derived class:

```c++
class Base{
private:
  virtual void DoSomething(){}
}

class Derived: public Base{
Public:
   void DoSomething() override {}
}

Base b;
Derived d;
b.DoSomething(); // Error, not accessible
d.DoSomething(); // OK
```
## Struct vs Class

`struct` inheritance is public by default, and `class` inheritance is private:
```cpp
class Base{};
class Derived: public Base{};
```
is similar to 

```cpp
struct Base{};
struct derived: Base{};
```


## Virtual Method
 Use `virtual` keyword to let the compiler know the method can be overridden in a future derived class. To complete overriding, use the keyword `override` in the derived class method:
 
 ```cpp 
 struct Base
{
    virtual void Move() {cout<<"I am Walking ...";}
};
struct Derived : Base
{
    void Move() override  {cout << "I am running" << std::endl;}
};

int main() {
    Base* b = new Derived();
    Derived* d = new Derived();
    b->Move(); // I am running
    d->Move(); // I am running
}
```
- If keyword `override` not used, no error will rise but polymorphic behaviour will be missing; in the above example, `b->Move()` would show `"I am walking ..."`.

## Interface (abstract class)

An interface mentions the methods of a class but not giving the details. In the example below, `ComputeArea` is a pure virtual function: no details of how it works is given, we only know its signature.  

```cpp
class Shape{
public:
    virtual double ComputeArea()=0
}
```
It expects derived classes define how they implement the methods.  

```cpp
class Circle: public Shape{
    double r;
    public:
    Circle(double _r):r(_r){}
    double ComputeArea() override {return 3.14*r*r}
}

class Square: public Shape{
    double s;
    public:
    Square(double _s):s(_s){}
    double ComputeArea() override {return s*s}
}
```

The interface cannot be used to create objects

```cpp
Shape s;  //Error
```

However, it can be used to create a generic piece of code that works with all different derived classes:

```cpp
void displayArea(Shape& shape){
      cout<<shape.ComputeArea();
}

Circle c(1.0);
Square s(1.0);

displayArea(c); // 3.14
displayArea(s); // 1.0
```

Interfaces can help to create loosely-coupled systems [see an example with C#](https://iamsorush.com/posts/ioc-and-numerical-programming/).

## Final class or method

A final class cannot be derived and a final method cannot be overridden. Use `final` keyword for this purpose:

```cpp
struct Base
{
     virtual void Move()  {cout<<"I am Walking ...";}
};
struct Derived final : Base
{
    virtual void Move() final override{cout << "I am running";}
};
struct Extended : Derived // Error
{
        void Move() override {cout<<"...";} //Error 
};
```
Making classes final increases the efficiency and safety of the code. 

## Order of constructors call in inheritance hierarchy

- If derived class constructor called, base default constructor is called first automatically (implicitly):

```c++
class Base{
  public:
  Base(){cout<<"Base called.";}
  Base(int j){cout<<"Parameter Base called.";}
};
class Derived: public Base{
  public: Derived(int j){cout<<"Derived called.";}
};
Derived d(0);
// Base called.  Derived called.
```

- To enforce call to parameterised constructor of the base class, it should be explicitly mentioned in
derived class constructor:

```c++
class Base{
  public:
  Base(){cout<<"Base called.";}
  Base(int j){cout<<"Parameterised Base called.";}
};
class Derived: public Base{
  public:
  Derived(int j):Base(j){cout<<"Derived called.";}
};
Derived d(0);
// Parameterised Base called.  Derived called.
```

- A virtual method, called in the constructor of the base class, will not be overridden when base constructor call is as a consequence of derived class construction.

```c++
class Base{
  public:
  Base(){cout<<"Base called."; Do();}
  virtual void Do(){cout<<"Base does something.";}
};
class Derived: public Base{
  public:
  Derived() {cout<<"Derived called.";}
  void Do() override {cout<<"Derived does something.";}
};

Derived d;

//Base called.  Base does something.  Derived called.
```

- In multiple inheritance, the base constructors are called in the order of appearance in class definition:

```c++
class Base1{
  public: Base1(){cout<<"Base1 called.";}
};
class Base2{
  public: Base2(){cout<<"Base2 called.";}
};

// The order below is important
class Derived: public Base1, public Base2 {
    public:
    Derived():Base2(),Base1(){} // Not here
};

Derived d; // Base1 called. Base2 called.   
```

## Order of destructors call in inheritance hierarchy

The opposite of of constructors.

## Multiple inheritance

- It can be used for merge feature classes to create a complex system.

- It can be done with the aid of interfaces (abstract classes) or implementations.

- Note some programming languages like C# only support multiple inheritance of interfaces but Not multiple inheritance of class implementations and they are successful.

- Example of multiple inheritance of interfaces:

```c++
struct IMotion {
	virtual void Walk() = 0;
};

struct ISpeech {
	virtual void Talk() = 0;
};

struct Robot : IMotion, ISpeech {
  void Walk() override {cout<<"Robot is walking... ";}
  void Talk() override {cout<<"Robot is talking... ";}
};

// Anything with interface of ISpeech accepted
void SpeechPlayer(ISpeech& speech){
  cout<< "playing the speech: ";
  speech.Talk();
}

int main(){
Robot robot;
SpeechPlayer(robot);}

```

- An example of multiple inheritance of implementations:

```cpp
struct Motion {
	void Walk() {cout<<"Walking ...";};
};

struct Speech {
	void Talk()  {cout<<"Talking ... \n";}
};

struct Robot : Motion, Speech { };

int main(){
  Robot r;
  r.Walk(); // Walking ...
  r.Talk(); // Talking ...
}
```

- An example of multiple inheritance of implementations with interface:

```c++
struct IMotion {
	virtual void Walk() = 0;
};

struct Motion: IMotion {
	void Walk() {cout<<"Walking ...";};
};

struct ISpeech {
	virtual void Talk() = 0;
};

struct Speech : ISpeech{
	void Talk()  {cout<<"Talking ... \n";}
};

struct Robot : Motion, Speech { };

void SpeechPlayer(ISpeech& speech){
  cout<< "playing the speech: ";
  speech.Talk();
}

int main(){
  Robot robot;
  SpeechPlayer(robot);
}
```

- Multiple inheritance can be used instead of Bridge design pattern if fine grain control over mixing classes needed.
Bridge Design:

```c++
struct IMotion {
	virtual void Move() = 0;
};

struct TwoLegs: IMotion {
	 void Move() {cout<<"Two-leg robot moving ... \n";};
};
struct FourLegs: IMotion {
	 void Move() {cout<<"Four-leg robot moving ...";};
};

struct CommunicatingRobot {    
    CommunicatingRobot(IMotion* motion):_motion(motion){}
    void Move(){ _motion->Move();}
    virtual void Communicate() = 0;
    private:
    IMotion* _motion;
};

struct TalkingRobot: CommunicatingRobot{
    TalkingRobot(IMotion* motion):CommunicatingRobot(motion){}
    void Communicate(){cout<<"Talking ...";}
};

struct DisplayRobot: CommunicatingRobot{
    DisplayRobot(IMotion* motion):CommunicatingRobot(motion){}
    void Communicate(){cout<<"Display ...";}
};


int main(){
  TalkingRobot twoLegTalkingRobot(new TwoLegs());
  TalkingRobot fourLegTalkingRobot(new FourLegs());
  DisplayRobot twoLegDisplayRobot(new TwoLegs());
  DisplayRobot fourLegDisplayRobot(new FourLegs());
  twoLegTalkingRobot.Move();//Two-leg robot moving ...
  twoLegTalkingRobot.Communicate(); // Talking ...
}
```

Above example using multiple inheritance

```cpp
struct IMotion {
	virtual void Move() = 0;
};

struct TwoLegs: IMotion {
	 virtual void Move() {cout<<"Two-leg robot moving ... \n";};
};
struct FourLegs: IMotion {
	 virtual void Move() {cout<<"Four-leg robot moving ...";};
};

struct ICommunicatingRobot {    
    virtual void Communicate() = 0;
};

struct TalkingRobot: ICommunicatingRobot{
    virtual void Communicate(){cout<<"Talking ...";}
};

struct DisplayRobot: ICommunicatingRobot{
    virtual void Communicate(){cout<<"Display ...";}
};

struct TwoLegTalkingRobot: TwoLegs, TalkingRobot {/* specific methods for this composition */};
struct FourLegTalkingRobot: FourLegs, TalkingRobot {/* specific methods for this composition */};
struct TwoLegDisplayRobot: TwoLegs, DisplayRobot {/* specific methods for this composition */};
struct FourLegDisplayRobot: FourLegs, DisplayRobot {/* specific methods for this composition */};

int main(){
  TwoLegTalkingRobot robo;
  robo.Move();//Two-leg robot moving ...
  robo.Communicate(); // Talking ...
}
```

## Dreaded diamond

To explain this, lets look at below example:

```cpp
struct Base{ int i;};
struct D1: Base {};
struct D2: Base {};
struct Target: D1, D2 {};

int main(){
Target  t;
t.i = 1; // Error: request for member ‘i’ is ambiguous 
}
```

The multiple inhertance graph of the example above is shown below .   
```
    Base    
     /\
    /  \
 D1     D2
    \  /
     \/
   Target
 ```
 
 D1 and D2 pass two copy of Base to target. So when `i` is called the compiler cannot figure out which copy to call. To avoid this, use keyword `virtual` in definition of D1 and D2, therefore, only one copy of Base is passed to Target:

```cpp
struct Base{ int i;};
struct D1: virtual Base {};
struct D2: virtual Base {};
struct Target: D1, D2 {};

int main(){
Target  t;
t.i = 1; // works fine :)
}
```
     
## Hiding rule

A method in derived class aims to overload a method of base class does not happen automatically. The compiler only looks in the scope of derived class for overloading. In this case the base method should be explicitely mentioned in the derived class, see below example:

```cpp
struct Base
{
    virtual void f(int i){cout<<"integer function called.";}
};
struct Derived : Base
{
    void f(double x){cout<<"double function called.";}
};

struct OverloadingDerived : Base
{
    using Base::f; // Let compiler consider base method for overloading
    void f(double x){cout<<"double function called.";}
};
 

int main() {
    Derived d;
    int j = 1;
    double x = 0.0;
    d.f(j); // double function called. :( 
    d.f(x); // double function called.

    OverloadingDerived o;
    o.f(j); //integer function called.
    o.f(x); //double function called.
}
```

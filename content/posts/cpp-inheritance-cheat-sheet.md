---
title: "C++ inheritance cheat sheet "
date: 2020-10-03T19:37:36+01:00
draft: true
image: /images/bird.webp
thumbnail: /images/bird_tn.webp
tags: ["C++"]
---

## Public, protected and private inheritance

These specifiers modify accessibility of inherited members as below


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

- Access specifiers can be relaxer or restricter when a method overridden in the derived class:

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

## Order of constructor call in inheritance hierarchy

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

- To enforce call to parameterised constructor of base class, it should be explicitly mentioned in
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

- A virtual method, called in constructor of base class, will not be overridden when base constructor call is as a consequence of derived class construction.

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

- Multiple inheritance can be a good alternative to Bridge design pattern.
Bridge Design:

```c++
struct IMotion {
	virtual void Move() = 0;
};

struct Run: IMotion {
	 void Move() {cout<<"running ... \n";};
};
struct Walk: IMotion {
	 void Move() {cout<<"walking ...";};
};

struct Robot {
    Robot(IMotion* motion):_motion(motion){}
    void Move(){ _motion->Move();}
    private:
    IMotion* _motion;
};


int main(){
  Robot fastRobot(new Run());
  Robot slowRobot(new Walk());
  fastRobot.Move(); // running ...
  slowRobot.Move(); // walking ...
}
```

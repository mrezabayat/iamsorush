---
title: 'What is "object slicing" trap in C++?'
date: 2020-02-26T20:05:39Z
draft: false
image: /images/lemon.jpg
tags: ['C++']
categories: "C++"
---
Every now and then, I switch programming language from C# to C++, I fall in the trap of object slicing. It happens when a derived object is assigned by value to a base object where the extra information in the derived object is scrapped for worst. This is not happening in C#. Let see an example<br/>

```cpp
class A{
public:
    virtual void Say(){
        std::cout<<"I am A"<<std::endl;
    }
};

class B: public A{
public:
    void Say() override{
        std::cout<<"I am B"<<std::endl;
    }
};

int main(){
   B b;
   A a1;
   A a2=b;

   b.Say(); // I am B
   a1.Say(); // I am A
   a2.Say(); // I am A   why???
}
```

B (object `b`) is derived from A (object `a1` and `a2`). `b` and `a1`, as we expect, call their member function. But from polymorphism viewpoint I don't expect `a2`, which is assigned by `b`, to  not be overridden. Basically, `a2` only saves `A`-class part of `b` and that is object slicing in C++.<br/>


Another common situation is when you pass an object to a function:<br/>

```c++
class C{
public:
    C(A a){
        obj = a;
    }
    A obj;

};

int main(){
   A a;
   B b;
   C c1(a);
   C c2(b);

   c1.obj.Say(); // I am A
   c2.obj.Say(); // I am A
}
```

In the above example, C has a class A member in the hope that it stores all the objects with a class derived from A. But Nope! object c2 initialised its obj member with b and only A part of it passed.<br/>

To avoid this problem, the assignment should be by reference or pointer. In the first example change as below<br/>

 ```c++   
  A& a2=b;
  a2.Say(); // I am B
 ```
And in the second example <br/>

```cpp
class C{
public:
    C(A* a){
        obj = a;
    }
    A* obj;
};

int main(){
   A a;
   B b;
   C c1(&a);
   C c2(&b);

   c1.obj->Say(); // I am A
   c2.obj->Say(); // I am B
}
```

Solved. Alternatively, I could use a pointer in the first example and reference member in the second example. <br/>

I should note that in C# assignments are by reference automatically; maybe that's why we don't see object slicing in C#. <br/>

If you are interested to have pointer/reference on assignment by value as well, have a look at this [article](https://www.modernescpp.com/index.php/c-core-guidelines-copy-and-move-rules).<br/>

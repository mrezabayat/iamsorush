---
title: "Is C++ static polymorphism useful?"
date: 2021-02-28T17:10:20+01:00
image: /images/boat.jpg
imageQuality: "q65"
imageAnchor: "Center" 
tags: ["C++", "OOP"]
categories: "C++" 
summary: "With examples, I explain static vs dynamic polymorphism. I show that static one limits the flexibility of the program at runtime. However, it can improve the performance of the code whose behaviour can be resolved at compile-time."
---

## Introduction

The short answer is: if all the benefits of polymorphism are used to the point that the program is compiled then static polymorphism
can relatively improve the performance of the program. However, in many cases, it is a layer of complexity to the code design that better be avoided.

The long answer as follows. I start with dynamic polymorphism which is more commonplace. Then the difference between static and dynamic polymorphism is explained. And finally, I talk 
about where static polymorphism is useful and where is not.

## Dynamic polymorphism

In OOP, dynamic polymorphism or polymorphism is to seclude a behaviour in a system that can proceed in different ways (or branches). We define each branch in a new class. For example in a geometry app, all shapes have an area but the calculation is different:

```cpp
struct Shape{
    virtual double CalculateArea()=0;
};
```

Then we can branch the behaviour

```cpp
struct Circle: Shape{
    double radius;
    Circle(double r):radius(r){}
    double CalculateArea() override {
        return 3.14*radius*radius;
    }
};

struct Square: Shape{
    double side;
    Square(double s):side(s){}
    double CalculateArea() override {
        return side*side;
    }
    
};
```

We can have 3D object, `Part`, with the different shapes as cross-section:

```cpp
struct Part{
    double height;
    Shape* shape;
    Part(double h):
        height(h), shape(nullptr){}
    double CalculateVolume(){
        return height*shape->CalculateArea();
    }    
};
```

A `Part` object can work with any shape. It doesn't care about the details of a shape:


```cpp
int main(){

// initialization
Square square{1.0};
Circle circle{1.0};
Part part{10.0};


while(true){
    
    // Change shape
    int option = 0 ;
    cout << "Choose Part: (1) cylinder (2) Box 
             (0) Exit program"<<endl;

    cin >> option;

    if (option==1)
        part.shape = &circle;
    else if (option==2)
        part.shape = &square;
    else if (option==0)
        return 0;
    else 
        throw runtime_error("Option not defined!");
    
    // Actions on part
    cout<< "Part Volume is:"<<
        part.CalculateVolume()<<endl;
}
return 0;
}
```

In the example above, the `part.shape` is changed by users during **runtime** without `part` being destroyed. The `part` initialization
and actions are not touched. That is the main advantage of dynamic polymorphism:  there is no if-condition to change the path of the software at initialization and actions. 

The example roughly resembles a combo box in an app with GUI. While the program is running, the user selects
an option of combo-box and observes a box turns to a cylinder.

Note that it is not only user interactions that change the dynamic behaviour of a problem. There are also situations that the code
is intelligent enough to decide a change of behaviour based on some criteria. For example, in a stock market app, the code dynamically changes forecast equations at different transaction levels. In a physics app, if the temperature around a solid particle goes beyond the melting point, the particle melts and follows liquid behaviour.


## Static polymorphism

The static polymorphism is defined as:

```cpp
template <class T> 
struct Base
{
    void DoSomething()
    {
        static_cast<T*>(this)-> DoSomethingSpecial();
    }
};

struct Derived : Base<Derived>
{
    void DoSomethingSpecial();
};

```
The `static_cast` makes sure the right behavior, `DoSomethingSpecial()`, is selected at **compile-time**. The selected behaviour can not be changed during runtime.


Let's re-code the previous example in static polymorphisim:


```cpp
template <class T> 
struct Shape{
    double GetArea(){
        return static_cast<T*>(this)
            -> CalculateArea();
    }
};

struct Circle: Shape<Circle>{
    double radius;
    Circle(double r):radius(r){}
    double CalculateArea() {
        return 3.14*radius*radius;
    }
};

struct Square: Shape<Square>{
    double side;
    Square(double s):side(s){}
    double CalculateArea() {
        return side*side;
    }
};

template<class T>
struct Part{
    double height;
    Shape<T>* shape;
    Part(double h):
        height(h), shape(nullptr){}
    double CalculateVolume(){
        return height*shape->GetArea();
    }    
};

```

So far the code is not that different from the dynamic example. I implement this one in a similar scenario:

```cpp
int main(){

// initialization
Square square{1.0};
Circle circle{1.0};

Part<Circle> partC{10.0};
partC.shape = &circle;
Part<Square> partS{10.0};
partS.shape = &square;

while(true){

    uint option=0;
    cout << "Choose Part: (1) cylinder (2) Box 
             (0) Exit program"<<endl;
    cin >> option;

    if (option==0)
        return 0;
    if (option>2) 
        throw runtime_error("Option not defined!");
    
    // Actions on part
    cout<< "Part Volume is:";

    if (option==1)
            cout<<partC.CalculateVolume()<<endl;
    else if (option==2)
            cout<<partS.CalculateVolume()<<endl; 
    
}
return 0;
}
```

As you see, we can write `Part` with different behaviours` Part<Circle>`, `Part<Square>` and so on. However, they are hard-coded at runtime i.e. we cannot transform
`Part<Circle>` to `Part<Square>` because at runtime as they are two different animals. 
Now we have to have two `Part` objects everywhere, or we have to destruct one and create another at the user's request. Moreover, the if-conditions are penetrated
into actions of `part`. 

## Proper usage

The static polymorphism should be used where there is no change of behaviour after compile-time. Therefore, if the code is an app that is compiled once and given to end-users to just run it, then, it is quite challenging to find a good place for static polymorphism. But if the app complies with every run, there are more possibilities for applying the idea.

So in the shape example, if the end-user at the beginning knows they need `Part<Square>` for the whole calculations, they compile the simple code below and run it once:

```cpp
int main(){

// initialization
Square square{1.0};
Part<Square> partS{10.0};
partS.shape = &square;
    
// Actions on part
cout<< "Part Volume is:"
    << partS.CalculateVolume() <<endl; 
    
return 0;
}
```

## Then Why?

So if the static polymorphism is limiting like that why do we bother using it when we have the dynamic one?  because of Performance. The dynamic polymorphism is slower because

* There is an overhead in dynamically finding the right implementation at runtime. The class points to a *vtable* which finds the right function to be called.

* The details of polymorphic functions are hidden from the compiler, so it cannot optimise the caller context with regard to the function.

To use static polymorphism, it should be somehow proven to developers that the above points are the bottleneck for a high-performance program.
Even then, we have to ask ourselves is worth it dumping sweet flexibility and easy maintenance of a dynamic polymorphism code.



















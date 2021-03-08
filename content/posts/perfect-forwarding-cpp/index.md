---
title: "An overview of C++ perfect forwarding"
date: 2021-03-07T19:07:21+01:00
image: /images/pizzadelivery.jpg
imageQuality: "q65"
imageAnchor: "Center" 
tags: ["C++"]
categories: "C++" 
summary: "With a simple example, it is demonstrated that how perfect forwarding can keep rvalueness of a function's parameters. The universal reference is also discussed."
---

## Intro

Perfect forwarding is when a wrapper function passes lvalueness/ravlueness of its arguments to a wrapped function. To do so `std::forward` is used:

```cpp
#include <iostream>
using namespace std;

void Display(int& i){
    cout<< i<<" int&"<<endl;
}

void Display(int&& i){
    cout<< i<<" int&& called"<<endl;
}

template<class T>
void DisplayWrapper(T&& t){
    Display(forward<T>(t));
}

int main(){

    int x=5;
    
    DisplayWrapper(5); // int&& called
    DisplayWrapper(x); // int&

return 0;}
```

In the above example, `DisplayWrapper` passes prvalue, `5`, and lvalue `x` to the correct overload of `Display`. This desired behaviour is conducted with `std::forward`. 
For more details read the following sections.

Here I assume, you are familiar with lvalue, rvalue, rvalue reference and `std::move`. If not, I recommend google them or have a quick look at my post [here](https://iamsorush.com/posts/move-semantics-cpp/) where I briefly explained them all together. 

## Problem

If we run the above example without `std::forward`, we have:

```cpp
template<class T>
void DisplayWrapper(T&& t){
    Display(t);
}
```
The outcome will be:

```cpp
DisplayWrapper(5); // 5 int&
DisplayWrapper(x); // 5 int&
```

So `DisplayWrapper` doesn't pass `5` as a prvalue to `Display` function but as an lvalue. 

## Overloading

Let's only focus on `Display` functions, and see which overload is selected with different parameters:

```cpp
#include <iostream>
using namespace std;

void Display(int& i){
    cout<< i<<" int& called"<<endl;
}

void Display(int&& i){
    cout<< i<<" int&& called"<<endl;
}

int main(){

    int x=5;
    int&& y=10;
    
    Display(5); // int&& called
    Display(move(y)); // int&& called
    Display(move(x)); // int&& called
    
    Display(x); // int& called
    Display(y); // int& called

    return 0;
}
```

To sum it up:

* if we pass an lvalue:  `x` and `y`, the first overload is called,  
* if we pass an rvalue: prvalue (`5`) and xvalue (`move(x)` and `move(y)`), the second overload is called.

Note that `y` is a named rvalue reference, so it is an lvalue. On the other hand, the outcome of `std::move` is an unnamed rvalue reference, therefore, it's 
an rvalue (or technically xvalue).  



## Universal reference

In a function with template parameter `T`, the argument `T&&` is called universal reference as **it can be lvalue reference or rvalue reference**.

```cpp
void Display(int& i){
    cout<< i<<" int& called"<<endl;
}
void Display(int&& i){
    cout<< i<<" int&& called"<<endl;
}
template<class T>
void DisplayWrapper(T&& t){
    Display(t);
}
int main(){

    int x=5;
    DisplayWrapper(x); // line 1
    DisplayWrapper(5); // line 2

    return 0;
}
```

So at line 1, `t` can bind to `x`, then it has the type of `int&`, lvalue reference. At line 2, `t` bind to `5` and its type is `int&&`, rvalue reference. 

When passing `t` to `Display`, in the first case the correct overload
 `Display(int& )` is called. In the second case, still the same overload is called because `t` in any case is an lvalue (it has a name and address). So somehow, we lost the rvalueness of `5` within `DisplayWrapper`. 


 ## Solution

 To ensure that an rvalue in outer scope is still an rvalue inside the wrapper function, we apply `std::forward` on the universal reference (see the first example in the Intro section). All in all, `std::forward` forwards an lvalue as lvalue and an rvalue as rvalue.


 ## Details 

The universal reference has only the form of `T&&` where `T` is a template type. Therefore, `vector<T>&&`, `const T&&`, `MyClass<T>&&` are not universal references, they are rvalue references.

Moreover, for `T&&` to be a universal reference, `T` must be deduced by the function call, not class instansiation:

```cpp
template<class T>
struct A {
    void DoIt(T&& t){};
}

A<int> a; // T is decided.
```
Now a call to `a.DoIt` is like

```cpp
void DoIt(int&& t){}
```

which is not a universal reference.


I feel for everyday coding the info here is enough on the subject, but there are a lot of details. If you are interested, start from references down here. 




## References

[Scott Meyers on Isocpp](https://isocpp.org/blog/2012/11/universal-references-in-c11-scott-meyers)
[Modernes C++](https://www.modernescpp.com/index.php/perfect-forwarding)
[cppreference](https://en.cppreference.com/w/cpp/utility/forward)




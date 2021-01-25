---
title: "C++ Concepts and constraints clear up templates"
date: 2021-01-24T18:10:20+01:00
image: /images/fence.jpg
imageQuality: "q65"
imageAnchor: "Center" # Smart, Center, TopLeft, Top, TopRight, Left, Right, BottomLeft, Bottom, BottomRight.
tags: ["Back-End Web", "C Sharp",".Net Core"]
categories: "C++" 
summary: "With examples, C++ concepts are used to constrain template classes and functions. It is shown that concepts improve the readability of code and facilitate finding bugs."
---

## Introduction

A *C++ 20* concept is a named predicate that constrains templates. It improves the readability of code and facilitates finding bugs. Concepts can also be used for function overloading. 

## Why Concepts?

Concepts make a template code easy to read and help to find bugs. 

In the example below, it is not clear what `T` is unless you read the whole function. The function works well with arrays. But let's, instead of an array, pass a wrong object to the function:
 
```cpp
#include<iostream>

template<class T>
double sum(T& items){
    double sum=0;
    for (auto& item:items)
        sum+=item;
    return sum;
}
 
class A{};

int main(){
    A a;
    auto c = sum(a);
}

```

Look at the errors, it takes a bit of time to decipher: 

```bash
<source>: In instantiation of 'double sum(T) [with T = A]':
<source>:15:19:   required from here
<source>:6:5: error: 'begin' was not declared in this scope; did you mean 'std::begin'?
    6 |     for (auto& item:items)
      |     ^~~
      |     std::begin
In file included from /opt/compiler-explorer/gcc-10.2.0/include/c++/10.2.0/string:54,
                 from /opt/compiler-explorer/gcc-10.2.0/include/c++/10.2.0/bits/locale_classes.h:40,
                 from /opt/compiler-explorer/gcc-10.2.0/include/c++/10.2.0/bits/ios_base.h:41,
                 from /opt/compiler-explorer/gcc-10.2.0/include/c++/10.2.0/ios:42,
                 from /opt/compiler-explorer/gcc-10.2.0/include/c++/10.2.0/ostream:38,
                 from /opt/compiler-explorer/gcc-10.2.0/include/c++/10.2.0/iostream:39,
                 from <source>:1:
/opt/compiler-explorer/gcc-10.2.0/include/c++/10.2.0/bits/range_access.h:108:37: note: 'std::begin' declared here
  108 |   template<typename _Tp> const _Tp* begin(const valarray<_Tp>&);
      |                                     ^~~~~
<source>:6:5: error: 'end' was not declared in this scope; did you mean 'std::end'?
    6 |     for (auto& item:items)
      |     ^~~
      |     std::end
In file included from /opt/compiler-explorer/gcc-10.2.0/include/c++/10.2.0/string:54,
                 from /opt/compiler-explorer/gcc-10.2.0/include/c++/10.2.0/bits/locale_classes.h:40,
                 from /opt/compiler-explorer/gcc-10.2.0/include/c++/10.2.0/bits/ios_base.h:41,
                 from /opt/compiler-explorer/gcc-10.2.0/include/c++/10.2.0/ios:42,
                 from /opt/compiler-explorer/gcc-10.2.0/include/c++/10.2.0/ostream:38,
                 from /opt/compiler-explorer/gcc-10.2.0/include/c++/10.2.0/iostream:39,
                 from <source>:1:
/opt/compiler-explorer/gcc-10.2.0/include/c++/10.2.0/bits/range_access.h:110:37: note: 'std::end' declared here
  110 |   template<typename _Tp> const _Tp* end(const valarray<_Tp>&);
      |                                     ^~~
Compiler returned: 1

```

The errors become even more entangled when something goes wrong in nested class templates.  

## Definition

Here, `Array` concept is defined to tell the user of this code that `T` should be an array:

```cpp
#include<iostream>

template<class U>
concept Array = std::is_array<U>::value;

template<Array T> // Note Array concept
double sum(T& items){
    double sum=0;
    for (auto& item:items)
        sum+=item;
    return sum;
}
```

There are many useful structs like `is_array` in `type_traits` header which can be used for defining a concept.

Again we injected the wrong parameter into the `sum` function:

```cpp 
class A{};

int main(){
    A a;
    int b[2]={1,2}; // b is the right input for sum()
    std::cout<<sum(a);
}
```
Now let's check the errors, they diretly point out that `a` is no an array:

```bash
: In function 'int main()':
:19:21: error: use of function 'double sum(T&) [with T = A]' with unsatisfied constraints
   19 |     std::cout<<sum(a);
      |                     ^
:7:8: note: declared here
    7 | double sum(T& items){
      |        ^~~
:7:8: note: constraints not satisfied
: In instantiation of 'double sum(T&) [with T = A]':
:19:21:   required from here
:4:9:   required for the satisfaction of 'Array<T>' [with T = A]
:4:35: note: the expression 'std::is_array< <template-parameter-1-1> >::value [with <template-parameter-1-1> = A]' evaluated to 'false'
    4 | concept Array = std::is_array<U>::value;
      |                                   ^~~~~

```

##  Concepts and constraints 

Two constraints can create conjunction with `&&` operator where both must be true

```cpp
template<class T> 
concept ConstInt = std::is_const<T>::value && std::is_integer<T>::value;

template<ConstInt T>
void f(T a){};
```

Note that If `is_const<T>::value` is false, `is_integer` term is ignored.

Disjunction can be created with `||` operator where either constraint can be true

```cpp
template<class T>
concept Arithmetic =  std::is_integral<T>::value || std::is_floating_point<T>::value;
```

Constraints can be created with other concepts:

```cpp
template<class T>
concept ConstArithmetic = Arithmetic && is_const<T>::value;
```

Before defining your concepts, it is worth checking already defined concepts in the `<concepts>` header. 

## Requires clause

Instead of imposing a concept in template brackets,
```cpp
template<Arithmetic T> 
void f(T a){/*function definition*/};
```

we can enforce it just after template declaration using `requires`:

```cpp
template<class T> 
requires Arithmetic<T>
void f(T a){/*function definition*/};
```
or after function declaration

```cpp
#include<concepts>
template<class T>
void f(T a) requires integral<T> // integral is in header <concepts>	
{/*function definition*/}; 
```

## Requires expressions

If working with type traits is hard, we can explain what we expect from a type with an object of that type:

```cpp
template<class T>
concept Vector = requires (T a){ 
    a.size(); // constraint #1
    a.push_back(0); // constraint #2
};

template<Vector T> // use the concept
class Box{}; 
```
So users get errors if a `Box` object is created that violates constraints #1 and #2.


Constraints can be imposed on types too

```cpp
template<class T>
concept MyArray = requires (T a){ 
    a[0]; // Accessing elements through [] works.
    a.size(); // a must have size() method.
    typename T::Type; // T must contain a datatype, Type.
};

template<MyArray T>
void DisplayArray(T x){
    
    typename x::Type sample;
    std::cout<<sample;
    for (size_t i=0;i<x.size();i++)
        std::cout<<x[i]<<" ";

}
```

## Compounds

The `requires` expression can constrain the return type of its statements

```cpp
template<class T>
concept AddableInt = requires (T a){
    { a + a } -> std::same_as<int>;
}
```
The above concept impose two constraints:

* `a+a` must be valid.
* `decltype(a+a)` must be the same as `int`.

Note that `same_as` is defined in the <concepts> header.

We can have multiple expressions:

```cpp
template<class T>
concept MyPointer = requires (T a){
    { *a + 1} -> std::convertible_to<MyBaseClass>;
    { a->sum()} -> std::same_as<double>;
};
```









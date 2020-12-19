---
title: "How and where to use C++ templates"
date: 2020-10-30T19:34:31+01:00
image: /images/hive.jpg
tags: ["C++", "Template"]
categories: "C++"
summary: "Using templates in C++, you can create functions or classes having similar behaviors for different types. Here, all the useful features of templates are explained with examples."
---

## Template

Using templates in C++, you can create functions or classes having similar behaviors for different types. Here, all the useful features of templates are explained with examples.

## Class Template

A class can use a generic type which can be any of `int`, `double`, `string`, and so on.

```cpp
template<class T>
class Array{
    T* data;
    public:
    Array(size_t size)
    {
        data = new T[size];
    }
    ~Array(){delete[] data;}
    T& operator[] (size_t i)
    {
        return data[i];
    }
};
```
`Array` can be used as an integer or string class:

```cpp
int main()
{
  Array<int> a(5);
  a[0] = 1;
  std::cout<< a[0] << std::endl;
  
  Array<std::string> b(5);
  b[0] = "Hello";
  std::cout<< b[0]  << std::endl;
}
```

## Function template

A function can be dependent on a generic type

```cpp
template<class T>
T Min(T a, T b){
  return a>=b?b:a;
}

int main()
{
  int a=2;
  int b=4;
  char x = 'h';
  char y = 'H';
  std::cout<< Min(a,b) << std::endl;// 2
  std::cout<< Min(x,y) << std::endl; // H has lower ASCII value 
}
```

Another useful example is the swap function:

```cpp
template<class T>
void Swap(T& a, T& b){
    auto tmp = a;
    a = b;
    b = tmp;  
}

int main()
{
    int a =0;
    int b =1;
    Swap(a,b);
    std::cout<< a << b << std::endl; // 10
    
    std::string x ="Hi ";
    std::string y ="Hello ";
    Swap(x,y);
    std::cout<< x << y << std::endl; // Hello Hi
}
```

## Call function template explicitly

In the previous examples, compiler figures type `T` out. But it gets confused for this case:

```cpp
int main()
{
  int a=2;
  double b=4;
  std::cout<< Min(a,b) << std::endl; // Error: T is int or double?
}
```
To solve this, template type needs to be mentioned explicitly:

```cpp
std::cout<< Min<int>(a,b) << std::endl;
```

Another example that the compiler cannot figure out the type is:

```cpp
template<class T>
void MyCast(double d){
    T a = (T) d;
    std::cout<< a << std::endl;
}

int main()
{
  MyCast(2.3); // Error: So what is T?
  MyCast<int>(2.3); // 2  OK, T is int.
}
```

## Template specialization

Sometimes the details of a template class/function need to be special for a type. For example, we define a special calculation for type `string` of `Min` function: 

```cpp
template<class T>
T Min(T a, T b){
  return a>=b?b:a;
}

template<>
string Min<string>(string a, string b){
    auto m = a.length();
    auto n = b.length();
    return    m>=n?b:a;
}

int main()
{
  int a=2;
  int b=4;
  string x = "Hello";
  string y = "Hi";
  std::cout<< Min(a,b) << std::endl;// 2
  std::cout<< Min(x,y) << std::endl; // Hi
}
```

## Definition & declaration files

It's a good practice to separate a class definition (implementation) file from its declaration file. However, the problem with a template class is that compiler creates  a specific class for a type only when it sees a template specialization or class instantiation of a template. 

```cpp

//file sample.h
template<class T>
struct Sample
{
	T Compute();
};

//file sample.cpp
#include "sample.h"

template<class T>
T Sample<T>::Compute(){

	return T();
}

//file main.cpp
#include "sample.h"
using namespace std;

int main()
{
	Sample<int> s;
	
	std::cout << s.Compute();
	return 0;
}

```

*sample.cpp* successfully compiles to sample.obj, but it doesn't have a clue that in *main.cpp* special template of `Sample<int>` used, so the compiler does not create that special class to be instantiated. Therefore, when *main.cpp* is compiled with *sample.obj* we get a linking error. 


The easiest solution is to put both declaration and definition in the same file, *sample.h*. But it increases the size of the executable file and surpasses capabilities that separation of declaration and definition brings like solving circular dependencies. 

The second solution is to inform the compiler that we need that special class

```cpp
// file sample.cpp

#include "sample.h"

template<class T>
T Sample<T>::Compute(){

	return T();
}

// This line is the key!
template class Sample<int>;

```

Now compiling *sample.cpp*, we get a *sample.obj* (*sample.o* on linux) containing `Sample<int>` class.

## Type Constraints

We can limit the types that a template can take using `static_assert`, `std::is_same`, and `std::is_base_of` :

```cpp
#include <type_traits>

template<class T>
class Foo
{
	Foo() {
		static_assert(std::is_same<T, int>::value, "T must be int");
	}
};

int main()
{
  Foo<int> a; // works fine
  Foo<bool> b; // Error: T must be int

	return 0;
}
```
## Enforcing inheritance

When inheriting from a template class, the compiler overlooks what is inherited.

```cpp
template<class T>
struct Animal{
  void Move(){}
};

template<class T>
struct Dog: Animal<T>{
  void Run(){
    Move(); // Error: Move() no defined!
  }
};
```

In the example above, when `Dog` is compiled, the compiler overlooks the content of `Animal` because it is 
dependent on `T`. Therefore, it has no idea of `Move()` coming from `Animal`. To fix that, call the method using `this` to defer the check until template instantiation:

```cpp
this->Move();
```

Another fix is to declare the method:

```cpp
template<T>
struct Dog: Animal{
  using Animal<T>::Move;
// rest...
}
```
## Type Alias

Since *C++11*, we can define a type alias for  and hard to read names

```cpp
template<T>
using VecPoint = vector<Point<T>>
```
See [here](https://iamsorush.com/posts/how-use-cpp-raw-pointer/#owner-convention), I created an alias for pointers to have an ownership convention.

## Meta-Programming

Metaprogramming is to write a program targeting compile-time values and types. For values, 
I recommend where possible, instead of templates, use `constexpr` of *C++11*  which is cleaner and easier to read. 

We can assess and conclude types using templates, for example, `const` qualifier can be dropped by

```cpp
// General type
template<typename T> 
struct RemoveConst{ 
    typedef T type;             
};

// const specialization
template<typename T> 
struct RemoveConst<const T> { 
    typedef T type;               
};

int main(){    
    std::is_same<int, removeConst<double>::type>::value; // true
    std::is_same<int, removeConst<double int>::type>::value;  // true
}
```
The function above is defined in the standard library as `std::remove_const`. In most cases, standard functions defined in  `<type_traits>` header such as `add_const`, `remove_pointer`, `add_pointer`, `is_same` along with `static_assert`  meet our needs. 

## Practical Cases

### Customize STL Containers

Templates are mostly used for creating custom containers. In the below example,  a vector is created that can print its items on the screen.

```cpp
#include <iostream>
#include <vector>
using namespace std;

template<class T>
class PrintableVector{
    vector<T> data;
    public:
    PrintableVector(std::initializer_list<T> list)
    {
        data.assign(list);
    }
    void Print(){
      for (auto& item: data)
        cout<< item<<" ";
    }
};
int main() {
   PrintableVector<int> a({1,3,5,7});
   a.Print(); // 1 3 5 7
return 0;
}
```
### Multidimensional space

Templates can helps us design a program with different dimensions with the same code. The below code, defines `Point` in 1D, 2D, ..., and nD dimensions:

```cpp
#include <iostream>
#include <vector>
using namespace std;

template<class T, size_t size>
class Point{
    T data[size];
    public:
    Point(){
        for (auto& item: data)
            item = T();
    }
    Point(std::initializer_list<T> list){
        size_t i=0;
        for (auto& item: list){
            data[i] = item;
            i++;
            if (i>=size) break;
        }
    }
    Point<T,size> GetDistanceTo(Point<T,size>& point){
        Point<T,size> distance;
        for (auto i=0;i<size;i++){
            distance[i] = data[i] - point[i];
        }
        return distance;
    }
    T& operator[] (size_t i)
    {
        return data[i];
    }
    void Print(){
      for (auto& item: data)
        cout<< item<<" ";
    }
};
int main() {
  
   Point<int,3> a({2,2,2}); // 3D point
   Point<int,3> origin({0,0,0}); // 3D point
   
   Point<int,2> m({5,5}); // 2D point
   Point<int,2> n({4,4}); // 2D point
   
   a.GetDistanceTo(origin).Print(); // 2 2 2
   m.GetDistanceTo(n).Print();// 1 1
return 0;
}
```


## References

[isocpp.org](https://isocpp.org/wiki/faq/templates#fn-templates)


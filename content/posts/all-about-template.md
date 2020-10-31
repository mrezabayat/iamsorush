---
title: "C++ template crash course"
date: 2020-10-31T19:34:31+01:00
image: /images/bird.webp
thumbnail: /images/bird_tn.webp
tags: ["C++", "Template"]
---

## Template

Using templates in C++, you can create functions or classes having similar behaviors for different types.

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

A function can be dependent to a generic type

```cpp
template<class T>
T& Min(T a, T b){
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
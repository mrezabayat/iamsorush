---
title: 'How to use C/C++ raw pointers properly?'
date: 2020-02-22T20:05:39Z
draft: false
image: /images/pointer.jpg
tags: ['C++']
categories: "C++"
summary: "A pointer is an 8-byte type on a 64-bit machine that holds the memory address of an object, target. Here, I  mention the most useful characteristics of pointers with examples."
---


## Introduction


*C/C++* is used widely for high-performance computing. Mastering pointers is an important step in writing efficient code. Here, I  mention the most useful characteristics of pointers with examples.   

I call them here pointers but nowadays they are called raw pointers to separate them from smart pointers. I will write on smart pointers separately.    



## Definition

A pointer is an 8-byte type on a 64-bit machine that holds the memory address of an object, target.    

```cpp
int  x = 20;   //  variable declaration
int* p; // pointer declaration
p = &x;  // pointer stores address of x
cout<< p <<endl; //0x7ffc52a21a84
cout<< *p <<endl; // 20
```



In the above example, `p` at the beginning is declared but undefined (it points to somewhere we don't know); then pointed to `x`. The pointer holds the memory address of `x`.  Using `*` operator, the pointer can be dereferenced to get the value of its target.     



## Memory Allocation



A pointer is usually pointed to dynamically allocated memory on the heap, a scalar   



```cpp
int* p = new int;
```

or an array 

``` cpp
int* q = new int[5];
```

## Delete

 The allocated memory can be deleted (not the pointer itself)   



```cpp
delete p; // new int memory now deleted
```
To delete all elements of the array 

```cpp
delete[] q; // All elements of array deleted
```
Note that they are not literally deleted, the memory is marked as free to be overwritten.    


Note that `new` ends with `delete`, `new[]` ends with `delete[]`. The compiler nows the number of elements of the array created via `new[]`, so `delete[]` doesn't need the number of elements.


Do not delete the dynamically created array using `delete`

```cpp
delete q; // Error: only one element is deleted
```






Do not delete a stack memory that a pointer points to    



```cpp
int x;
int* p=&x;
delete p; // Undefined Behaviour: deleting a memory on stack!
```



Do not double delete   



```cpp
int* p = new int;
delete p; // target memory deleted
delete p; // error or undefined behaviour
```



## Null usage



I prefer to point the pointer to `nullptr` (or `NULL` for *C* and older than *C++11* compilers) when there is nothing to point to: at declaration and deletion. In this way, we avoid undefined behavior.    



```cpp
int* p = nullptr  // declaration with null
int* q = new int; // memory allocation
delete q; // removing allocated memory
q = nullptr;
```



`nullptr` is type-safe in comparison with `NULL`. In some [cases](https://stackoverflow.com/questions/20509734/null-vs-nullptr-why-was-it-replaced), compilers confuse the type of `NULL` with `int`. We can check if a pointer is null like below   



```cpp
if(p!=nullptr) {...}  // C++11 and later
if(p!=NULL) {...} // C and older C++ compilers
```



It should be noted that making a pointer null after delete hides the double-delete problem explained in the previous section. And it does not affect other pointers pointing to the same deleted memory. Some people don't like this convention read [here](https://stackoverflow.com/questions/4190703/is-it-safe-to-delete-a-null-pointer).    



## Memory leak



There is no memory management system for raw pointers. Therefore, not deleting the allocated memory of pointer explicitly causes memory leak:   



```cpp
int x;
int* p = new int;
p = &x;  // re-pointed but "new int" not deleted
```

In the above example, new int memory is an island in the sea of computer memory. We could only find it via `p` but, in the last line, `p` is pointed to another place, `x`. So we have a memory leak! We have to remember to delete allocated memory and then point the pointer to another variable/new allocated memory:   



```cpp
int x;
int* p = new int;
delete p;
p = &x;
```


The same happens if the pointer goes out of scope   



```cpp
// some code here
{
    int* p = new int; // p declared and given a new memory
    // do some stuff with p
}
// p is destroyed here but new int memory is somewhere not deleted
```



Again we have to remember to delete it ourself:



```cpp
{
    int* p= new int; // p declared and given a new memory
    // do some stuff with p
    delete p;  // the new int is deleted.
}
```

There is another situation that memory leaks:   


```cpp
int* p = new int;
... an exception is thrown here..
delete p; // this is not reached.
```


A raw pointer cannot handle this, you need to use smart pointers (see this [discussion](https://stackoverflow.com/questions/24150472/c-avoiding-memory-leak-with-exceptions) ).   


For deleting a memory, the situation gets complicated fast when it is pointed by many different pointers:   



```cpp
Class Student{...}
Class CourseA{
  public:
    CourseA(*Student student):Top(student) {}
    ~A(){// delete Top here?}
    Student* Top;
}
Class CourseB{
  Public:
    CourseB(*Student student):Top(student) {}
    ~B(){// delete Top here?}
    Student* Top;
}
...
{
Student* Jack= new Student();
CourseA* A= new CourseA(Jack);
CourseB* B= new CourseB(Jack);
// delete Jack here, in CourseA or in CourseB destructor?
}
```

In the above example, three pointers target the same memory location, thus we cannot run `delete` for all of them as we face double-delete problems explained in the Delete section. 

## Owner Convention

In the previous example, we have to decide which one is the owner or which one 
needs to outlive others, so we run `delete` command on that one and leave the rest as observers.

We can have `owner` as a type alias for `T`.

```cpp
template<class T>
using owner = T;
```

Now we can have a convention for our code that pointers are defined by `owner` only when the class containing them is responsible for deleting them.

A simple example that owner acts as a raw pointer:

```cpp
struct A{
    owner<int*> p;
    ~A(){delete p;}
};
```



 Note that smart pointers, which are introduced in *C++11*, elegantly address this problem.    



##  Dereference class members


A class member, method or variable, can be accessed via `->` operator:   


```cpp
class Person{
public:
    string name = "Jack";
}
Person* p = new Person();
std::cout << p->name << endl;  // Jack
```



## Pass by pointer

It is a good practice to pass objects especially the huge ones by a pointer. Instead of copying the whole data, only the pointer is passed:   



```cpp
void DoSomething(vector<int>* v){
 /* do something with v */
}
...
auto a = new vector<int>(10000);
DoSomething(a);
```



I mostly prefer pass by pointer than by reference, both methods have the same efficiency but a pointer can be null while a reference cannot. But you may want to use reference because you are not handling null in the function.    



When passing by pointer, the pointer itself passed by value    



```cpp
void f(int* p)
{
    *p = 100;   // the pointed memory changed
    p = nullptr;  // p is changed within function not externally
}
...
int* q = new int(0);
cout<< q << endl;
f(q);
cout<< *q << endl;  // 100
cout<< q << endl;  // q is not changed
...
```



## Constant



A constant definition can be added to a pointer as below   



```cpp
const int* p // constant or read-only target, pointer can be reassigned
int* const p // constant pointer cannot be reassigned
const int* const p // both above constraints
```



Too many options? Well, they are there to constrain the usage of a pointer, so, when other developers read your code they quickly understand the purpose of variables. For example, if the target must not be changed in specific scope then use a constant-target pointer and other developers do not mistakenly change them.    



The target of a constant-target pointer is not necessarily constant:   



```cpp
int a=5;
const int* p = &a; // ok: read-only pointer
a = 10;  // ok
*p = 20; // Error:: against "read-only" contract
```



However, a constant target must be pointed only by a constant-target pointer.   



## Pointer vs reference member


A reference member of a class must be initialised in the constructor and it cannot be reassigned. However, a pointer member can be reassigned, freed, and null. So, if not sure, a pointer is an easy choice as it is more flexible.    



## Arrays and vectors



In *C* language, it is common to define an array using a pointer   



```cpp
int *p = new int[5]; // dynamically allocated array
cout<< p[2]; // prints 3rd element

int *q[5]; // array of 5 integer pointers  

int arr[5];  // array of 5 integers
int* r = arr;  // pointer points to first element of array
cout<< *(r+2); // shows 3rd element of arr
```

A dynamic 2D array can be created with a pointer-to-pointer type

```cpp
int **p;
// dynamic array of pointers
// each pointer is a row
p = new int*[5]; 

// loop over rows
for (int i = 0; i < 5; ++i) {
  p[i] = new int[6]; // each row has 6 columns
  // p[i] points to dynamic array of int values
}
```
The elements can be accessed via `[]` operators

```cpp
int row=1, column=2;
p[row][column]=3; // 
```


In *C++*, we have the vector class which has many features and in terms of read-and-write is as fast as a raw array [see here](https://stackoverflow.com/questions/3664272/is-stdvector-so-much-slower-than-plain-arrays).  So it's better to use a vector than a pointer to create an array.  But how to dereference a pointer to a vector? many ways:   

```cpp
vector<int> *v = new vector<int>(10);

v->operator[](2); // using operator
(*v)[2]; // dereferencing whole vector first
v->at(2); // using At
v->size(); //Get size
vector<int> &r = *v; // create alias using a reference
r[2]; // index reference
```

## Void pointer 

All the pointers (int*, double*, string*, custom_class*) have the same datatype holding the memory address of different targets. So, `void*` pointer is a pointer the same as others pointing to some memory address but the datatype of the target is unknown. 

```cpp
void* p;
int i=10;
double d=1.5;
p = &i;
p = &d;
cout<<*(double*)p; // cast when dereferenced
```

It is a *C* language feature to write generic functions. But in *C++*, knowing `void*` tricks are not necessary since generic code can be elegantly written with templates, functors and interfaces.  

## Read Pointers

Pointers are printed in hexadecimal (hex) system which includes {0-9,a-f} characters.

```cpp
    int* p = new int;
    cout << p   << endl; // 0x10dbc20 
    cout << p+1 << endl; // 0x10dbc24
    cout << p+2 << endl; // 0x10dbc28
    cout << p+3 << endl; // 0x10dbc2c
```

"0x" represents hex system. Focusing on the last numbers, {0, 4, 8, c}, they increase by 4 unit because an integer on the target machine was 4 bytes. Note in hex system, 8+4=c.   
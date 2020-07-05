---
title: 'How to use C/C++ raw pointers properly?'
date: 2020-02-22T20:05:39Z
draft: false
image: /images/pointer.webp
thumbnail: /images/pointer_tn.webp
---
## Introduction


C/C++ is used widely for high performance, number crunching, and gaming projects. For example in computational fluid dynamics (CFD) codes millions of times equations are solved on millions of mesh nodes to simulate a few seconds in real life. However, An unoptimised code can run 10, 100, or 1000 times slower. There are many tips and tricks on optimising a code but simply mastering pointers is an important step in writing efficient code. Here, I try to mention some important characteristics of pointers that help you design your code better.   



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



In the above example, p at the beginning is declared but undefined (it points to somewhere we don't know); then pointed to x. The pointer holds the memory address of x.  Using * operator, the pointer can be dereferenced to get the value of its target.     



## Delete



A pointer is usually pointed to dynamically allocated memory on the heap   



```cpp
int* p = new int;
```

 the allocated memory can be deleted (not the pointer itself)   



```cpp
delete p; // new int memory now deleted
```



Note it is not literally deleted, the memory marked as free to be overwritten.    



Do not delete a stack memory that a pointer points to    



```cpp
void main(){
int x;
int* p=&x;
delete p; // Undefined Behaviour: deleting a memory on stack!
}
```



Do not double delete   



```cpp
int* p = new int;
delete p; // target memory deleted
delete p; // error or undefined behaviour
```



## Null usage



I prefer to point the pointer to nullptr (or NULL for C and older than c++11 compilers) when there is nothing to point to: declaration and deletion. In this way, I avoid undefined behaviour.    



```cpp
int* p = nullptr  // declaration with null
int* q = new int; // memory allocation
delete q; // removing allocated memory
q = nullptr;
```



nullptr is type-safe in comparison with NULL. In some <a href="https://stackoverflow.com/questions/20509734/null-vs-nullptr-why-was-it-replaced">scenarios</a>, compilers confuse the type of NULL with int. We can check if a pointer is null like below   



```cpp
if(p!=nullptr) {...}  // C++11 and later
if(p!=NULL) {...} // C and older C++ compilers
```



It should be noted that making pointer null after delete hides the double-delete problem explained in the previous section. And it has no effect on other pointers pointing to the same deleted memory. Some people don't like this convention read <a href="https://stackoverflow.com/questions/4190703/is-it-safe-to-delete-a-null-pointer">here</a>.    



## Memory leak



There is no memory management system for raw pointers. Therefore, not deleting the allocated memory of pointer explicitly causes memory leak:   



```cpp
 int x;
int* p = new int;
p = &x;  // re-pointed but "new int" not deleted
```

<p class="has-normal-font-size">In the above example, new int memory is an island in the sea of computer memory. We could only find it via p but, in the last line, p is pointed to another place, x. So we have a memory leak! We have to remember to delete allocated memory and then point the pointer to another variable/new allocated memory:   



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



Again we have to remember to delete it ourself   



```cpp
{
    int* p= new int; // p declared and given a new memory
    // do some stuff with p
    delete p;  // the new int is deleted.
}
```



However,  in practice, it is not that straightforward. The things get complicated fast when an object is pointed by many different pointers:   



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

In the above example, three pointers target the same memory location, thus we cannot run delete on all of them we face double-delete problems explained in the Delete section. Here, we have to decide which one is the owner or which one needs to outlive others, so we run delete command on that one, so the rest are observers. Because of these complexities, smart pointers are introduced in C++11.    


There is another situation that memory leaks:   


```cpp
int* p = new int;
... an exception is thrown here..
delete p; // this is not reached.
```



A raw pointer cannot handle this, you need to use smart pointers (see this <a href="https://stackoverflow.com/questions/24150472/c-avoiding-memory-leak-with-exceptions">discussion</a>).   



##  Dereference class members


A class member, method or variable, can be accessed via -&gt; operator:   


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



I mostly prefer pass by pointer than by reference, both methods have the same efficiency but a pointer can be null while reference cannot. But you may want to use reference because you are not handling null in the function.    



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



Too many options hah? Basically, they are there to constrain the usage of a pointer, so, when other developers read your code they quickly understand the purpose of variables. For example, if the target must not be changed in specific scope then use constant-target pointer and other developers do not mistakenly change them.    



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



## Pointer, array, vector



In C language, it is common to define an array using a pointer   



```cpp
int (*p)[5]; // array of 5 integer using pointer  
int arr[5];  // array of 5 integer
int* q = arr;  // pointer points to first element of array
cout<< *(q+2) << endl; // shows third element of array
```



In C++, we have the vector class which has many features and in terms of read-and-write is as fast as a raw array (<a href="https://stackoverflow.com/questions/3664272/is-stdvector-so-much-slower-than-plain-arrays">see here</a>).  So it's better to use a vector than a pointer to create an array.  But how to dereference a pointer to a vector? many ways:   



```cpp
vector<int> *v = new vector<int>(10);

v->operator[](2); // using operator
(*v)[2]; // dereferencing whole vector first
v->at(2); // using At
v->size(); //Get size
vector<int> &r = *v; // create alias using a reference
r[2]; // index reference
```

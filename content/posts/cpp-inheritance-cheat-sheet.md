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

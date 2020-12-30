---
title: "What are Smart pointers and how to use them?"
date: 2020-12-05T18:10:20+01:00
image: /images/pingpong.jpg
imageQuality: "q65"
imageAnchor: "Center" # Smart, Center, TopLeft, Top, TopRight, Left, Right, BottomLeft, Bottom, BottomRight.
tags: ["MPI", "C++"]
categories: "C++" 
summary: "Summary of this page used in cards, and also in SEO description of the page."
draft: true
---

## Introduction

- The first choice is the unique pointer. Unless you know, avoid shared pointers.
- Where the ownership of a pointer is not important, pass it as a reference.

```cpp
#include<iostream>
#include<memory>
using namespace std;

struct CsvWriter{
    void Write(int data){cout<<"Writing CSV file:"<<data<<endl;};
};
struct Controller{ 
  Controller(CsvWriter& writer_):writer(writer_){}
  void Run(){
      cout<< "Producing data ..."<<endl;
      writer.Write(1000);
  }
  private:
  CsvWriter& writer;
};
int main(){
unique_ptr<CsvWriter> csvWriter(new CsvWriter);
Controller controller(*csvWriter);
controller.Run();
}
```

- in the above situation, you can pass raw pointer in case the pointer may become null.


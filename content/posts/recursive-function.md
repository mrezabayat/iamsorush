---
title: 'What is a recursive function?'
date: 2020-06-03T20:04:00Z
draft: false
image: /images/circle.webp
thumbnail: /images/circle_tn.webp
tags: ['C++', 'Numerical Code']
categories: "Algorithms"
---

## Definition

A recursive function is a function that calls itself with different arguments. Therefore, it is applied to a problem that each step of it is similar to the previous one. The function must have a condition (base case) to break self-calling when desired result is achieved.

## Examples

**1-  Function calls itself once: Factorial of a positive integer**

n! = n (n-1) (n-2) ... 1 = n [(n-1) (n-2) ... 1] = n × (n-1)!

```cpp
//C++
int factorial(int n)
{
    if (n==1) return 1;
    return n*factorial(n-1);
 }
```
In the above example, the operations are self similar: n is multiplied by the expression inside square brackets. The expression in fact is `(n-1)!` And that’s exactly what we wrote in the code. The condition `(n==1)` is to break the self-calling loop.

**2- Function calls itself multiple times: Finding permutations of a string**

Permutations of `ABC` are `P(ABC) = {ABC, BAC, CAB, ACB, BCA,  CBA}`. This set can be written as `P(ABC) = {A P(BC), B P(AC), C P(AB)}`. In this problem, the left hand-side expression is similar to the expressions in the curly brackets, but we have three similar branches instead of one.

```cpp
//C++
void FindPermutations(string str, int j, int k)  
{  
    if (j == k)  
        cout<<str<<endl;  
    else
    {  
        for (int i = j; i <= k; i++)  
        {  
            // std::swap() is a built-in function
            swap(str[j], str[i]);  
            FindPermutations(str, j+1, k);    
            swap(str[j], str[i]);  
        }  
    }  
}
```
The code is the same as the equation. We have multiple (the number of letters) branches of function calling itself. Each branch starts with a unique letter which is not permuted. The whole string is injected to the next function call but, the focused interval `[j,k]` is narrowed down to `[j+1,k]`. The leaves of this tree are reached when `j==k`.

## Discussion

Recursive functions can be a bit challenging to grasp but when you get it, they can be used to code self-similar procedures and trees easier than iterations. Recursive functions, applied to the right problems, are usually shorter and more elegant than iterations. If the first example is written using iterations, the difference may not be obvious. However, writing the second example using iterations, can be a nightmare.

The main concern about recursive functions is their efficiency. Every time a function calls itself, a newly created function memory is pushed into the stack. The more local variables and more self-calling, the more chance of stack-overflow. This is not the case for iterative algorithms where the local variables are overwritten after each iteration. It should be noted the run-time speed depends on the code details, the context that the function is used and compiler optimisations. Therefore, if the efficiency of a recursive method is of concern, it should be assessed with a code profiler.

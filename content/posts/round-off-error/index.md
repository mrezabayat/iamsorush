---
title: "A note on computer round-off error in physics"
date: 2020-12-26T18:10:20+01:00
image: /images/error.jpg
imageQuality: "q65"
imageAnchor: "Center" # Smart, Center, TopLeft, Top, TopRight, Left, Right, BottomLeft, Bottom, BottomRight.
tags: ["C++", "C Sharp"]
categories: "C++" 
summary: "The way floating-point numbers are stored in the memory of a computer can lead to unwanted errors. Here we have an overview of the basics of storing numbers and how they affect the outcome of physics programs."
katex: true
---
 
## Introduction

{{< rawhtml >}}A \(16-bit\) floating-point number is stored roughly as below {{< /rawhtml >}}

```
0     |  100  0000 00|00 0001
sign     Mantissa      Exponent
```
{{< rawhtml >}}
One bit for sign of the number, \(6\) bits for the exponent and \(9\) bits for significant numbers, mantissa.
For more details on how the number is returned to base \(10\) {{< /rawhtml >}} , see [here](https://en.wikibooks.org/wiki/A-level_Computing/AQA/Paper_2/Fundamentals_of_data_representation/Floating_point_numbers). 

This is similar to showing numbers with scientific notation in base {{< rawhtml >}} \(10\) {{< /rawhtml >}}

$$-123 = (-1) \times 0.123 \times 10^3 $$

$$0.000456 = (+1) \times 0.456 \times 10^{-3}$$

Looking at this style of saving a floating number, we can conclude below points

* The precision is finite and dependent on the size of the mantissa. So, if mantissa can only store {{< rawhtml >}} \(3\) {{< /rawhtml >}} digits

$$x = 0.12345 \Rightarrow x = 0.123$$


* Multiplication happen by calculation of mantissa's and exponents separately and then round-off

{{< rawhtml >}}
\[
\begin{aligned}
x &= 0.0123 \times 567  \\
  &= 0.123 \times 10^{-1} \times 0.567 \times 10^3  \\
  &= (0.123 \times 0.567) \times (10^{-1}  \times 10^3) \\ 
  &= 0.069741 \times 10^2     \\
  &= 0.69741 \times 10    ~~ \text{ remove leading 0's}  \\
  &= 0.697 \times 10    ~~~~~   \text{round-off } 
  \end{aligned}
\]
{{< /rawhtml >}}

* Addition happens by bringing the small number to the same exponent as the large number then adding mantissa's

{{< rawhtml >}}
\[
\begin{aligned}
x &= 567 + 0.123 \\
  &= 0.567 \times 10^3 + 0.000123  \times 10^3 \\
  &= 0.567123 \times 10^3  \\
  &= 0.567 \times 10^3     ~~ \text{round-off }
\end{aligned}
\]
{{< /rawhtml >}}

Note that in the above example, the whole small number disappeared in the result.


## Implicationn in Physics

{{< rawhtml >}}

 In physics codes, we have to ensure the precision is enough to capture the small magnitude phenomena. For example in a system that maximum temperature is \(1000\degree C\), with single-precision numbers (8 digits), we cannot have a heat source at \(0.00001 \degree C\). 
 {{< /rawhtml >}}

In systems with different unit properties like pressure, density, and velocity, it becomes hard to track the precision of all properties. Therefore, they are usually normalized with reference values to measure their accuracy from 1. 

For example, let's have a look at Bernoulli's equation in a horizontal pipeline:

$$p + \frac{1}{2} \rho v^2 = c$$

{{< rawhtml >}}
Where \(p\) is pressure, \(\rho\) is the density of the fluid, \(v\) is the velocity of the fluid and \(c\) a constant. Before coding,  we can normalize the equation. Let's assume the pressure is in the order of atmospheric pressure, \(p_0\). A reference velocity can be found as
{{< /rawhtml >}}

{{< rawhtml >}}
\[
p_0 = \frac{1}{2} \rho v_{0}^2 \\ 
\text{ }\\
v_0 = \sqrt{ 2 p_0 / \rho}
\]

Dividing both side by \(p_0\)
{{< /rawhtml >}}

{{< rawhtml >}}
\[
\frac{p}{p_0} + \frac{1}{2} \frac{ \rho v^2}{p_0}  = \frac{c}{p_0}    \\
\text{ }\\
\frac{p}{p_0} + (\frac{ v}{v_0})^2 = c_2 \\
\text{ }\\
P + V^2 = c_2
\]

So we code the equation with \(P\) and \(V\) which are close to \(1\) rather than absolute pressure and velocity which can be of different orders, for example, \(5 \times 10^5\) pa and \(5\) m/s respectively. Note that by normalization, we do not increase the accuracy but facilitate analyzing accuracy. 
{{< /rawhtml >}}


## Round-off error accumulation

{{< rawhtml >}}
In algorithms where round-off error is accumulated the outcome deviates from what expected. In the below example, \(1/3\) is constantly added to a number then it is subtracted the same amount from the outcome. The result is different from the initial value. 
{{< /rawhtml >}}

```cpp
#include <iostream>
#include <iomanip>

int main()
{
  float initial = 1.0;
  float result = initial;
  float one_third = 1.0/3.0;
  int iterations = 100000;  
  for (auto i = 1 ;i< iterations;i++)
    result = result + one_third;
  
           
  for (auto i = 1 ;i< iterations;i++)
    result = result - one_third;
    
    std::cout << std::fixed << std::setprecision(8) 
        << "initial= " << initial    // 1.00000000
        << "\nresult = "<<result;    // 1.00017393 
}

```
{{< rawhtml >}}
Note \(1/3 = 0.3333...3\) cannot be exactly stored in floating-point memory. if we assume delta as the error of storing \(1/3\), we can write the above sequence as


\[
\begin{aligned}
r_0 &= 1.0 \\
r_1 &= (1+\delta) (r_0 + \frac{1}{3}) \\
r_2 &= (1+\delta) (r_1 + \frac{1}{3}) \\
r_n &= (1+\delta) (r_{n-1} + \frac{1}{3}) \\
\end{aligned}
\]
{{< /rawhtml >}}

It can be concluded that the error of each term added to the next term and we get an accumulation of the round-off error.

Note that if the sequence was in a way that we had subtraction of terms, the errors could cancel out each other.


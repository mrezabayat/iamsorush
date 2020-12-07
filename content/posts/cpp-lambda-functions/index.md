---
title: "MPI Traffic Program"
date: 2020-12-07T18:10:20+01:00
image: /images/pingpong.jpg
imageQuality: "q65"
imageAnchor: "Center" # Smart, Center, TopLeft, Top, TopRight, Left, Right, BottomLeft, Bottom, BottomRight.
tags: ["MPI", "C++"]
categories: "C++" 
summary: "Summary of this page used in cards, and also in SEO description of the page."
draft: true
---

## Goal

I want to solve a traffice problem (see references) with MPI. 

- We have a road comprised of n points. 
- Cars move over these points.
- At each time step, each car may move to next point.
- A car moves only if next point is empty.
- The road has periodic boundaries.

## Result

See the code on [GitHub](https://github.com/sorush-khajepor/mpi-samples/tree/main/traffic).

## Example
"-" an empty point, 
"o" a car

step=0:  -  o  o  -  o  -   - 

step=1:  - o - o - o -  

setp=2:  - - o - o - o  

step=3:  o - - o - o - 


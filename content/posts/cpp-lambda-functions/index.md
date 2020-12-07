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

## Dependency

State of each point at next time step depends on current state of itself and its nearest points:

```
P = A point
i= Index of a point
t = Time step
f = A function of 

P[i] @(t+1) = f( P[i-1], P[i], P[i+1] ) @t
```

The function can be divided into two steps:

```
1) if P[i-1] has car & P[i] is empty
        P[i] will have the car @t+1
2) if P[i] has car & P[i+1] is empty
        P[i] will be empty @t+1
```

In the first condition `P[i]` needs to be empty, in the second one `P[i]` must have a car. They cannot happen at the same time for a point. Either (1) happens or (2). Therefore, we can separate or reorder them and still we get same result for 'P[i] @t+1' .    

## Design

My approach to the problem can be simply shown in this code:

```cpp
struct RoadSection{

    vector<char>& points;

    void Run(){
        ISendBoundaryPoints();
        MoveInternalPoints();
        RecvGhosts();
        MoveBoundaryPoints();
    }

    
    // The rest ...
    
};
```

Each processore is going to solve a `RoadSection`. Each `RoadSection` is allocated some `points`. When run is called, each processor run these tasks:

- `ISendBoundaryPoints()`: In a non-blocking way, send  boundary points to neighboring road sections. 
- `MoveInternalPoints()`: Move cars which are not on boundaries, i.e. defer solving boundaries.  
- `RecvGhosts()`: Receive boundary of neighbors which are ghosts in this `RoadSection. 
- ` MoveBoundaryPoints()`: A boundary points, now, knows its left and right points, its dependencies, so it can be moved.



## Why Vector<char> not vector<bool>

`vector<bool>` is a special case of `vector<>` container where each element is a stored as a bit in contrast with a normal `bool` takes. For more info, [read here](https://stackoverflow.com/questions/17794569/why-isnt-vectorbool-a-stl-container). Therefore, I use `vector<char>` with `t` and `f` values as *true* and *false*.



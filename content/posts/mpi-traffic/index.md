---
title: "MPI Traffic Program with C++"
date: 2020-12-14T23:10:20+01:00
image: /images/traffic.jpg
imageQuality: "q65"
imageAnchor: "Bottom" # Smart, Center, TopLeft, Top, TopRight, Left, Right, BottomLeft, Bottom, BottomRight.
tags: ["MPI", "C++"]
categories: "C++" 
summary: "I want to solve a traffic problem with MPI and C++. The road is divided into sections which send their boundaries and receive their ghost points."
---

## Goal

I want to solve a traffic problem with MPI. 

- We have a road comprised of n points. 
- Cars move over these points.
- At each time step, each car may move to the next point.
- A car moves only if the next point is empty.
- The road has periodic boundaries.

## Example

"-" is an empty point and "o" is  a car:

step = 0:  -  o  o  -  o  -   - 

step = 1:  - o - o - o -  

setp = 2:  - - o - o - o  

step = 3:  o - - o - o - 

## Code

The solution is placed in [GitHub](https://github.com/sorush-khajepor/mpi-samples/tree/main/traffic).

## Dependency

The state of each point at the next time step depends on the current state of itself and its nearest points:

```
P = A point
i = Index of a point
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

In the first condition `P[i]` needs to be empty, in the second one `P[i]` must have a car. They cannot happen at the same time for a point. Either (1) happens or (2). Therefore, we can separate or reorder them and still we get the same result for 'P[i] @t+1' .    

## Design

Let's say the road has 12 points, and is modeled by 3 processors. We have 3 `RoadSections` shown below.

{{< img "*roadsections*" "road sections" >}}


Each processor has 4 points plus 2 ghost (G) points. The right ghost point of RoadSection 1 represents point 0 of RoadSection 2 and the left ghost point of RoadSection 1 is an image of point 3 of RoadSection 0. 

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

Each `RoadSection` is allocated some `points`. When run is called, each processor run these tasks:

- `ISendBoundaryPoints()`: In a non-blocking way, send  boundary points (0,3) to neighboring road sections. 
- `MoveInternalPoints()`: Move cars that are not on boundaries (1,2), i.e. defer solving boundaries.  
- `RecvGhosts()`: Receive boundary of neighbors which are ghosts in this `RoadSection`. 
- ` MoveBoundaryPoints()`: A boundary point, now, knows its left and right points, its dependencies, so it can be moved.

## Constructor

The rank of a road section and its neighbors are initialized in the constructor

```cpp
RoadSection(vector<char>& _points)
:points(_points)
{
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    leftRank = (rank+size-1)%size;
    rightRank = (rank+1)%size;
}
```

## Send Boundary Points

We send the first node of a road section to its left neighbor and the last node to its right neighbor. The send is non-blocking, therefore, these points can be overridden during internal movement, so they are sent via temporary variables.

```cpp
void ISendBoundaryPoints()
{
    // l
    tmpLeftPoint = points.front();
    tmpRightPoint = points.back();
    MPI_Isend(&tmpLeftPoint, 1, MPI_CHAR, leftRank, 0, MPI_COMM_WORLD, &leftReq);
    MPI_Isend(&tmpRightPoint, 1, MPI_CHAR, rightRank, 0, MPI_COMM_WORLD, &rightReq);
}
```

## Internal Movement

 A simple strategy to update points is to use a second array of points as the new position. However, here to save memory the points are updated directionally from left to right and in the original array of points. Point[i] and Point[i+1] are updated at the same time by swap function, we keep a copy of old value of Point[i+1] to be used for updating p[i+2]. 

```cpp
void MoveInternalPoints(){
    char points_i = points[0];
    for (size_t i = 0; i < points.size()-1; i++)
    {
        if (points_i=='t' && points[i+1]!='t' ){
            points_i = points[i+1]; 
            swap(points[i], points[i+1]); 
        }
        else{
            points_i = points[i+1];
        }
    }
}
```
## Receive Ghosts

The ghost cells are received from the left and right neighbors. One receive is non-blocking to make sure the second receive is not blocked. 

```cpp
void RecvGhosts(){
    MPI_Request req;
    MPI_Irecv(&rightGhost, 1, MPI_CHAR, rightRank, 0, MPI_COMM_WORLD, &req);
    MPI_Recv(&leftGhost, 1, MPI_CHAR, leftRank, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
    MPI_Wait(&req , MPI_STATUS_IGNORE);
    }
```

## Move Boundary Points

The final step is to move boundary points using their backed-up values and ghost points. Note that Point[0] and Point[last] (=Point[3] in the picture) may have changed during internal movement because of that we use their backed-up value. Moreover, as we explained in the dependency section if boundary points are updated by this method, they certainly didn't change during internal movement.

```cpp
void MoveBoundaryPoints(){
    // This release tmpLeftPoint, tmpRightPoint
    MPI_Wait( &rightReq , MPI_STATUS_IGNORE);
    MPI_Wait( &leftReq , MPI_STATUS_IGNORE);

    if (leftGhost=='t' && tmpLeftPoint!='t'){
            swap(leftGhost, tmpLeftPoint);
            points.front() = tmpLeftPoint;
    }
    if (tmpRightPoint=='t' && rightGhost!='t'){
            swap(tmpRightPoint, rightGhost);
            points.back() = tmpRightPoint;
    }
}
```

## Why Vector\<char> ?

Each point either has a car or is empty. I needed a boolean type. But, unfortunately, `vector<bool>` is a special case of `vector<>` container where each element is a stored as a bit in contrast with a normal `bool` takes. For more info, [read here](https://stackoverflow.com/questions/17794569/why-isnt-vectorbool-a-stl-container). Therefore, I used `vector<char>` with `t` and `f` values as *true* and *false* to be MPI friendly. 



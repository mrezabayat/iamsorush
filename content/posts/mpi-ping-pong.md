---
title: "MPI ping pong program using C++"
date: 2020-11-14T10:30:30+01:00
image: /images/pingpong.jpg
imageQuality: "q65"
imageAnchor: "Center"
tags: ["MPI", "C++"]
categories: "Algorithms"
summary: "I want to write an MPI ping pong program where two processes send a piece of data back and forth to each other."
---

## Goal

I want to write an MPI ping pong program where two processes send a piece of data back and forth
to each other. This is a good example to measure the latency and bandwidth of a cluster machine. Since, currently, the MPI for C is developing stronger than C++ (see [References](#references)), I am wrapping MPI-C commands in C++ classes here. 

## The ball

If we imagine the data transfer between two nodes is like a ping-pong game, the data is the ball.
The ball can be an array of MPI types. Here for simplicity, is the integer:

```cpp
struct Ball
{
    Ball(int size){
        Data = new int[size];
        Data[0] = 0;
        Size = size;
    }
    int* Data;
    int Size;
};
```

In this example, I ignore what is in `Data` array except *0-th* element which counts the number of back-and-forths of the ball.

## IPlayer

As I am still thinking in the world of ping pong, I call each process a player. We have different players, rank 0 and 1 which play the game and the other ranks which are idle. So to avoid nested if-conditions, I created `IPlayer` interface:

```cpp
struct IPlayer
{
    virtual void Play()=0;
};
```

## Idle 

`IPlayer` is adopted by the `Idle` class which does nothing


```cpp
struct Idle: IPlayer
{
    void Play() override{};
};
```

## Player

The players of the game adopt the same interface. The constructor of `Player`  needs to set some private members like who is the starter of the game. If the player's rank is 0 its target is 1 and vice versa. 

```cpp
struct Player: IPlayer
{
    Player(Ball& _ball, bool _iAmGameStarter): 
        ball(_ball), iAmGameStarter(_iAmGameStarter){
        
        MPI_Comm_rank(MPI_COMM_WORLD, &rank);
        MPI_Comm_size(MPI_COMM_WORLD, &size);

        // At least 2 processors needed
        if (size<2){throw;}

        target = (rank + 1) % 2;
    };
    // ... rest of the code
}
```

A player sends the ball and waits to receive it back. I used `MPI_Send` to send the ball in a blocking way. It will receive the ball using `MPI_Recv` which blocks the process until the ball buffer is reusable. Both block the buffer, the ball, to make sure there is not a race condition to read and write there. For more information, read more on [the MPI race condition here](https://iamsorush.com/posts/mpi-race-condition/).  

```cpp
    void SendBall(){
        MPI_Send( ball.Data , ball.Size , MPI_INT , target , 0 , MPI_COMM_WORLD);
    }
    void RecvBall(){
        MPI_Recv( ball.Data, ball.Size , MPI_INT, target, 0 , MPI_COMM_WORLD, &stat);
    }
```

I have to override `Play` of the interface. It basically calls `SendBall()` and `RecvBall()` in the order depending on who's started the game. After each player receives the ball, they increment `Data[0]` by one, firstly to count communications and secondly to show the program works fine.  

```cpp

    void Play() override{
        if (iAmGameStarter) SendBall();
        RecvBall();
        ball.Data[0]++;
        cout<< "Rank :" << rank <<" has the ball, No of throws: "
            << ball.Data[0] <<endl;
        if (!iAmGameStarter) SendBall();
    }
```



## Code

The whole code is here.

```cpp
#include <mpi.h>
#include <stdio.h>
using namespace std;

struct Ball
{
    Ball(int size){
        Data = new int[size];
        Data[0] = 0;
        Size = size;
    }
    int* Data;
    int Size;
};

struct IPlayer
{
    virtual void Play()=0;
};

struct Idle: IPlayer
{
    void Play() override{};
};

struct Player: IPlayer
{
    Player(Ball& _ball, bool _iAmGameStarter): 
        ball(_ball), iAmGameStarter(_iAmGameStarter){
        
        MPI_Comm_rank(MPI_COMM_WORLD, &rank);
        MPI_Comm_size(MPI_COMM_WORLD, &size);

        // At least 2 processors needed
        if (size<2){throw;}

        target = (rank + 1) % 2;
    };
    
    void SendBall(){
        MPI_Send( ball.Data , ball.Size , MPI_INT , target , 0 , MPI_COMM_WORLD);
    }
    void RecvBall(){
        MPI_Recv( ball.Data, ball.Size , MPI_INT, target, 0 , MPI_COMM_WORLD, &stat);
    }
    void Play() override{
        if (iAmGameStarter) SendBall();
        RecvBall();
        ball.Data[0]++;
        cout<< "Rank :" << rank <<" has the ball, No of throws: "<<ball.Data[0]<<endl;
        if (!iAmGameStarter) SendBall();
    }
    
private:
    Ball& ball;
    int rank;
    int size;
    int target;
    bool iAmGameStarter;
    MPI_Request req;
    MPI_Status stat;
};


int main() {

    MPI_Init(NULL, NULL);

    int rank;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);

    // Customize here
    int ballSize = 1000000;
    int warmupIterations = 0;
    int mainIterations = 3;

    Ball ball(ballSize);

    IPlayer* player;

    // Only rank 0 and 1 play the game
    if (rank==0){
        // Rank 0 starts the game
        player = new Player(ball, true);
    } else if (rank==1)
    {
        player = new Player(ball, false);
    } else
    {
        player = new Idle();
    }
    
    // Warm up players before the game
    for (size_t i = 0; i < warmupIterations; i++)
    {
        player->Play();
    }

    double start = MPI_Wtime();
    // Main loop to be monitored
    for (size_t i = 0; i < mainIterations; i++)
    {
        player->Play();
    }
    double end = MPI_Wtime();

    auto elapsedTime = end-start;
    // each iteration has 2 transfers: send and receive
    auto transferTime = elapsedTime/(mainIterations * 2);
    auto ballSizeInGigaByte = ballSize * 4.0 /* byte */ / 1000000000;

    if (rank==0) 
    {
        cout<< "Ball size (GB): "<< ballSizeInGigaByte<<endl;
        cout<< "Transfer time (Sec): "<< transferTime <<endl;
        cout<< "Bandwidth (GB/s): " << ballSizeInGigaByte/transferTime <<endl;
    }
    
    MPI_Finalize();
}
```
## Validation 

The first run is only 3 iterations to see how the ball moves back and forth. In all tests, only 2 processes were utilized.

``` cpp
BallSize = 1000,000
main iterations = 3
warm up iterations = 0

Rank :1 has the ball, No of throws: 1
Rank :0 has the ball, No of throws: 2
Rank :1 has the ball, No of throws: 3
Rank :0 has the ball, No of throws: 4
Rank :1 has the ball, No of throws: 5
Rank :0 has the ball, No of throws: 6
```

## Bandwidth

The second run is to measure the bandwidth:


```cpp
BallSize = 1000,000
warm up iterations = 10
iterations = 10,000

Ball size (GB): 0.004
Transfer time (Sec): 0.000531798
Bandwidth (GB/s): 7.52166
```


## References

I got ideas and codes from the below website(s)

[OpenMPI](https://www.open-mpi.org/doc/v4.0/)
[EPCC MPI Exercise](https://www.archer.ac.uk/training/course-material/2017/08/mpi-exeter/exercises/MPP-exercises.pdf)
[OLCF-tutorials](https://github.com/olcf-tutorials/MPI_ping_pong)
[Boost MPI](https://www.boost.org/doc/libs/1_74_0/doc/html/mpi.html#mpi.introduction)
[MPI Deprecated the C++ bindings](https://github.com/mpi-forum/mpi-forum-historic/issues/150)
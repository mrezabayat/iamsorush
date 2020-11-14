---
title: "MPI ping pong program using C++"
date: 2020-11-14T10:30:30+01:00
image: /images/camerastand.webp
thumbnail: /images/camerastand_tn.webp
tags: ["MPI", "C++"]
categories: "Diverse"
summary: "I want to write an MPI ping pong program where two processes send a piece of data back and forth to each other."
---

## Goal

I want to write an MPI ping pong program where two processes send a piece of data back and forth
to each other. This is a good example to measure the latency and bandwidth of a cluster machine. 

## The ball

If we imagine the data transfer between two nodes is like a ping-pong game, the data is the ball.
The ball can be an array of MPI types. Here for simplicity, is an integer:

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

In this example, I don't care exactly what is in `Data` array except 0-th element which counts the number of forths and backs of the ball.

## IPlayer

As I am still in the world of ping pong, I call each process a player. We have different players, rank 0 and 1 which play the game and the other ranks which are idle. So to avoid nested if-conditions, I created `IPlayer` interface:

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

A player sends the ball and waits to receive it back. I used MPI_Isend to send the ball in a non-blocking way. But it will receive the ball using MPI_Recv which blocks the process until the ball is back. 

```cpp
    void SendBall(){
        MPI_Isend( ball.Data , ball.Size , MPI_INT , target , 0 , MPI_COMM_WORLD ,  &req);
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
        MPI_Isend( ball.Data , ball.Size , MPI_INT , target , 0 , MPI_COMM_WORLD ,  &req);
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
    int ballSize = 2;
    int iterations = 3;

    Ball ball(ballSize);

    // player can be Idle or Player 
    IPlayer* player;

    // setup players
    if (rank==0){
        // Rank 0 starts the game
        player = new Player(ball, true);
    } else if (rank==1)
    {
        // Rank 1 is the first receiver
        player = new Player(ball, false);
    } else
    {
        // The other ranks do nothing
        player = new Idle();
    }
    
    // Start measuring time in MPI world
    double start = MPI_Wtime();

    // Loop of the game
    for (size_t i = 0; i < iterations; i++)
    {
        player->Play();
    }
    
    // Meaure when the game ended
    double end = MPI_Wtime();

    if (rank==0) cout<<"elapsed time: "<< end-start <<endl;

    
    MPI_Finalize();
}
```
## More



## References

I got ideas and codes from the below website(s)

[OpenMPI](https://www.open-mpi.org/doc/v4.0/)
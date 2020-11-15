---
title: "MPI race condition"
date: 2020-11-15T19:22:30+01:00
image: /images/race.webp
image_v: /images/race_v.webp
thumbnail: /images/race_tn.webp
tags: ["MPI", "C++"]
categories: "Diverse"
summary: "When a buffer, which is involved in an uncompleted non-blocking communication, is used in another communication, there will be a race to read and write the buffer."
---

## Definition

When a buffer, which is involved in an uncompleted non-blocking communication, is used in another communication, there will be a race to read and write the buffer. The outcome of this situation is undefined. That is why the MPI standard states that a buffer must not be reused unless its communication is completed. It might look acceptable that multiple communications only read a buffer, however, it is still illegal in the MPI.

## Example  

In the example below, process 0 sends `buff0` in a non-blocking way to another process, it immediately moves forward to fill the buffer with data coming from another process. `MPI_Isend` can complete before, during or after the MPI_recv, therefore there is a race of reading and writing on `buff0`. To avoid this, we have two solutions: first using different buffers for `MPI_Isend` and `MPI_Recv`, and second, waiting for `MPI_Isend` to complete with the aid of `MPI_Wait`.

{{< rawhtml >}}
<div style="text-align:center;">
<img src="/images/mpi-race.png" />
</div>
{{< /rawhtml >}}


 

## Always check non-blocking communication

Let’s modify the previous example in a way that after `MPI_Isend` a very time-consuming task happens. Let’s say we are sure that `MPI_Isend` has time to  complete during the task, is it OK to reuse the buffer in another communication afterward? Nope, we **Must** check the completion of `MPI_Isend` using MPI_Wait or MPI_Test. 

{{< rawhtml >}}
<div style="text-align:center;">
<img src="/images/mpi-race2.png" />
</div>
{{< /rawhtml >}}

## Code

Let’s create a code to examine the previous rule. Rank 0 sends `buffer=2` to rank 1 which receives it using `MPI_Irecv`. Then the threads are put in sleep for 2 seconds to mimic a time-consuming task. 

```cpp
#include <mpi.h>
#include <chrono>
#include <thread>
#include <stdio.h>
using namespace std;
 
int main(){
   MPI_Init(NULL, NULL);
  
   int rank;
   MPI_Comm_rank(MPI_COMM_WORLD, &rank);
 
   MPI_Request req;
   MPI_Status stat;
 
   int sendbuf = 2;
   int recvbuf = 3;
 
   if (rank == 0){
       MPI_Isend( &sendbuf, 1, MPI_INT, 1, 0, MPI_COMM_WORLD, &req);
       std::this_thread::sleep_for(std::chrono::milliseconds(2000));
       cout<< "Rank"<< rank<< " sendbuf="<< sendbuf<< endl;
   }
   if (rank==1){
       MPI_Irecv( &recvbuf, 1, MPI_INT, 0, 0, MPI_COMM_WORLD, &req);
       std::this_thread::sleep_for(std::chrono::milliseconds(2000));
 
       int result = 0;
      // MPI_Test( &req, &result , &stat);
       cout<<"Rank"<< rank <<
           " recvbuf="<< recvbuf <<
           " success:"<< (result?"Yes":"No")
           <<endl;
   }
  
   MPI_Finalize();
}
 
 ```

We expect within two seconds the data transfer happens, and the content of `recvbuf` to be 2, but we see the below outcome:

```
Rank0 sendbuf=2 
Rank1 recvbuf=3 success:No
```

Now we uncomment the `MPI_Test` line, and run the code, we get

```
Rank0 sendbuf=2
Rank1 recvbuf=2 success:Yes
```


Therefore, always call `MPI_Test` or `MPI_Wait` before reusing the buffer of  non-blocking communications without any exception.


## References

I got ideas and codes from the below website(s)

[OpenMPI](https://www.open-mpi.org/doc/v4.0/)
[CodingGame](https://www.codingame.com/playgrounds/349/introduction-to-mpi/race-conditions)
[Stackoverflow](https://stackoverflow.com/questions/10017301/mpi-blocking-vs-non-blocking)



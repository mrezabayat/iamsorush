---
title: "The difference between modes of MPI send"
date: 2020-11-09T21:46:00+01:00
image: /images/message.jpg
imageAnchor: "Center"
tags: ["MPI"]
categories: "Diverse"
summary: "There are different modes of *MPI send*: MPI_Send, MPI_Isend, MPI_Ssend, MPI_Bsend, and so on. They can be local or non-local, blocking or non-blocking, and synchronous or asynchronous. Their definition and differences are explained here in detail. "
---

## Introduction

There are different modes of *MPI send*: MPI_Send, MPI_Isend, MPI_Ssend, MPI_Bsend, and so on. They can be local or non-local, blocking or non-blocking, and synchronous or asynchronous. Their definition and differences are explained here in detail.


## MPI_Send

This is the **standard** mode. When it is called, (1) the message can be directly passed to the receive buffer, (2) the data is buffered (in temporary memory in the MPI implementation) or (3) the function waits for a receiving process to appear. See the picture below.
Therefore, It can return quickly (1)(2) or block the process for a while. MPI decides which scenario is the best in terms of performance, memory, and so on. 
In any case, the data can be safely modified after the function returns. 

{{< rawhtml >}}
<div style="text-align:center;">
<img src="/images/mpi_send.png" style="max-width:100%;" />
</div>
{{< /rawhtml >}}


## MPI_Ssend

It is the **synchronized** blocking function. When this function returns, the destination has started receiving the message. The moment the destination starts receiving, it signals an *ACK* to the source.


{{< rawhtml >}}
<div style="text-align:center;">
<img src="/images/mpi_ssend.png" style="max-width:100%;" />
</div>
{{< /rawhtml >}}

Note, the signal of receiving the message is the difference between `MPI_Ssend` and `MPI_Send`. 


## MPI_Bsend

It is the local blocking send. The programmer defines a **local buffer** that when this function is called. If there is not a matching receive available, the process is blocked until the message is copied into the buffer. Therefore, the coder can immediately modify the source data after the function returns. 

{{< rawhtml >}}
<div style="text-align:center;">
<img src="/images/mpi_bsend.png" style="max-width:100%;" />
</div>
{{< /rawhtml >}}

Note, when the function returns the message is probably not sent yet, it will happen concurrently in the background of the process when a matched receive is found.

## MPI_Rsend

It is a blocking function the same as MPI_Send, but, it expects a **ready destination** to receive the message. This can increase the MPI performance if the programmer is sure there is a receive function waiting for this. If no receive posted before, it is erroneous.

## MPI_Isend

It is the non-blocking version of `MPI_Send`. When this function is called the function returns immediately but runs `MPI_Send` actions in the background of the process.  Therefore, After the function returns, the data **must not** be modified unless `MPI_Test` and `MPI_Wait` confirm `MPI_Isend` is completed. After the completion, the data is reusable because it either is buffered in MPI or sent to the destination.   

{{< rawhtml >}}
<div style="text-align:center;">
<img src="/images/mpi_isend.png" style="max-width:100%;" />
</div>
{{< /rawhtml >}}

## MPI_Issend

It is the non-blocking version of `MPI_Ssend`. It returns immediately, but runs `MPI_Ssend` actions in the background.  `MPI_Test` or `MPI_Wait` **must** be used to assess if the function is completed in the background. At that point, not only the message has been sent but also the destination has started to receive the message.

{{< rawhtml >}}
<div style="text-align:center;">
<img src="/images/mpi_issend.png" style="max-width:100%;" />
</div>
{{< /rawhtml >}}

## MPI_Ibsend

 This is the local non-blocking send. It blocks for neither copying the message to the buffer nor sending the message. After the test positive or wait, we can modify the source data because, if it is not sent, it is locally copied to the allocated buffer.

 {{< rawhtml >}}
<div style="text-align:center;">
<img src="/images/mpi_ibsend.png" style="max-width:100%;" />
</div>
{{< /rawhtml >}}

## MPI_Irsend

The same as `MPI_Rsend`, but non-blocking. 

## Priority list

It's hard to give a recipe for all the problems. However, some points can help to choose:

- When there is a **deadlock**, non-blocking communication can help.
- When there is a [**race condition**](https://iamsorush.com/posts/mpi-race-condition/), blocking communication can help.
- When there is a **computationally expensive** task, a non-blocking communication, posted before the task, may improve the performance.
- `MPI_Send` and `MPI_Isend`, are **top** in the priority list as MPI decides what is best.
- `MPI_Ssend` and `MPI_Issend`, when the sender needs to know **when** the message is received and to avoid local buffering.
- `MPI_Bsend`, `MPI_Ibsend`, `MPI_Rsend`, `MPI_Irsend` are for **fine-tuning** the performance.


## References

I got ideas and codes from the below website(s)

[MPI 3.1 Report - section 3.4, 3.7](https://www.mpi-forum.org/docs/mpi-3.1/mpi31-report.pdf)



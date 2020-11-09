---
title: "The difference between modes of MPI send"
date: 2020-11-09T21:46:00+01:00
image: /images/envelop.webp
image_v: /images/envelop_v.webp
thumbnail: /images/envelop_tn.webp
tags: ["MPI"]
categories: "Diverse"
summary: "There are different modes of MPI send which are explained here. Firstly, MPI_Send, MPI_Isend and MPI_Ssend
are described which are popular ones, then the others are mentioned. "
---

## Introduction

There are different modes of *MPI send* which are explained here. Firstly, `MPI_Send`, `MPI_Isend` and `MPI_Ssend`
are described which are popular ones, then the others are mentioned. 


## MPI_Send

When this function is called, the data is either buffered (in the sender or receiver process) or the function waits for a receiving process to appear. 
Therefore, It can return quickly or block the program from moving to the next line. MPI decides what scenario is the best in terms of performance, memory, and so on. 
In either case, the data can be safely changed or reused after the function returns. 


## MPI_Isend

When this function is called, the message is not buffered, the function returns immediately and Program runs the next line of code. However, the function continues running in the background waiting for a matching receive. When it finds it, it passes the source data. Therefore, After the function returns, the data must not be reused or changed unless we are sure the message is received.
`MPI_Test` and `MPI_Wait` are usually used with `MPI_Isend`. 

## MPI_Ssend

It is the synchronized blocking function. It means when this function returns, the destination has received the message. 

Note, a guarantee of receiving the message is the difference between `MPI_Ssend` and `MPI_Send`. Because when `MPI_send` returns there is a chance the message is only buffered and the destination has not received the message yet.

## MPI_Bsend

It is the asynchronous blocking send. The programmer defines a buffer that when this function is called, the program is blocked until the message is copied into the buffer. Therefore, the coder can immediately reuse or change the source data after the function returns. 

Note, when the function returns the message is not sent yet, it will happen in the background when a matched receiver is found.

## MPI_Rsend

It is a blocking function the same as MPI_Send, but, it expects the destination process has been ready to receive the message. 

## MPI_Ibsend

 This is the asynchronous non-blocking send. It doesn't block for either copying the message to the buffer or sending the message.

## MPI_Issend

It is the synchronous nonblocking send. It returns immediately regardless of the message being sent.

## MPI_Irsend

The same as `MPI_Rsend`, but nonblocking.

## References

I got ideas and codes from the below website(s)

[MPI 3.1 Report - section 3.4](https://www.mpi-forum.org/docs/mpi-3.1/mpi31-report.pdf)



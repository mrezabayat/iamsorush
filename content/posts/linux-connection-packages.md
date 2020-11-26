---
title: "Handy cross-platform packages to connect to a remote Linux server"
date: 2020-11-11T21:30:30+01:00
image: /images/tools.jpg
tags: ["Linux", "Ubuntu"]
categories: "Diverse"
summary: "Interaction with a remote Linux server like transferring files, editing code, or accessing the remote desktop can be much easier with these free cross-platform packages."
---

## Intro

To download or upload files from/into a Linux server, edit code, work with desktop, or install applications remotely, some cross-platform - *Windows, Mac, Linux* - packages can be really helpful. Here, I talk about my favorites. I assume the Linux system has an SSH server like [OpenSSH](https://www.openssh.com/) installed.


## PuTTy

[PuTTy](https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html) can connect via SSH to a remote system. You just need to insert the IP of the remote computer and your credentials to have access to a Linux terminal. It can also be used for port forwarding. 

If you just one to edit some files containing text or code on the remote machine, make sure **Vim** or **nano** are installed on the remote machine. They both are terminal code editors which have syntax highlighting, search-and-replace capabilities, and so on. Vim takes more time to learn, but when you master it probably you cannot live without it. 


## X2Go 

If you like to visually see the desktop of a remote Linux system, [X2Go](https://wiki.x2go.org/doku.php) is the solution. It has server and client packages. You have to install the server package on the remote computer and client one on your local system. 

From my experience, the *Unity* desktop of Ubuntu doesn't work with X2Go. However, *Mate* desktop works flawlessly. So, if you have Ubuntu install *Mate* for X2Go.

Note that X2Go only uses the CPU of your remote, so it is not a good option for gaming or watching high-quality videos.

Using X2Go, many users can connect to a Linux server having independent desktops.



## FileZilla

If you are interested to see directories and files visually, create, copy, cut, delete, drag and drop them, FileZilla is the best. It is used mainly to connect to FTP servers. But by creating an SFTP profile, you can see the content of a remote Linux storage from a local system.

## NoMachine

This is another remote desktop solution which uses NX protocol. [NoMachine](https://www.nomachine.com/) uses the remote machine GPU to render the desktop. So, if you need the remote desktop to render heavy duty images like 3D CADs on a high-performance GPU, this is the way to go. 

NoMachine is only free for one user using one server. Moreover, it cannot create multiple independent desktops for different users, in contrast to X2Go. I think it is a hardware issue that unlike CPU, GPU can not be easily shared among multiple users. Therefore, even you buy an enterprise license of NoMachine, multiple users can access only one shared desktop on the server.


## Visual Studio Code

If you aim to develop code on a remote Linux machine, [Visual Studio Code](https://code.visualstudio.com/) (VS Code) is a swiss army knife. It is a free open-source code editor that supports syntax highlighting, intelligent code completion (IntelliSense), debugging, Git, and many more features. VS Code can connect to a remote machine via SSH and open a remote folder as a workspace, [see the instruction here](https://code.visualstudio.com/docs/remote/ssh#_connect-to-a-remote-host). After a successful connection, the whole experience is  more enjoyable and productive in comparison with terminal editors like Vim and nano. Moreover, if you are a Vim lover, you can install a Vim extension on VS Code.






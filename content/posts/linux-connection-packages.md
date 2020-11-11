---
title: "Handy free Windows packages to connect to a remote Linux server"
date: 2020-11-11T21:30:30+01:00
image: /images/tools.webp
image_v: /images/tools_v.webp
thumbnail: /images/tools_tn.webp
tags: ["Linux", "Ubuntu"]
categories: "Diverse"
summary: "To download or upload files from/into a Linux server, or work with a remote desktop, some free Windows packages can be really helpful."
---

## Intro

To download or upload files from/into a Linux server, work with desktop, or install applications remotely, some free packages can be really helpful. Here, I talk about my favorites. I assume the Linux system has an SSH server like [OpenSSH](https://www.openssh.com/) installed.


## PuTTy

[PuTTy](https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html) can connect via SSH to a remote system. You just need to insert the IP of the remote computer and your credentials to have access to a Linux terminal. It can also be used for port forwarding. 


## X2Go 

If you like to visually see the desktop of a remote Linux system, [X2Go](https://wiki.x2go.org/doku.php) is the solution. It has server and client packages. You have to install the server package on the remote computer and client one on your Windows system. 

From my experience, the *Unity* desktop of Ubuntu doesn't work with X2Go. However, *Mate* desktop works flawlessly. So, if you have Ubuntu install *Mate* for X2Go.

Note that X2Go only uses the CPU of your remote, so it is not a good option for gaming or watching high-quality videos.

Using X2Go, many users can connect to a Linux server having independent desktops.



## FileZilla

If you are interested to see directories and files visually, delete, drag and drop them, FileZilla is the best. It is used mainly to connect to FTP servers. But by creating an SFTP profile, you can see the content of a remote Linux storage from a Windows system.

## NoMachine

This is another remote desktop solution which uses NX protocol. [NoMachine](https://www.nomachine.com/) uses the remote machine GPU to render the desktop. So, if you need the remote desktop to render heavy duty images like 3D CADs on a high-performance GPU, this is the way to go. 

NoMachine is only free for one user using one server. Moreover, it cannot create multiple independent desktops for different users, in contrast to X2Go. I think it is a hardware issue that unlike CPU, GPU can not be easily shared among multiple users. Therefore, even you buy an enterprise license of NoMachine, multiple users can access only one shared desktop on the server.




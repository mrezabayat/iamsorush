---
title: "SSH port forwarding to download files"
date: 2021-04-18T14:10:20+01:00
image: /images/port.jpg
imageQuality: "q65"
imageAnchor: "bottom" # Smart, Center, TopLeft, Top, TopRight, Left, Right, BottomLeft, Bottom, BottomRight.
tags: ["Linux"]
categories: "Diverse" 
summary: "I want to download files from a destination computer connected to a public SSH server. The destination is accessible only via the server by SSH tunnel."
---

## Intro

I want to download files from a remote computer (**destination**), into my laptop (**client**). The remote computer is not accessible directly. I first have to SSH to a **server** then, from that server, SSH to the destination computer. 

{{< img "*ssh*" "ssh to remote computer" >}}


So my usual procedure to connect to the destination is to open a Linux terminal and write

```bash
ssh myUserName@serverAddress
```
Inserting the password, I am in the server terminal. I run

```bash
ssh destinationAddress
```
and I am in the destination terminal. I can do whatever I want there. 

Note the server and destination addresses are in the form of either IPs or names. The server address is public and accessible from anywhere, but the destination address is local to the server network.

Now how can I download files from the destination to my laptop? read the next section.

## Portforwarding

The idea is to set a port on my laptop to point to a port on the destination computer. The SSH command is:

```bash
ssh -L aLaptopPort:destinationAddress:destinationPort myUsername@serverAddress
```

Because we are going to download files through ssh, I forward `port 22` of the destination. 

To find listening ports on my laptop, I run the below command in the terminal:

```bash
sudo netstat -tulpn | grep LISTEN
```
So I choose a port that is not on the list. I usually use port 5901.

So the port forwarding command becomes like

```bash
ssh -L 5901:destinationAddress:22 myUsername@serverAddress
```

After inserting the password, you should be in the server terminal. Now port `5901` of my laptop points to port `22` of the destination. I leave the terminal open but we do not work with it.

To check the port is forwarded, in another terminal on my laptop I can run the `netstat` command above.

## Download files

To download files I use [FileZilla](https://filezilla-project.org/download.php?type=client). Go to File->Site Manager. Push *New site* button. In the *General* tab, fill the fields like the picture below:

{{< img "*sitemanager*" "site manager window" >}}


and finally, press *Connect*. Insert the password and you should see the files and folders of the destination in FileZilla. 

{{< img "*files*" "files and folders window" >}}


The rest is easy, dragging files from the right window (destination) and dropping them in the left window (my laptop).


## More

Here I use Linux Ubuntu but you can do the same on Windows with [PuTTY](https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html) or PowerShell. 

The technique explained here can be used to connect to a remote printer, desktop and so on.

If you like this article, you may like this article too: [Handy cross-platform packages to connect to a remote Linux server](https://iamsorush.com/posts/linux-connection-packages/).

















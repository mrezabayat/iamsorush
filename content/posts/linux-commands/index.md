---
title: "Essential Linux commands to know"
date: 2021-05-19T18:10:20+01:00
image: /images/dog.jpg
imageQuality: "q65"
imageAnchor: "Center" 
tags: ["Linux"]
categories: "Diverse" 
summary: "Here, I picked essential Linux commands, you need to know to use a Bash terminal: navigation, copy, delete, variables, aliases, and so on."
---


Here, I gather useful Linux commands that you need know to work with a Bash terminal.

## Navigation


Change current directory with `cd` command:

```Bash
cd /home
```

I highly recommend installing `zsh` instead of Bash. In `zsh`, you don't need to write `cd`, only the name of the directory takes you there. Here, I assume you don't use `zsh`.

Go one folder up, or to parent directory with `..`

```Bash
cd /home/sorush
# we are at /home/sorush
cd ..
# we are at /home/
```
And `.` means the current directory, it doesn't do anything with `cd` command.

we can mix `..` with the absolute path:

```bash
cd /home/sorush/../../home/sorush/../.
# we are at /home
```

Two useful shortcuts are 
* `~` : home folder, where current user's files reside
* `-` : previous folder

```Bash
cd /
cd ~
# we are at /home/sorush
cd -
# we are back to /
```

Get current directory address using the print-working-directory command :

```Bash
pwd
``` 
## Create file

Create an empty file via

```bash
touch myFile.txt
```

If you are a `vi`/`vim` user, 

```bash
vim myFile.txt
```
opens `vim`. When you save your changes, the file is created.

## See file content

To print all the content of a file on screen

```bash
cat myFile.txt
```

To browse up and down in an interactive way, use

```Bash
less myFile.txt
# or
more myFile.txt
```

`vim` and `nano` are two popular text editors in Bash which can also be used for viewing the content of files.

## Read live logs

To see the live updates to a log file that is being written by a program, run

```bash
tail -f logFile
```

* `-f`: follow updates

If `-f` is dropped, you see only the last 10 lines of the file at the moment you press Enter. 


## Directory

Create a directory with

```Bash
mkdir nameOfDirectory
```

Get content of a directory with the list command
```Bash
ls -al /home
```

* `-a`: show everything 
* `-l`: show details. 

You can drop `-al` to see the difference. If you drop the destination folder, it shows the content of the current directory. 



To show a tree-like list of content:

```bash
tree -d -L 2
```

* `-d`: show only directories
* `-L 2`: show only 2 layers of subdirectories

On some Linux distros `tree` is not available by default, you have to install it.


Get the size of a directory (I read it "dush"):

```Bash
du -sh ~/myFolder
```

* `-h`: human-readable like MegaByte (M), GigaByte (G)
* `-s`: to hide subdirectories.


## Print to file

To write the output of a command into a file, use `>` followed by the name of the file:

```bash
ls > myFile.txt
```
Nothing will be shown in the terminal.

## Copy file

A file in the current folder can be copied into another folder

```bash
cp myfile.txt ~/myfolder/
```
A folder can be copied into another place:

```bash
cp -r ~/myfolder ~/anotherFolder 
```
* `-r`: copy the folder and everything inside (Recursive) 

Note `cp` command overwrites existing files without any question.

## Move file

Move command is to copy a file/folder to another place and delete the original file/folder. It is equivalent to cut-paste in Windows and copy-move in Mac.

A file can be moved to a new folder via:
```bash
mv myfile.txt ~/myfolder
```

A folder can be moved into another folder:

```bash
mv ~/myfolder ~/anotherFolder 
```

## Rename file

The move command is used for renaming a file

```Bash
mv myfile.txt info.csv
```
or renaming folder:

```Bash
mv ~/myfolder ~/Simulation01
```

So when using `mv` command, if the destination folder exists, cut-paste happens, otherwise, the current folder is renamed to the destination folder.

## Remove file

To remove a file or directory 

```bash
rm ./myFileOrFolder -rf
```
* `-r` : recursively delete i.e. removes everything including subfolders and files in them. This is what happens when we delete a folder in Windows or Mac. This is not necessary for files.

* `-f` : Use forced deletion i.e. `rm` will remove all the files without any confirmation, even if the files are write-protected. 

## Sudo

Add it before any command to be run as a superuser (admin). You will be requested for your admin password. For example, to install an application on Ubuntu you need to have sudo privilege:

```Bash
sudo apt install tree
```

Changing and deleting sensitive system folders needs a superuser.

## Search for file

You can find a file in the current directory and its subdirectories via

```Bash
find . -name "*.txt"
```

* `*`: wildcard for any `txt` file. 

You can also put the exact name there.



## History

To get a list of all the commands you've used so far,  run
```Bash
history
```
the result is two columns, the first column is the ID of command and the second is the command like

```
  316  cd /home/sorush/../../home/sorush/../.
  317  cd /
  318  cd ~
  319  pwd
```

To run command again, use `!`+ID of the command:
```bash
!319
# will run pwd
```

To run the last command, use `!!`. Here I run the last command with `sudo`:

```bash
sudo !!
```

## Grep via pipes

Using `grep`, we can filter the outcome of a command. For example, we want to filter the outcome of `history` command to only show the ones that contain `ssh` word:

```Bash
history | grep ssh
```

or list the files of the current directory but only show text files

```bash
ls | grep .txt
```

## Variables

We can set a variable in Bash by 

```Bash
nameOfVariable=TheContentOfVariable
```
We store a text in a variable. If there are spaces in the content, use quotations:

```Bash
nameOfVariable="The Content Of Variable"
```

The content is usually a path to a file or folder:


```Bash
destination=/home/sorush/documents
```

The variable is called with `$` sign.
Use `echo` to see the content of a variable

```Bash
echo $destination
```

We can use the variable in any Bash command:

```Bash
cd $destination
cp myFile.txt $destination
```

Store the outcome of a command into a variable :

```sh
aVariable=`aCommand`
```
for example:

```bash
address='pwd'
```


## Environment variables

If a variable is needed to be available inside every program, we use `export` command to make it an environment variable:

```Bash
export variable=Content
```

For example, CMake reads `CC` environment variable to find *C* compiler path. In a terminal, we can set it as:

```Bash
export CC=/usr/local/gcc-11.1.0/bin/gcc
```

We can see all the environment variables defined, with the command
```bash
env
```

A good place to define environment variables is `~/.bashrc` in Ubuntu or `~/.zshrc` for Z-shell.

To have an executable available in every working directory, add its folder to `PATH` 

```Bash
export PATH="/home/shared/bin:$PATH"
```

To have a library accessible by compilers, add its folder to `LD_LIBRARY_PATH`:

```Bash
export LD_LIBRARY_PATH="/home/vtk6.3/lib:$LD_LIBRARY_PATH"
```


## Alias

To create a custom command, we use alias. See some of aliases I use in my terminal:

```Bash
alias hgrep="history | grep"
alias lgrep="ls | grep"
alias current='cd "/home/sorush/test program"'
alias brc="vim ~/.bashrc"
alias zrc="vim ~/.zshrc"
alias dirsize="du -sh"
alias unicomputer="ssh sorush@xxxx.xxx.xx"
```

So we can do this:

```Bash
hgrep ssh
# equals to history | grep ssh
```
A good place for aliases is `~/.bashrc` in Ubuntu.
We can see all the aliases defined in a terminal by running 

```Bash
alias
```


## System info

Get the list of disks and their free space with **disk free** command

```Bash
df -h
```

* `-h`: human-readable.

Get memory usage by

```Bash
free -h
```

Get the list (ls) of CPUs (cpu) and their info with

```Bash
lscpu
```

Get a list of running processes similar to Windows Task Manager with

```Bash
top
```

I recommend using `htop`, it looks much nicer than `top`:

```Bash
htop
```

But usually `htop` is not available, and you have to install it by yourself.


## Clear & Exit

You can clear the terminal with

```Bash
clear
```
You can press `ctrl+l` to do the same.

You can exit a terminal by:

```Bash
exit
```


## Stop a process

Press `ctrl+c` to kill a process running in the current terminal:

```Bash
# takes 5 seconds to finish
sleep 5 
# press ctrl+c before it finishes
```
To stop an application (or process) that is running in the background or another terminal: 

```Bash
killall nameOfapplication
```

Another way is to first get the ID of the application:

```Bash
pidof nameOfapplication
```
You can also use `top` or `htop`. Then stop it using its ID

```Bash
kill idOfApplication
```


## Extract tar.gz

`tar.gz` is a very popular format for compressed files in Linux. You can extract them via:

```Bash
tar -xvf myFile.tar.gz
```
* `-x`: extract 
* `-v`: verbosely
* `-f`: file 

The same works for `.tar.bz2` files. 

## Clipboard Copy-paste 

Sometimes you want to copy a text from the terminal into the Linux clipboard, and then paste it somewhere else, for example in a Word document. This is what I do in Ubuntu: 

* **Copy**: select a text with the mouse and press `ctrl+shift+c` to copy it. 
* **Paste**: paste the clipboard content into a terminal with `ctrl+shift+v`. 

You can also do both of the above with right-click on a terminal.

## Terminal cut-paste

Write a line in a terminal and move the cursor to the center:

* ctrl+k: cut everything after the cursor (I say Knock)
* ctrl+u: cut everything before the cursor (I say Up)
* ctrl+y: paste what cut before (Yank)

## Jump cursor

Jump cursor:

* ctrl+a: to the begining of the line (Arch)
* ctrl+e: to the end of the the line (End)


## Permissions

You can change who is eligible to read/write/execute a file using `chmod` command. There are a lot of details there but a few useful tricks are mentioned here.

Make a file executable:
```bash
chmod +x nameOfTheFile
```

Make a file/folder to be read/written/executed by only you (a private file)

```bash
chmod 700 nameOfTheFile
```

Make a file available to every user (a shared file) 
```bash
chmod 777 nameOfTheFile
```

## Background process

Sometimes you want to run a command that takes a lot of time like copying huge files and in the meantime, you want to do other stuff. You can run the time-consuming task in the background of the terminal by adding `&` to it: 

```Bash
# A CPU sleeps 20 seconds
sleep 20 &
```

You can see the list of all processes in the background via 
```Bash
jobs
# [1]  + running    sleep 20
```
You can kill the process with its job id

```bash
# Note the % sign
kill %1
```


If you want to run a program, for example, a GUI program, from a terminal but you want them to be detached. In other words, if you close the terminal, the GUI program is still running, use `nohup`:

```Bash
nohup paraview & 
```

The window of Paraview will be opened and detached from the terminal. All the messages Paraview want to send to the terminal are redirected to `nohup.out` file.



## Download 

You can download a file from the internet by knowing its download link:

```Bash
wget urlOfFile
```

## Manual

Before jumping to google to understand a Linux command, try the `man` command. It may explain them better:

```Bash
man ls
man cp
man history
```


## Find executables

Some executables are in the system path. You run them without you know where they reside.
To know where the binary, source and manual of command are, run:

```bash
whereis ls
whereis history
whereis gcc
```

If you just want to know the address of the binary of a command, use

```bash
which cp
which ls
which gcc
```
## symlink

A symbolic link or symlink is a file that refers to another file or folder. It is similar to a shortcut in Windows.

To create a link file from an existing file, run 
```Bash
ln -s ExistingFile LinkFile
```
See this example:

```bash
# create a new file
touch myFile.txt
# create a symlink to it
ln -s myFile.txt linkToMyFile.txt 
```
Now any change to the content of `linkToMyFile.txt` is applied to `myFile.txt`. 

Note symlinks can be also created for folders. 


If you create a symlink to an executable, running the symlink is the same as running the executable. 


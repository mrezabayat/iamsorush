---
title: "Python for file management instead of Bash"
date: 2021-06-05T09:10:20+01:00
image: /images/python.jpg
imageQuality: "q65"
imageAnchor: "Center" # Smart, Center, TopLeft, Top, TopRight, Left, Right, BottomLeft, Bottom, BottomRight.
tags: ["Linux", "Python"]
categories: "Diverse" 
summary: "I show how Bash file management can be replaced with Python. Therefore, if you are familiar with Python you won't need Bash programming for automating complex tasks."
---

## Intro

I show how Bash file management can be replaced with Python. Therefore, if you are familiar with Python you won't need Bash programming for automating complex tasks.


## Assumptions

To avoid repetition, the codes in this post assume the libraries below are imported:
```python
import os, shutil, fnmatch, ntpath
```
Moreover, I assume that users of these codes, employ `try` blocks to catch exceptions at a higher level because there are always I/O exceptions when reading and writing files. 

## Commands

In the below codes, comments show bash commands which are followed by their Python equivalent.

The current working directory can be found via:

```python
# pwd
os.getcwd()
```

Move a file/directory into another directory with:
```python
# mv myFile myDir
shutil.move('myFile', 'myDir')
```

Copy a file into another directory

```python
# cp myFile myDir
shutil.copy2('myFile', 'myDir')
```

Copy a directory in another place with the same or different name:


```python
# $ cp -r myDir1 myDir2
shutil.copytree('myDir1', 'myDir2')
```
If `myDir2` is not existed, the command creates it and then the content of `myDir1` is copied into it

Remove a file:

```python
# $ rm a_file
os.remove('a_file')
```

Create a file:

```python
# touch myFile
f = open("myFile.txt", "w")
f.write("Hello dear!")
f.close()
```

Remove a directory and its content:
```python
# $ rm -r myDir
shutil.rmtree('myDir')
```

Create a directory:
```python
# mkdir myDir
os.makedirs('myDir')
```

Get a list of files and directories inside a directory:
```python
# $ ls myDir
os.listdir('myDir')
```

To check if a path is a file:
```python
isIt = os.path.isfile('/dir1/myFile')
```
To check if a path is a directory:

```python
isIt = os.path.isdir('/dir1/dir2')
```
To check if a path (file/directory) exists:

```python
Exists = os.path.exists('/dir1/myFile')
```

Get a file or directory from its path i.e. strip everything from left to the rightest `/` in a the path:

```python
# basename path
ntpath.basename(a_path)
# /dir1/dir2/dir3 -> dir3
# /dir1/dir2/file.txt -> file.txt
```

Recursively get directories and files within a directory:

```python
for root,dirs,files in os.walk(a_path):
        print (root)
        print (dirs)
        print (files)

```

`os.walk()` is perfect for searching files or directories. See its usage in the next section.

## Programming

Here, I define some functions for higher level programmaing.

To delete the content of directory:
```python
def removeDirContent(dir):
    shutil.rmtree(dir)
    os.makedirs(dir)
```

Get a list of all files within a directory:

```python
def listSubfiles(dir=os.getcwd()):
    files=[]
    for file_path in os.listdir(dir):
        if os.path.isfile(file_path) or os.path.islink(file_path):
            files.append(file_path)
    return files
```

Get a list of directories in a directory (not recursively): 
```python
def listSubdirs(dir=os.getcwd()):
    dirs=[]
    for file_path in os.listdir(dir):
        if os.path.isdir(file_path):
            dirs.append(file_path)
    return dirs
```


Get all sub-directories of a directory recursively like `tree -d` in Bash:

```python
def listAllSubdirs(dir=os.getcwd()):
    return [x[0] for x in os.walk(dir)]
```

Find files with matching a pattern:

```python
def findFiles(pattern, path=os.getcwd()):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result
```


Find recursively list of directories that their name contains `name`:

```python
def findDir(name, path=os.getcwd()):
    allsubs=listAllSubdirs(path)
    result=[]
    for dir in allsubs:
        if name in ntpath.basename(dir):
            result.append(dir)
    return result
```

Remove a list of files
```python
def removeFiles(files):
    for file in files:
        os.remove(file)
```
Remove a list of directories

```python
def removeDirs(dirs):
    for dir in dirs:
        shutil.rmtree(dir)
```

Copy a file in multiple directories

```python
def scatterFile(file, dirs):
    for dir in dirs:
        shutil.copy2(file, dir)
```

Copy a folder multiple times

```python
def multiCopyDir(dir, destNames, destParent=os.getcwd()):
    for name in destNames:
        shutil.copytree(dir, os.path.join(destParent, name))
```

For example, to copy `~/a` folder into `~` and change the
name of copies to `b`, `c`, `d`, the inputs are: 

* dir = `~/a`   
* destParent=`~` 
* destNames=`['b', 'c', 'd']` 
---
title: "Build GCC 11 from source on Ubuntu"
date: 2021-04-29T18:05:20+01:00
image: /images/cement.jpg
imageQuality: "q65"
imageAnchor: "Center" # Smart, Center, TopLeft, Top, TopRight, Left, Right, BottomLeft, Bottom, BottomRight.
tags: ["C++"]
categories: "C++" 
summary: "Here I am building and installing the latest GCC,  11.1, on Ubuntu 21.04 from the source. The procedure is explained step by step. "
---

## Intro

Here, I want to build and install GCC 11.1 on my Ubuntu 21.04. This procedure is probably valid for future versions of GCC too.

## Method

Go to GCC releases on [GitHub](https://github.com/gcc-mirror/gcc/releases), download the latest version in the format of `tar.gz`. Here, I install GCC 11.1. I downloaded it in the `home` folder. 

Extract the file

```bash
cd ~
tar -xvf gcc-releases-gcc-11.1.0.tar.gz
```
A folder with the same name as the `tar.gz` file is created.

Install prerequisites
```bash
cd gcc-releases-gcc-11.1.0
contrib/download_prerequisites
```

Make sure you have flex too
```bash
sudo apt install flex
```

Create a build directory:

```bash
cd ~
mkdir build
cd build
```
Configure GCC for compilation:

```bash
../gcc-releases-gcc-11.1.0/configure -v --build=x86_64-linux-gnu --host=x86_64-linux-gnu --target=x86_64-linux-gnu --prefix=/usr/local/gcc-11.1.0 --enable-checking=release --enable-languages=c,c++,fortran --disable-multilib --program-suffix=-11.1
```

If everything goes well, you get a `Makefile` in `~/build/` directory, otherwise, read the errors and fix them and configure again.

Build GCC:

```bash
make -j 16
```

My laptop has 16 processing threads (8 logical cores), because of that, I put 16. For me, it took about 10 min to finish.

During the `make` process, you might get errors, read, google and fix them. Then run the `make` command again.

Install compiled files:

```bash
sudo make install-strip
```
You finally see the below message:

```
Libraries have been installed in:
   /usr/local/gcc-11.1.0/lib/../lib64
```

## Usage

There are several options to use the new GCC, the simplest is to add the lines below to `~/.bashrc`:

```bash
export PATH=/usr/local/gcc-11.1.0/bin:$PATH
export LD_LIBRARY_PATH=/usr/local/gcc-11.1.0/lib64:$LD_LIBRARY_PATH

# To let CMake know
export CC=/usr/local/gcc-11.1.0/bin/gcc-11.1
export CXX=/usr/local/gcc-11.1.0/bin/g++-11.1
export FC=/usr/local/gcc-11.1.0/bin/gfortran-11.1
```
Nowadays, most *Fortran/C/C++* projects are build by CMake. To guide CMake to use the new compiler, I defined `CC`, `CXX` and `FC` environment variables.

Afterwards, open a new terminal and run
```bash
gcc-11.1 --version
```
You should see the one newly installed.

Instead of editing `~/.bashrc`, another option is to create a file like `~/load_gcc11.1.sh` and paste the above `export` lines in it. Then whenever you need to load this GCC in a terminal, you run

```bash
source ~/load_gcc11.1.sh
```
In this way, you can have multiple versions, and load the one that suits your project.

## Compilers

You can check all available GCC commands with:

```bash
ls /usr/local/gcc-11.1.0/bin/
```
I have below ones and some more:
```
c++-11.1
cpp-11.1
g++-11.1
gcc-11.1
gfortran-11.1
```

## Delete garbage

If all good, we don't need the source and build folders anymore, delete them

```bash
rm ~/build -rf
rm ~/gcc-releases-gcc-11.1.0 -rf
```



## More details 

The default installation of GCC on Ubuntu is accessible with commands without the version extension:

```bash
c++
gcc
```

These commands are symlinks. To find out where they point to 

```bash
which gcc
```
For me it gives `/usr/bin/gcc`. We check its link 

```bash
ls -l /usr/bin/gcc
```

It gives `/usr/bin/gcc -> gcc-10`. We can find the address of it:

```bash
which gcc-10
```

It gives `/usr/bin/gcc-10` for me. You can change the symlinks, for example, `gcc`, to point to `gcc-11.1`, but personally I do not change the default settings of Ubuntu.



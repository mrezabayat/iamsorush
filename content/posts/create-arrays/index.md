---
title: "Various ways to create arrays and their differences in C++"
date: 2020-12-08T18:10:20+01:00
image: /images/pingpong.jpg
imageQuality: "q65"
imageAnchor: "Center" # Smart, Center, TopLeft, Top, TopRight, Left, Right, BottomLeft, Bottom, BottomRight.
tags: ["C++"]
categories: "C++" 
summary: "Summary of this page used in cards, and also in SEO description of the page."
draft: true
---

## Introduction

## C array

## Pointer 1D

## Pointer 2D

## technique of first pointer to all, the rest to later ones

## std::array

## std::vector
Creates an array of objects on the heap. The array is dynamic: objects can be added or removed during runtime. The memory of a vector is managed by C++, when it goes out of scope all the elements are automatically destructed. Note that if the elements are raw pointers, only raw pointers are removed but their target is untouched. 

## Boost::multiarray

## Custom array nD

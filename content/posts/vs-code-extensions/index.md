---
title: "Essential VS Code font and extensions for C++"
date: 2021-03-14T14:10:21+01:00
image: /images/tools2.jpg
imageQuality: "q65"
imageAnchor: "Center"
tags: ["C++", "VS Code"]
categories: "C++" 
summary: "I briefly enumerate the primary font and extensions that I install on my Visual Studio (VS) Code to develop a C++ code: Fira Code font, CMake tools, bookmarks, snippets, and so on."
---

## Intro

I briefly enumerate the primary font and extensions that I install on my Visual Studio (VS) Code to develop a C++ code. The first mention is a font, the rest are extensions which can be found by searching their names in the extensions panel of VS Code.


## Fira Code Font

This is a beautiful ligature font that can turn multiple characters into one symbol. *C++* operators are shown much nicer, for example, `>=` will be shown as `≥` and `<=` is seen as  `≤`. The picture below from [Fira Code GitHub](https://github.com/tonsky/FiraCode), shows the transformations

{{< img "*fira*" "pointer allocation" >}}

The instraction for adding Fira Code can be found [here](https://github.com/tonsky/FiraCode/wiki/VS-Code-Instructions). At some point in the instruction, you have to change a line in `settings.json` of VS Code from

```json    
"editor.fontLigatures": null,
```
to

```json
"editor.fontLigatures": true,
```
so, the transformations happen.
I recommend applying the stylistic sets explained in the instruction to make the code look better.


## C/C++ by Microsoft

This extension brings IntelliSense to your code. While typing, it suggests relevant classes, their members, and functions. Moreover, it shows errors in the code without compilation. It supports GCC, Clang and MSVC.


When you search C/C++, besides this extension, you may see *C/C++ Extension Pack*. Have a look at the pack too, it contains all the extensions recommended by Microsoft. 


## CMake Tools by Microsoft

CMake is currently the most popular build system. By installing this extension, configuring, building, and debugging a CMake project become a breeze.

You get handy buttons at the bottom of VS Code, and a panel listing all the targets. By right-clicking on each target you can build/debug that target.

{{< img "*cmake*" "pointer allocation" >}}


## CMake by twxs

This one brings language support to CMake files. While you type, it suggests CMake commands. 

{{< img "*cmakelang*" "pointer allocation" >}}


## Bookmarks by Alessandro Fragnani

This adds bookmarks capabilities to your code. It is very useful in projects with many/big files. A line can be bookmarked with `alt+ctrl+k` and you navigate to the next bookmark with `alt+ctrl+l` or the previous one with `alt+ctrl+j`. Note that these shortcuts can be overwritten by other extensions. By pressing `ctrl+shift+p`, and typing *bookmarks*, all the commands and keyboard shortcuts can be seen.

{{< img "*bookmark*" "pointer allocation" >}}


## Bracket Pair Colorizer 2 by CoenraadS

I don't know how I lived before without this. It gives different colours to different matching brackets.
It hugely improves code readability. The colours also can be customised in `settings.json` of a project.

The extension also draws colourful lines to group codes in between brackets. See the colourful brackets and the yellow line highlighting the function block.

{{< img "*bracketpair*" "pointer allocation" >}}



## C/C++ Snippets by Harsh

This one saves a lot of time for writing blocks of *if condition*, *for loop*, and so on. 
You write a few first characters of the snippet, for example, `for` and the desired snippet
appears top in the autocomplete suggestions, press `Tab` key and the block is pasted in the code.



{{< img "*snippet*" "pointer allocation" >}}





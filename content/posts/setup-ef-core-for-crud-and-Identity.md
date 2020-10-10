
---
title: "Basic setup of Entity Framework (EF) core for CRUD and authentication"
date: 2020-10-10T19:37:36+01:00
draft: true
image: /images/bird.webp
thumbnail: /images/bird_tn.webp
tags: ["C#","Back-end Web"]
---

In this post, step by step I create a web app using Entity Framework core and razor pages. The app is library that admin can CRUD books info on a database and authenticated users can browse the records.

* Open visual studio (mine is 2019 v16.7),  click on *Create a new project*  and follow below pictures

select_project.JPG
choose_razor_pages.JPG
choose_name.JPG

You will have a project like below

project_expolrer.JPG

## Create EF Models

Models can contain any logic, but here models refer to tables in database. Create the folder and files like below

model_folder.JPG

When we defining a model (or table here), we not only consider columns of the table but also it's relationship with other models (or tables). In this example, I only focus on one-to-many relationship. Each book *has a* publisher, and  each publisher *has many* books. 

In `Publisher.cs` I have

```c#
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace EfTest.Models
{
    public class Publisher
    {
        public int Id { get; set; }
        public string Name { get; set; }

        public ICollection<Book> Books { get; set; }
    }
}
```

`Id` must be named Id so EF set it as primary key of `Publisher` table. `Name` is 






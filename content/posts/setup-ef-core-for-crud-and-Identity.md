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

`Id` must be named Id so EF set it as primary key of `Publisher` table. `Name` is an example of a table column, other columns can be added by defining new properties like address and website. The last line will not create a column but is an EF core convention to create one-to-many relationship that each publisher has many books. The properties which are not primitive type like `Book` are called navigation properties. We can mention the relationship in the Book class, see `Book.cs`:

```cpp
using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations.Schema;
using System.IO;
using System.Linq;
using System.Threading.Tasks;

namespace EfTest.Models
{
    public class Book
    {
		public int Id { get; set; }
		public string Title { get; set; }

		public int PublisherId { get; set; }
		public Publisher Publisher { get; set; }

		[NotMapped]
		public string FilePath
		{
			get { return Path.Combine("..","pdf",Title + ".pdf"); }
		}

	}
}
```

In `Book` class, `Id` is the default primary key, `Title` is an arbitrary column in the Book table, more  can be added like author, year, edition. `PublisherId` and `Publisher` are EF core conventions to have the relationship of each book has a publisher. Here `Publisher` is the navigation property. Note that the foreign class id and name must follow the convetion "class name + Id" and "class name".   

If a property needs to be ignored by EF core, like `File Path`, annotate it with `[NotMapped]`. 


To have one-to-many relationship, mentioning the relationship in `Book` class was not necessary. Personally, I prefer to have them in `Book` class, so when a Book record pulled from database, automatically its correspondant publisher is found too. 

`IdentityUser` is the default class that .Net core uses for user authentication. It contains username, email, password and related information. To add custom properties to the class we have to derive another class, `AppUser` here. `AppUser.cs` file contains

```cpp
using Microsoft.AspNetCore.Identity;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace EfTest.Models
{
    public class AppUser : IdentityUser
    {
        public string Name { get; set; }
    }
}
```

I added only property `Name` but any arbitrary column table can be added like StartMembership, EndMembership, or a one-to-many relationship with `Book` class to denote the books user barrowed. 

We have to modify `ConfigureServices` in `Startup.cs` so it uses the new `AppUser` class instead of default `IdentityUser`:

```cpp
public void ConfigureServices(IServiceCollection services)
        {
            // some codes here ...
            services.AddDefaultIdentity<Models.AppUser>(options => options.SignIn.RequireConfirmedAccount = true)
                .AddRoles<IdentityRole>()
                .AddEntityFrameworkStores<ApplicationDbContext>();
            // rest of the code ...
        }
```

Make sure `.AddRoles<IdentityRole>()` is there as well which is necessary to have roles like admin, user, and so on.
There are other instances of `IdentityUser` in other files, simply find all them by `Ctrl+f` replace them with `Models.AppUser`. Otherwise you get some errors.

I found two of them in `_LoginPartials.cshtml`:

```c#
@inject SignInManager<Models.AppUser> SignInManager
@inject UserManager<Models.AppUser> UserManager
```

`ApplicationDbContext.cs` is changed to have the name of tables

```c#
    public class ApplicationDbContext : IdentityDbContext
    {
        public ApplicationDbContext(DbContextOptions<ApplicationDbContext> options)
            : base(options)
        {
        }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            base.OnModelCreating(modelBuilder);

            SeedData(modelBuilder);
            AddAdmin(modelBuilder);
        }

        public DbSet<Book> Books { get; set; }
        public DbSet<Publisher> Publishers { get; set; }
	
	// rest of the code ...
    }
}
```

`SeedData` is created to initialize database with some test records:

```c#
        private void SeedData(ModelBuilder modelBuilder)
        {
            modelBuilder.Entity<Publisher>().HasData(
                new Publisher() { Name = "Little, Brown and Company", Id = -1 },
                new Publisher() { Name = "Scholastic", Id = -2 }
                );
            modelBuilder.Entity<Book>().HasData(
                new Book() { Id = -1, Title = "Harry Potter And The Cursed Child", PublisherId = -1 },
                new Book() { Id = -2, Title = "The Hunger Games", PublisherId = -2 }
                );


            modelBuilder.Entity<AppUser>().HasData(

                new AppUser()
                {
                    Id = Guid.NewGuid().ToString(),
                    UserName = "a@test.com",
                    NormalizedUserName = "a@bp.com".ToUpper(),
                    Email = "a@bp.com",
                    NormalizedEmail = "a@bp.com".ToUpper(),
                    EmailConfirmed = true,
                    SecurityStamp = string.Empty,
                    PasswordHash = HashPassword(null, "pass")
                });
        }
        
```
and I added the admin here as well

```c#
private void AddAdmin(ModelBuilder modelBuilder)
        {
            string adminId = Guid.NewGuid().ToString();
            string roleId = Guid.NewGuid().ToString();


            modelBuilder.Entity<IdentityRole>().HasData(new IdentityRole { Id = roleId, Name = "Admin", NormalizedName = "Admin".ToUpper() });

            modelBuilder.Entity<AppUser>().HasData(
                new AppUser()
                {
                    Id = adminId,
                    Name = "admin",
                    UserName = "admin@x.com",
                    NormalizedUserName = "admin@x.com".ToUpper(),
                    Email = "admin@x.com",
                    NormalizedEmail = "admin@x.com".ToUpper(),
                    EmailConfirmed = true,
                    SecurityStamp = string.Empty,
                    PasswordHash = HashPassword(null, "pass")

                });

            modelBuilder.Entity<IdentityUserRole<string>>().HasData(new IdentityUserRole<string>
            {
                RoleId = roleId,
                UserId = adminId
            });
        }
```

`IdentityUser` saves the hash of a password, so I created the below function for that purpose:

```c#
string HashPassword(AppUser user, string password)
        {
            var hasher = new PasswordHasher<AppUser>();
            return hasher.HashPassword(user, password);
        }
```

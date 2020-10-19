---
title: "Lockout user after multiple failed authentication via .Net core Identity"
date: 2020-10-19T19:10:20+01:00
image: /images/bird.webp
thumbnail: /images/bird_tn.webp
tags: ["Back-End Web", "C Sharp",".Net Core"]
---

## Goal

I want to configure .Net core Identity in a way that when a user inserts wrong passwords several times the account gets locked for 5 minutes.

## Result

{{<rawhtml>}}
<video width=100% controls>
  <source src="/videos/lockedout_user.webm" type="video/webm">
Your browser does not support the video tag.
</video>
{{< /rawhtml >}}

## Step 1: Configure *Startup.cs*

Edit *Startup.cs* file as below

```c#
public void ConfigureServices(IServiceCollection services)
{
    // other codes

    services.Configure<IdentityOptions>(options =>
    {
        // Lockout settings.
        options.Lockout.DefaultLockoutTimeSpan = TimeSpan.FromMinutes(5);
        options.Lockout.MaxFailedAccessAttempts = 5;
        options.Lockout.AllowedForNewUsers = true;
    });
    
}
```

## Step 2: Change calls to SignInManager

By default Identity pages are not accessible to be edited. See [my post](https://iamsorush.com/posts/add-identity-pages-net-core/) to add Identity Login page.
Then find file */Areas/Identity/Account/Login* page. In the code behind, *Login.cshtml.cs*, find and edit below line

```c#
var result = await _signInManager
            .PasswordSignInAsync(
                Input.Email, 
                Input.Password, 
                Input.RememberMe, 
                
                // Make Sure This is true
                lockoutOnFailure: true);
```

Please note, this works well for users who register through the app, but might not work for user accounts which are created through seeding the database.
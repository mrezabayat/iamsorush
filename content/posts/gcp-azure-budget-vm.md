---
title: "Host a .Net core web application for less than $5 a month"
date: 2020-10-02T18:50:47+01:00
image: /images/azure.webp
thumbnail: /images/azure_tn.webp
---

It is very tempting to deploy your website with web hosting services like Bluehost and Hostgator
 due to their long time existence in this market. Recently, I tried Ionos to host
my .Net core  app. The price was very cheap £1 ($1.29) for 12 months and then £5 ($6.47)/month.
I fell for the good price, but when I passed the fancy well marketed home page,
 the control panel for deploying the app had no
user guide, everything was slow, the system was 32-bit, and you'd get more help from a baker than their customer service. After days of trial
and error I figured that out; I might write a post in detail about how I published the app eventually.


But here I want to talk about Google Cloud Platform (GCP) and Microsoft Azure.
You can register with them free of charge and try their services with 300$ credit
for GCP for 90 days and £150 credit for Azure for 30 days. Azure also provides 12 months free access
to its popular products.

You have an option to deploy your app directly
from Visual Studio to these clouds with Web App services and all being taken
care of. You don't need to
think about operating systems, compilers, firewalls. The web app is scaled based
on the amount of traffic it gets.


Moreover, you have the option of virtual machines which are my favourites now. You choose a
virtual machine instance with any number of cores and memory. You can even choose
the storage to either be HDD or SSD. The good bit  is if you have complex code like interoperability
between .Net and C++, it can be easily setup as your local machine. However there is a gotcha when the app is
cpu intensive. I explain it in the following. Let's check out some budget systems.

GCP cheapest machine is f1-micro from Series N1 with 1vCPU and 614MB memory. With a few clicks
the instance got ready with Ubuntu 20.04. It came up immediately taking only ~220 MB of ram.
It is suitable for a website with a light application and low
traffic. I deployed a template of Blazor server app and it ran smoothly with memory being ~ 260MB.
This instance is introduced as a free machine but not completely.
You will be charged if there is cpu burst (hitting 100%) or the egress (download/outbound) traffic from
the website is more than
1 GB per month [see GCP for more details](https://cloud.google.com/compute/docs/machine-types). Google estimates $4.28/month for this instance [see GCP options here](https://cloud.google.com/compute/vm-instance-pricing).

Azure budget machine is [see in Azure website](https://azure.microsoft.com/en-gb/pricing/details/virtual-machines/windows/):
Instance B1S: 1 vCPU, 1GB RAM 4GB storage  
OS: Ubuntu  
Region North Central US  
$4.42/month when 1 year reserved ($7.59/month pay as you go)  

The prices are estimates. Azure charges egress as well. There are free, F1, and shared (£0.01/hour), D1, app services with Azure however they are limited to 60 CPU minutes/day and 240 CPU minutes/day, so not
suitable for production, [see them in Azure website](https://azure.microsoft.com/en-gb/pricing/details/app-service/windows/).

I should mention Heroku too. They have a completely free app service which you can deploy onto. it has 550 dyno/hour which is less than a month but if you verify your credit car it is increased to 1000 dyno/hour which is higher than a month of usage. But the problem is the app sleeps after 30 minutes of inactivity (no visitors). You can pay $7 and it never sleeps.
Check my Blazor hosted app on [Heroku](https://iamsorush.herokuapp.com/), it takes several seconds to wake up.

# What is this repo?

This is the code behind my blog [IamSorush.com](https://iamsorush.com)  in which I write about numerical coding and app development. The blog is a static website complied using Hugo on Netlify. 
GitHub host the code, Netlify provides CDN and Continuous deployment. So after pushing each commit to this repo
Netlify compiles it automatically and re-publish the website on its CDN.

The website is designed by myself to keep it as light and fast as possible. Each page is around 100 KB while 
on the internet average pages are around 4MB (reference google). To reach this aim:

* I write most of CSS and Javascript by myself rather than using relatively heavy libraries like JQuery and Bootstrap.  
* The layout of the website is done using Pure Grid library. 
* There are some libraries that I cannot write or don't have time to write like showing math equations properly. In most pages, I try to avoid them as much as aesthetically not jeopardising the website.  If a page needs a library, it is only added to that page, not others.  
* Non-vector images are in WebP format as they are very light compared to JPEG. Some browsers do not support them yet, but sooner or later all will pick this format.   
* Vector images are in SVG format.  
* Where needed, Netlify facilities are prefered than Javascript, libraries or third-party websites like Subscription forms because Netlify does not compromise website loading speed.  
* I frequently monitor the speed of the website, currently at this commit, all pages get the score of 100/100 on mobile and desktop from Google PageSpeed Insights.  

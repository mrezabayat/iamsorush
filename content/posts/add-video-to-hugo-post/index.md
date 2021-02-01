---
title: "How to add a video to a Hugo post"
date: 2020-10-16T18:30:30+01:00
image: /images/camera.jpg
tags: ["Front-End Web", "Hugo"]
categories: "Html"
summary: "I want to add a video to a Hugo blog post. The video is hosted on my website, so it is not a Youtube or Vimeo."
---

## Goal

I want to add a video to a Hugo blog post. The video is hosted on my website, so it is not a Youtube or Vimeo. 


## Result

{{< rawhtml >}}
<video width=100% controls>
  <source src="/videos/table_of_contents.webm" type="video/webm">
Your browser does not support the video tag.
</video>
{{< /rawhtml >}}


## Setup a raw HTML shortcode

The posts in Hugo are written using *Markdown* syntax. To have raw HTML code included, create `shortcodes` folder in your Hugo website directory as

```bash
/your-website/layouts/shortcodes
```

create a file, `rawhtml.html` with the content

```html
<!-- raw html -->
{{.Inner}}
```

Now, in any post we can insert the desired HTML code using the below code:

```go
{{</* rawhtml >}}    
    <!-- html codes here-->  
{{< /rawhtml */>}}
```

## Add Video

The video files are placed in the path `/your-website/static/videos`. 

To embed a video, the `video` tag is used: 


```go
{{</* rawhtml >}} 

<video width=100% controls autoplay>
    <source src="/videos/table_of_contents.webm" type="video/webm">
    Your browser does not support the video tag.  
</video>

{{< /rawhtml */>}}
```

`controls` gives video *play*, *pause*, *full-screen* controls and `autoplay` plays the video automatically when the page is loaded. 
The video type can be	`video/mp4`, `video/webm`, or `video/ogg` depending on the format of the file.


## References

I got ideas and codes from the below website(s)

[Raw html](https://anaulin.org/blog/hugo-raw-html-shortcode/)



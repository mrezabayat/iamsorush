---
title: "How to have math equations in your website"
date: 2020-07-17T23:33:46+01:00
draft: true
image: /images/matrix.webp
thumbnail: /images/matrix_tn.webp
---
If you want to write math equations in your website or blog, plain text becomes immediately illegible when
writing something more complex than addition and subtraction. Here, I list what solutions I found and what
I am implementing in this website.

## jqMath

[jqMath](https://mathscribe.com/author/jqmath.html) is a simple and fast JavaScript library which uses
JQuery. The syntax is similar to LaTeX. It is supported
by almost all up-to-date browsers. In terms of weight, it is the lightest I found. It works with only
three files

* jqmath-X.css (7 KB)
* jqmath-etc-X.min.js (37 KB)
* jquery-X.min.js (78 KB)

with total unzip size of 122 KB. This is the one I am using in my website. But I have to confess
this is the least beautiful one.

To install jqMath go to its [website](https://mathscribe.com/author/jqmath.html) and find the download link.
In the downloaded zip file, there are all necessary files and webpage sample, use that one or just copy the below lines in the <head> section of your page. Note, the version
of files I used maybe different to yours.

<meta charset="utf-8">
<link rel="stylesheet" href="/css/jqmath-0.4.3.css">
<script src="/js/jquery-1.4.3.min.js"></script>
<script src="/js/jqmath-etc-0.4.6.min.js" charset="utf-8"></script>

Then copy the downloaded files (only ones mentioned above) into their directories in the root of the website.
For Wordpress, you need a plugin to write in the header of pages.

My website is a Hugo website, in the bottom of `baseof.html` I added

```go
{{ if .Params.jqmath}}
    {{ partial "jqmath.html" . }}
{{ end }}
```

where `jqmath.html` is placed in `/layouts/partials` which contains exactly the header lines above.
In the `config.toml` file I defined jamath paramter which is `false` by default

```toml
[params]
  jqmath=false
```

So whenever I write a post containing equations in Hugo, at the top section I add `jqmath: true`

```
title: "Title of a math post"
date: 2020-07-17T23:33:46+01:00
draft: false
jqmath: true
```
and I am good to go to write equations in LaTeX format like `$a*X^2=b$`.

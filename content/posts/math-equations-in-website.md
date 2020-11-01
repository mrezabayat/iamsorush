---
title: "How to have math equations in your website"
date: 2020-07-17T23:33:46+01:00
draft: false
image: /images/equation.webp
thumbnail: /images/equation_tn.webp
tags: ['Front-End Web']
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
In the downloaded zip file, there are all necessary files and a webpage sample, use that one or just copy the below lines in the `<head>` section of your page. Note, the version
of files I used may be different to yours.

```html
<meta charset="utf-8">
<link rel="stylesheet" href="/css/jqmath-0.4.3.css">
<script src="/js/jquery-1.4.3.min.js"></script>
<script src="/js/jqmath-etc-0.4.6.min.js" charset="utf-8"></script>
```

Then copy the downloaded files (only ones mentioned above) into their directories in the root of the website.
For a WordPress blog, you need a plugin to write in the header or footer of pages.

My website is compiled using Hugo, in the bottom of `baseof.html` I added

```go
{{ if .Params.jqmath}}
    {{ partial "jqmath.html" . }}
{{ end }}
```

where `jqmath.html` is placed in `/layouts/partials` which contains exactly the snippet above.
In the `config.toml` file I defined jqMath parameter which is `false` by default

```toml
[params]
  jqmath=false
```

So whenever I write a post containing equations in Hugo, at the top section I add `jqmath: true` like below

```markdown
title: "Title of a math post"
date: 2020-07-17T23:33:46+01:00
draft: false
jqmath: true
```
and I can write equations in LaTeX format like `$a*X^2=b$`.

## KaTeX

[KaTeX](https://katex.org/) has a higher print quality than jqMath and supports major browsers. It is independent of other libraries. KaTeX is faster than MathJax (next section) and the library is
relatively light (~350 KB). Their [website](https://katex.org/docs/browser.html) explains installation on Node.js and browsers in details. Basically, the below lines need to be added to the `<head>` section of an HTML page:

```HTML
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.12.0/dist/katex.min.css" integrity="sha384-AfEj0r4/OFrOo5t7NnNe46zW/tFgW6x/bCJG8FqQCEo3+Aro6EYUG4+cU+KJWu/X" crossorigin="anonymous">

<!-- The loading of KaTeX is deferred to speed up page rendering -->
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.12.0/dist/katex.min.js" integrity="sha384-g7c+Jr9ZivxKLnZTDUhnkOnsh30B4H0rpLUpJ4jAIKs4fnJI+sEnkvrMWph2EDg4" crossorigin="anonymous"></script>

<!-- To automatically render math in text elements, include the auto-render extension: -->
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.12.0/dist/contrib/auto-render.min.js" integrity="sha384-mll67QQFJfxn0IYznZYonOWZ644AWYC+Pt2cHqMaRhXVrursRwvLnLaebdGIlYNa" crossorigin="anonymous"
    onload="renderMathInElement(document.body);"></script>
```

I have KaTeX setup on my website, so when jqMath doesn't render well I use it. To have it on my Hugo website,
I added file `/layouts/partials/katex.html` containing above codes.
In the `config.toml` file I defined `katex` parameter which is `false` by default

```toml
[params]
  katex=false
  jqmath=false
```

and in the bottom of `baseof.html` I added

```go
{{ if .Params.katex }}
    {{ partial "katex.html" . }}
{{ end }}
```

So I add `katex:true` in top of a markdown post to activate KaTex.

## MathJax

[MathJax](https://www.mathjax.org/) is the most famous and popular library to add math
 equations to a webpage but apparently slower than KaTeX see this [live comparison](https://www.intmath.com/cg5/katex-mathjax-comparison.php). If it doesn't have a higher print quality than KaTex, it does not have lower.

 To install MathJax, you need to add the below snippet, for more details see their [website](https://www.mathjax.org/#gettingstarted)

 ```HTML
<script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>

 ```

 The library size is about 800 KB, therefore, heaviest in this list. That's why I don't use it in my
 website.


## MathML

[MathML](https://www.w3.org/Math/) is not a library but a capability that some browsers have, currently
only Firefox and Safari [more here](https://www.w3.org/wiki/Math_Tools#Browsers). MathML is written
in XML style like

```xml
<math>
  <munderover>
    <mo>&int;</mo>
    <mi>a</mi>
    <mi>b</mi>
  </munderover>
    <mi>x</mi>
  <mi>dx</mi>
</math>
```

I know this is not
a great option due to lack of supports, however, if it was a commonplace feature by all browsers,
it could have been my top choice.

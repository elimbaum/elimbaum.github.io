---
permalink: /readme
---

{% include math.html %}

# [readme]
{:.no_toc}

You're either reading this on [github][1], or [hosted on the web via github pages][2]. This is a meta-page, for notes about the creation and operation of this website.

1. TOC
{:toc}

## TODO
- make better layout with navbar
- styling
- pictures and finish about
- make image include or module or something?
- favicon?
- new theme? I don't think I can modify `<head>` otherwise.
- auto run link checker and linter

## Local usage
`> bundle exec jekyll serve`

Give it a few seconds after saving to regenerate.

To access from other devices on LAN, add `-H 0.0.0.0`. Note that this will break the title link, since it will try to link to `0.0.0.0`.

## Jekyll/Kramdown notes

### Table of contents

Add the following markdown where the TOC should be:
```
1. TOC
{:toc}
```
Add `{:.no_toc}` below headings (such as the title) which should not be included in the TOC.

### Random

- 404 page should be in base directory with front matter `permalink: /404`.
- Posts must use the format `YYYY-MM-DD-XXXX`.
- Custom styling can be added with `style.scss`, as long as that file also imports the theme's style.
- Added CSS rule so that centered captions will be created from any *italicized text* directly following an image.
- To force a width for an image, use HTML `img` tag instead of Markdown. (actually, looks like kramdown _does_ support extra attributes with `{: ...}` syntax.)
    + `![alt](/img.jpeg){: width="25%"}`

## Personal domain

HTTPS certificate is from Let's Encrypt via Github pages.

I am hosting this on `elibaum.com`, with a DNS ALIAS for `www`. However, there is a [known issues][3] with Github Pages that causes navigation to `www` to show a security error: basically, Github is _only_ generating a certificate for `elibaum.com`, not `www.elibaum.com`; the latter returns a certificate for `www.github.com`, instead. (The redirect works fine for http, and returns `301 Moved Permanently`, so browsers should cache the redirect...)

<s>Ah, shoot. Just realized trying to run the website from `elibaum.com` means that my email forwarding won't work (since namecheap is providing the email forward).</s>

Nevermind! It still does. Uses an `MX` record instead of `A`, and there are apparently some smarts in there so that it doesn't forward when the messages _comes from_ the forwarding address.


## math

it works (mathjax)! Just need to 

{% raw %}
```
{% include math.html %}
```
{% endraw %}

at the top of the page, and then

$$
e^{i\theta} = \cos(\theta) + i\sin(\theta)
$$

`$$` for math blocks. Inline math with `\\( \\)` like this: \\(a = b\\)

tada!

---

[1]: https://github.com/elimbaum/elimbaum.github.io
[2]: https://elibaum.com/readme
[3]: https://github.com/isaacs/github/issues/1675
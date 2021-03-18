---
permalink: /readme
---

# readme
{:.no_toc}

You're either reading this on [github][1], or [hosted on the web via github pages][2]. two birds, etc. :) This is a meta-page; a page for notes about the creation and operation of this website.

1. TOC
{:toc}

## TODO
- make better layout with navbar
- styling
- pictures and finish about
- finish life post
- add dates (month year? "%b %Y" front page and on post.)
- make meta page/readme!
- favicon

## Local usage
`> bundle exec jekyll serve`

Give it a few seconds after saving to regenerate.

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

## Personal domain

HTTPS certificate is from Let's Encrypt via Namecheap.


[1]: https://github.com/elimbaum/elimbaum.github.io
[2]: {{ site.url }}/readme

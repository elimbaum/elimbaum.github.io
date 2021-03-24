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
- does `_site` need to be in git? guess it can't hurt
- broken link crawler

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
- Posts must use the format `YYYY-MM-DD-XXXX`.

## Personal domain

HTTPS certificate is from Let's Encrypt via Github pages.

I am hosting this on `elibaum.com`, with a DNS ALIAS for `www`. However, there is a [known issues][3] with Github Pages that causes navigation to `www` to show a security error: basically, Github is _only_ generating a certificate for `elibaum.com`, not `www.elibaum.com`; the latter returns a certificate for `www.github.com`, instead. (The redirect works fine for http, and returns `301 Moved Permanently`, so browswers should cache the redirect...)

<s>Ah, shoot. Just realized trying to run the website from `elibaum.com` means that my email forwarding won't work (since namecheap is providing the email forward).</s>

Nevermind! It still does. Uses an `MX` record instead of `A`, and there are apparently some smarts in there so that it doesn't forward when the messages _comes from_ the forwarding address.


[1]: https://github.com/elimbaum/elimbaum.github.io
[2]: https://elibaum.com/readme
[3]: https://github.com/isaacs/github/issues/1675
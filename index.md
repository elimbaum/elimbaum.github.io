{% include navbar.md %}

This is Eli Baum’s personal website.

I am a PhD student at Boston University, advised by [John Liagouris](https://cs-people.bu.edu/liagos/index.html) and [Mayank Varia](https://www.mvaria.com/).  We are working on building usable and secure tools for multi-party computation.

### posts
{% for post in site.posts %}
- [{{ post.title }}]({{ post.url }}) ({{ post.date | date_to_string }}, {{ post.content | strip_html | number_of_words }} words){% endfor %}

*updated {{ site.time | date: "%d %b %Y %H:%M %Z" }}*

---
---

{% include navbar.md %}

This is Eli Baum’s personal website.

I am a PhD student at Boston University advised by [Kinan Dak Albab](https://www.babman.io/). I work on building usable and secure tools for multi-party computation, and dabble in a few other flavors of cryptography.

### posts

<table class="post-list">
{% for post in site.posts %}
<tr>
<td>{{ post.date | date_to_string }}</td>
<td><a href="{{ post.url }}">{{ post.title }}</a> ({{ post.content | strip_html | number_of_words }} words)</td>
</tr>
{% endfor %}
</table>

*updated {{ site.time | date: "%d %b %Y %H:%M %Z" }}*


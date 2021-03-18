{% include_relative navbar.md %}

This is Eli Baum’s personal website.

### posts
{% for post in site.posts %}
- [{{ post.title }}]({{ post.url }})
{% endfor %}

### TODO
- make better layout with navbar
- styling
- pictures and finish about
- finish life post
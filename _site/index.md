{% include navbar.md %}

This is Eli Baum’s personal website.

### posts
{% for post in site.posts %}
- [{{ post.title }}]({{ post.url }}) ({{ post.date | date_to_string }}){% endfor %}
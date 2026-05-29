---
layout: default
---

# Today's Schmeichel(s):


## Groups
{% for group in site.data.groups %}
- [{{ group.name }}]({{ '/pages/' | append: group.slug | append: '.html' | absolute_url }})
{% endfor %}

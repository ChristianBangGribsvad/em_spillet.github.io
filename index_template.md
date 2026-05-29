---
layout: default
---

# Today's Schmeichel(s):


# Next Matches

NEXT_MATCHES

# Groups
{% for group in site.data.groups %}
- [{{ group.name }}]({{ '/pages/' | append: group.slug | append: '.html' | absolute_url }})
{% endfor %}

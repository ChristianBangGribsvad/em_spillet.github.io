---
layout: default
---

# Today's Schmeichel(s):


# Next Matches

NEXT_MATCHES

# Yesterday's Results

YESTERDAY_RESULTS

# Groups
{% for group in site.data.groups %}
- [{{ group.name }}]({{ '/pages/' | append: group.slug | append: '.html' | absolute_url }})
{% endfor %}

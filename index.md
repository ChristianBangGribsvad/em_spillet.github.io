---
layout: default
---

# Today's Schmeichel(s):
- Alice Sm with 397.0 points part of Team Alpha [see their predictions](./pages/Alice_Sm.html)
- Bob Jo with 397.0 points part of Team Beta [see their predictions](./pages/Bob_Jo.html)


## Groups
{% for group in site.data.groups %}
- [{{ group.name }}]({{ '/pages/' | append: group.slug | append: '.html' | absolute_url }})
{% endfor %}

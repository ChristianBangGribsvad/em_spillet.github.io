---
layout: default
---

# Today's Schmeichel(s):


# Next Matches

NEXT_MATCHES

# Yesterday's Results

YESTERDAY_RESULTS

# Group vs Group

Average cumulative score per group over time — the higher the line, the better that group's participants are performing overall.

![Group vs Group](./pages/group_plots/group_avg.svg?raw=true)

# Groups
{% for group in site.data.groups %}
- [{{ group.name }}]({{ '/pages/' | append: group.slug | append: '.html' | absolute_url }})
{% endfor %}

---
layout: default
---

# Today's Schmeichel(s):


# Leaderboard

LEADERBOARD

# Next Matches

NEXT_MATCHES

# Yesterday's Results

YESTERDAY_RESULTS

# Team vs Team

Average cumulative score per team over time — the higher the line, the better that team's participants are performing overall.

![Team vs Team](./pages/group_plots/group_avg.svg?raw=true)

# Teams
<ul>
{% for group in site.data.groups %}
<li><a href="{{ '/pages/' | append: group.slug | append: '.html' | absolute_url }}" style="background: {{ group.color }};">{{ group.name }}</a></li>
{% endfor %}
</ul>

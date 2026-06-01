---
layout: default
title: WC Prediction Game 2026
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

TEAM_CHART

# Teams

Click on your team to see the standings and individual predictions.

{% if site.data.groups %}
<ul>
{% for group in site.data.groups %}
<li><a href="{{ '/pages/' | append: group.slug | append: '.html' | absolute_url }}" style="background: {{ group.color }};">{{ group.name }}</a></li>
{% endfor %}
</ul>
{% else %}
<p class="chart-placeholder"><em>No teams registered yet — check back once participants have signed up.</em></p>
{% endif %}

---
layout: default
title: WC Prediction Game 2026
---

# Today's Schmeichel(s):
<p class="chart-placeholder"><em>World Cup has not started — Today's Schmeichel will be revealed on each matchday throughout the tournament.</em></p>


# Leaderboard

<div class="leaderboard"><p class="lb-empty"><em>No scores yet.</em></p></div>

# Next Matches

<div class="next-matches">
<p>Mexico vs South Africa &mdash; Thu 11 June, 21:00</p>
<p>South Korea vs Czechia &mdash; Fri 12 June, 04:00</p>
</div>

# Yesterday's Results

<div class="yesterdays-results">
<p><em>No results yet.</em></p>
</div>

# Team vs Team

Average cumulative score per team over time — the higher the line, the better that team's participants are performing overall.

<p class="chart-placeholder"><em>Chart will appear once matches are scored.</em></p>

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

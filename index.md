---
layout: default
title: WC Prediction Game 2026
---

# Today's Schmeichel(s):
- Alice Smith with 397 points part of Team Alpha [see their predictions](./pages/Alice_Sm.html)


# Leaderboard

<div class="leaderboard">
<div class="lb-row lb-gold"><span class="lb-pos">🥇</span><span class="lb-info"><a href="./pages/Alice_Sm.html">Alice Smith</a> <small>(Team Alpha)</small></span><span class="lb-pts">937 pts</span></div>
<div class="lb-row lb-silver"><span class="lb-pos">🥈</span><span class="lb-info"><a href="./pages/Bob_Jo.html">Bob Johnson</a> <small>(Team Beta)</small></span><span class="lb-pts">769 pts</span></div>
<div class="lb-row lb-bronze"><span class="lb-pos">🥉</span><span class="lb-info"><a href="./pages/Carol_Da.html">Carol Davis</a> <small>(Team Alpha &amp; Team Beta)</small></span><span class="lb-pts">701 pts</span></div>
</div>

# Next Matches

<div class="next-matches">
<p><em>No matches scheduled in the next 24 hours.</em></p>
</div>

# Yesterday's Results

<div class="yesterdays-results">
<p><em>No results yet.</em></p>
</div>

# Team vs Team

Average cumulative score per team over time — the higher the line, the better that team's participants are performing overall.

![Team vs Team](./pages/group_plots/group_avg.svg?raw=true)

# Teams

Click on your team to see the standings and individual predictions.

<ul>
{% for group in site.data.groups %}
<li><a href="{{ '/pages/' | append: group.slug | append: '.html' | absolute_url }}" style="background: {{ group.color }};">{{ group.name }}</a></li>
{% endfor %}
</ul>

---
layout: default
---

# Today's Schmeichel(s):
- Alice Smith with 397 points part of Team Alpha [see their predictions](./pages/Alice_Sm.html)
- Bob Johnson with 397 points part of Team Beta [see their predictions](./pages/Bob_Jo.html)


# Leaderboard

<div class="leaderboard">
<div class="lb-row lb-gold"><span class="lb-pos">🥇</span><span class="lb-info">Alice Smith <small>(Team Alpha)</small></span><span class="lb-pts">937 pts</span></div>
<div class="lb-row lb-silver"><span class="lb-pos">🥈</span><span class="lb-info">Bob Johnson <small>(Team Beta)</small></span><span class="lb-pts">769 pts</span></div>
<div class="lb-row lb-bronze"><span class="lb-pos">🥉</span><span class="lb-info">Carol Davis <small>(Team Alpha &amp; Team Beta)</small></span><span class="lb-pts">701 pts</span></div>
</div>

# Next Matches

<div class="next-matches">
<p>Mexico vs South Africa &mdash; Thu 11 June, 21:00</p>
<p>South Korea vs Czechia &mdash; Fri 12 June, 04:00</p>
<p>Canada vs Bosnia-Herzegovina &mdash; Fri 12 June, 21:00</p>
<p>USA vs Paraguay &mdash; Sat 13 June, 03:00</p>
<p>Qatar vs Switzerland &mdash; Sat 13 June, 21:00</p>
</div>

# Yesterday's Results

<div class="yesterdays-results">
<p><em>No results yet.</em></p>
</div>

# Team vs Team

Average cumulative score per team over time — the higher the line, the better that team's participants are performing overall.

![Team vs Team](./pages/group_plots/group_avg.svg?raw=true)

# Teams
{% for group in site.data.groups %}
- [{{ group.name }}]({{ '/pages/' | append: group.slug | append: '.html' | absolute_url }})
{% endfor %}

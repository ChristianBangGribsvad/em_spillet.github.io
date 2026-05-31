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

<div class="chart-wrapper">
<canvas id="chart-team-vs-team"></canvas>
</div>
<script>
(function(){
new Chart(document.getElementById("chart-team-vs-team"),{
  type:"line",data:{"labels": ["2026-06-12", "2026-06-16", "2026-06-20"], "datasets": [{"label": "Team Alpha", "data": [245.5, 471.5, 819.0], "borderColor": "#7c0e0e", "backgroundColor": "rgba(124,14,14,0.08)", "tension": 0.3, "pointRadius": 5, "pointHoverRadius": 8, "borderWidth": 2.5, "fill": true}, {"label": "Team Beta", "data": [205.5, 436.0, 735.0], "borderColor": "#0e7c7c", "backgroundColor": "rgba(14,124,124,0.08)", "tension": 0.3, "pointRadius": 5, "pointHoverRadius": 8, "borderWidth": 2.5, "fill": true}]},
  options:{
    responsive:true,maintainAspectRatio:false,
    interaction:{mode:"index",intersect:false},
    plugins:{
      legend:{position:"right",labels:{boxWidth:12,padding:12,usePointStyle:true}},
      tooltip:{callbacks:{label:function(c){return c.dataset.label+": "+Math.round(c.raw)+" pts";}}}
    },
    scales:{
      x:{grid:{color:"rgba(0,0,0,0.05)"},ticks:{maxTicksLimit:10}},
      y:{beginAtZero:true,
         title:{display:true,text:"Points"},
         grid:{color:"rgba(0,0,0,0.05)"}}
    }
  }
});
})()
</script>

# Teams

Click on your team to see the standings and individual predictions.

<ul>
{% for group in site.data.groups %}
<li><a href="{{ '/pages/' | append: group.slug | append: '.html' | absolute_url }}" style="background: {{ group.color }};">{{ group.name }}</a></li>
{% endfor %}
</ul>

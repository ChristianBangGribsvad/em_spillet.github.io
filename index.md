---
layout: default
title: WC Prediction Game 2026
---

<div class="countdown-block" id="countdown-block">
  <div class="countdown-label">&#x26BD; World Cup kicks off in</div>
  <div class="countdown-units">
    <div class="countdown-unit"><span id="cd-days">-</span><small>days</small></div>
    <div class="countdown-unit"><span id="cd-hours">-</span><small>hours</small></div>
    <div class="countdown-unit"><span id="cd-minutes">-</span><small>min</small></div>
    <div class="countdown-unit"><span id="cd-seconds">-</span><small>sec</small></div>
  </div>
</div>
<div class="countdown-live" id="countdown-live" style="display:none">&#x1F534; Tournament is live</div>
<script>
(function(){
  var KICKOFF=new Date('2026-06-11T19:00:00Z');
  var block=document.getElementById('countdown-block');
  var live=document.getElementById('countdown-live');
  function pad(n){return String(n).padStart(2,'0');}
  function tick(){
    var diff=KICKOFF-new Date();
    if(diff<=0){block.style.display='none';live.style.display='block';return;}
    var d=Math.floor(diff/86400000);
    var h=Math.floor(diff%86400000/3600000);
    var m=Math.floor(diff%3600000/60000);
    var s=Math.floor(diff%60000/1000);
    document.getElementById('cd-days').textContent=d;
    document.getElementById('cd-hours').textContent=pad(h);
    document.getElementById('cd-minutes').textContent=pad(m);
    document.getElementById('cd-seconds').textContent=pad(s);
  }
  tick();setInterval(tick,1000);
})();
</script>

<div class="form-cta">
  &#x1F4CB; Fill out your predictions: <a href="https://docs.google.com/forms/d/e/1FAIpQLSefBXw4cBjKwpa_s_IXLKEHxSgm6pslikPZxRU0JgWBELpr1Q/viewform?usp=dialog" target="_blank" rel="noopener">Open prediction form &#x2192;</a>
</div>

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

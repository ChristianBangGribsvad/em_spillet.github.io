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
  var KICKOFF=new Date('2026-06-11T19:00:00Z'); /* 21:00 Copenhagen / CEST */
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
- Bob Johnson with 95 points part of Team Beta [see their predictions](./pages/Bob_Jo.html)


# Leaderboard

<div class="leaderboard">
<div class="lb-row lb-gold"><span class="lb-pos">🥇</span><span class="lb-info"><a href="./pages/Alice_Sm.html">Alice Smith</a> <small>(Team Alpha)</small></span><span class="lb-pts">169 pts</span></div>
<div class="lb-row lb-silver"><span class="lb-pos">🥈</span><span class="lb-info"><a href="./pages/Bob_Jo.html">Bob Johnson</a> <small>(Team Beta)</small></span><span class="lb-pts">142 pts</span></div>
<div class="lb-row lb-bronze"><span class="lb-pos">🥉</span><span class="lb-info"><a href="./pages/Carol_Da.html">Carol Davis</a> <small>(Team Alpha &amp; Team Beta)</small></span><span class="lb-pts">119 pts</span></div>
</div>

# Biggest Movers

<div class="biggest-movers">
<div class="mover-row"><span class="mv-up">&#x2191;1</span><span class="mv-name"><a href="./pages/Carol_Da.html">Carol Davis</a></span><span class="mv-rank">2nd</span></div>
<div class="mover-row"><span class="mv-down">&#x2193;1</span><span class="mv-name"><a href="./pages/Bob_Jo.html">Bob Johnson</a></span><span class="mv-rank">3rd</span></div>
<div class="mover-row"><span class="mv-neutral">&#x2192;</span><span class="mv-name"><a href="./pages/Alice_Sm.html">Alice Smith</a></span><span class="mv-rank">1st</span></div>
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
<div class="chart-controls">
<button id="chart-team-vs-team-toggle" class="chart-toggle">Show Rank</button>
</div>
<canvas id="chart-team-vs-team"></canvas>
</div>
<script>
(function(){
var el=document.getElementById("chart-team-vs-team");
var btn=document.getElementById("chart-team-vs-team-toggle");
var data={"labels": ["2026-06-12", "2026-06-13", "2026-06-14", "2026-06-11"], "datasets": [{"label": "Team Alpha", "data": [42.5, 88.5, 144.0, 42.5], "borderColor": "#7c0e0e", "backgroundColor": "rgba(124,14,14,0.08)", "tension": 0.3, "pointRadius": 5, "pointHoverRadius": 8, "borderWidth": 2.5, "fill": true}, {"label": "Team Beta", "data": [30.0, 57.0, 130.5, 30.0], "borderColor": "#0e7c7c", "backgroundColor": "rgba(14,124,124,0.08)", "tension": 0.3, "pointRadius": 5, "pointHoverRadius": 8, "borderWidth": 2.5, "fill": true}]};
var N=data.datasets.length;

/* store original colours for highlight/reset */
data.datasets.forEach(function(ds){ds._c=ds.borderColor;ds._b=ds.backgroundColor;});

/* pre-compute rank at each time point (1 = highest score) */
var pts=data.datasets.map(function(ds){return ds.data.slice();});
var rnk=pts.map(function(myPts,di){
  return myPts.map(function(v,li){
    var r=1;pts.forEach(function(op,oi){if(oi!==di&&op[li]>v)r++;});return r;
  });
});

var hl=null,isRank=false;

function resetHL(){
  data.datasets.forEach(function(ds){
    ds.borderWidth=2.5;ds.borderColor=ds._c;ds.backgroundColor=ds._b;
  });
  hl=null;
}

var chart=new Chart(el,{
  type:"line",data:data,
  options:{
    responsive:true,maintainAspectRatio:false,
    interaction:{mode:"index",intersect:false},
    plugins:{
      legend:{
        position:"right",
        labels:{boxWidth:12,padding:12,usePointStyle:true},
        /* click legend entry to highlight one line, click again to reset */
        onClick:function(e,item){
          var idx=item.datasetIndex;
          if(hl===idx){resetHL();}
          else{
            data.datasets.forEach(function(ds,i){
              if(i===idx){ds.borderWidth=4;ds.borderColor=ds._c;ds.backgroundColor=ds._b;}
              else{ds.borderWidth=1;ds.borderColor="rgba(0,0,0,0.1)";ds.backgroundColor="rgba(0,0,0,0.02)";}
            });
            hl=idx;
          }
          chart.update();
        }
      },
      tooltip:{callbacks:{label:function(c){
        return c.dataset.label+": "+(isRank?"#"+Math.round(c.raw):Math.round(c.raw)+" pts");
      }}}
    },
    scales:{
      x:{grid:{color:"rgba(0,0,0,0.05)"},ticks:{maxTicksLimit:10}},
      y:{beginAtZero:true,title:{display:true,text:"Points"},grid:{color:"rgba(0,0,0,0.05)"}}
    }
  }
});

/* toggle between Points and Rank views */
btn.addEventListener("click",function(){
  isRank=!isRank;
  resetHL();
  data.datasets.forEach(function(ds,i){
    ds.data=isRank?rnk[i]:pts[i];
    ds.tension=isRank?0:0.3;
    ds.fill=!isRank;
  });
  var y=chart.options.scales.y;
  if(isRank){
    y.reverse=true;y.beginAtZero=false;y.min=0.5;y.max=N+0.5;
    y.title.text="Position";
    y.ticks={stepSize:1,callback:function(v){return v%1===0?"#"+v:"";}};
  } else {
    y.reverse=false;y.beginAtZero=true;y.min=undefined;y.max=undefined;
    y.title.text="Points";y.ticks={};
  }
  btn.textContent=isRank?"Show Points":"Show Rank";
  btn.classList.toggle("active",isRank);
  chart.update();
});
})()
</script>

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

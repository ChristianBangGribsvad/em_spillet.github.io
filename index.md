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
<p class="chart-placeholder"><em>World Cup has not started — Today's Schmeichel will be revealed on each matchday throughout the tournament.</em></p>


# Leaderboard

<div class="leaderboard">
<div class="lb-row lb-gold"><span class="lb-pos">🥇</span><span class="lb-info"><a href="./pages/MetteMuttiFrankfurt_Is.html">MetteMuttiFrankfurt Isaacs-Bøttger</a> <small>(Friends and Family)</small></span><span class="lb-pts">0 pts</span></div>
<div class="lb-row lb-silver"><span class="lb-pos">🥈</span><span class="lb-info"><a href="./pages/Thomas_Pe.html">Thomas Petersen</a> <small>(GeH Fys)</small></span><span class="lb-pts">0 pts</span></div>
<div class="lb-row lb-bronze"><span class="lb-pos">🥉</span><span class="lb-info"><a href="./pages/Matias_Bu.html">Matias Bundgaard-Nielsen</a> <small>(Frederiksborg Gymnasium)</small></span><span class="lb-pts">0 pts</span></div>
<div class="lb-row "><span class="lb-pos">4</span><span class="lb-info"><a href="./pages/sexy_os.html">sexy ossi</a> <small>(Frederiksborg Gymnasium &amp; Friends and Family)</small></span><span class="lb-pts">0 pts</span></div>
<div class="lb-row "><span class="lb-pos">5</span><span class="lb-info"><a href="./pages/Emil_Jo.html">Emil Johansen</a> <small>(Friends and Family)</small></span><span class="lb-pts">0 pts</span></div>
<div class="lb-row "><span class="lb-pos">6</span><span class="lb-info"><a href="./pages/Renee_Pe.html">Renee Petersen</a> <small>(GeH Fys)</small></span><span class="lb-pts">0 pts</span></div>
<div class="lb-row "><span class="lb-pos">7</span><span class="lb-info"><a href="./pages/Christian_Is.html">Christian Isaacs</a> <small>(Friends and Family)</small></span><span class="lb-pts">0 pts</span></div>
<div class="lb-row "><span class="lb-pos">8</span><span class="lb-info"><a href="./pages/Sebastian_Le.html">Sebastian Lefmann</a> <small>(GAHK &amp; Frederiksborg Gymnasium)</small></span><span class="lb-pts">0 pts</span></div>
<div class="lb-row "><span class="lb-pos">9</span><span class="lb-info"><a href="./pages/RK__Fy.html">RK  Fysioterapi</a> <small>(GeH Fys)</small></span><span class="lb-pts">0 pts</span></div>
<div class="lb-row "><span class="lb-pos">10</span><span class="lb-info"><a href="./pages/Hanne_Ho.html">Hanne Hornshøj</a> <small>(GeH Fys)</small></span><span class="lb-pts">0 pts</span></div>
</div>

# Biggest Movers

<p class="chart-placeholder"><em>Biggest movers will appear after the first two scoring updates.</em></p>

# Next Matches

<div class="next-matches">
<p>South Korea vs Czechia &mdash; Fri 12 June, 04:00</p>
<p>Canada vs Bosnia-Herzegovina &mdash; Fri 12 June, 21:00</p>
</div>

# Yesterday's Results

<div class="yesterdays-results">
<p>Mexico None - None South Africa</p>
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
var data={"labels": ["2026-06-11"], "datasets": [{"label": "Friends and Family", "data": [0.0], "borderColor": "#0e4d7c", "backgroundColor": "rgba(14,77,124,0.08)", "tension": 0.3, "pointRadius": 5, "pointHoverRadius": 8, "borderWidth": 2.5, "fill": true}, {"label": "ATP", "data": [0.0], "borderColor": "#7c0e0e", "backgroundColor": "rgba(124,14,14,0.08)", "tension": 0.3, "pointRadius": 5, "pointHoverRadius": 8, "borderWidth": 2.5, "fill": true}, {"label": "Frederiksborg Gymnasium", "data": [0.0], "borderColor": "#0e7c4d", "backgroundColor": "rgba(14,124,77,0.08)", "tension": 0.3, "pointRadius": 5, "pointHoverRadius": 8, "borderWidth": 2.5, "fill": true}, {"label": "Danica Ejendomme", "data": [0.0], "borderColor": "#2d7c0e", "backgroundColor": "rgba(45,124,14,0.08)", "tension": 0.3, "pointRadius": 5, "pointHoverRadius": 8, "borderWidth": 2.5, "fill": true}, {"label": "Buzzanova", "data": [0.0], "borderColor": "#7c6c0e", "backgroundColor": "rgba(124,108,14,0.08)", "tension": 0.3, "pointRadius": 5, "pointHoverRadius": 8, "borderWidth": 2.5, "fill": true}, {"label": "GeH Fys", "data": [0.0], "borderColor": "#7c0e6c", "backgroundColor": "rgba(124,14,108,0.08)", "tension": 0.3, "pointRadius": 5, "pointHoverRadius": 8, "borderWidth": 2.5, "fill": true}, {"label": "GAHK", "data": [0.0], "borderColor": "#2d0e7c", "backgroundColor": "rgba(45,14,124,0.08)", "tension": 0.3, "pointRadius": 5, "pointHoverRadius": 8, "borderWidth": 2.5, "fill": true}]};
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

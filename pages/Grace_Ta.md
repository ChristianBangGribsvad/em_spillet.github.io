---
layout: default
---

# Grace Taylor

<div class="participant-meta"><span class="pmeta-ts">Submitted 1 Jun 2026 · 11:30</span><span class="pmeta-team">Team Beta</span></div>

<div class="stat-cards">
<div class="stat-card"><span class="stat-icon">🏆</span><div class="stat-body"><span class="stat-main">#6th out of 10 players across the game</span><span class="stat-sub">You beat 40% of all players</span></div></div>
<div class="stat-card"><span class="stat-icon stat-up">↑</span><div class="stat-body"><span class="stat-main">-83 pts last round</span><span class="stat-sub">+15 pts vs global avg (-98 pts) &middot; Moved up 6 places &middot; 1st out of 10 total players</span></div></div>
</div>
## Your score vs averages

<div class="chart-wrapper">
<canvas id="personal-Grace_Ta"></canvas>
</div>
<script>
(function(){
var el=document.getElementById("personal-Grace_Ta");
var data={"labels": ["2026-06-14", "2026-06-04"], "datasets": [{"label": "Your score", "data": [83.0, 0.0], "borderColor": "#1e40af", "backgroundColor": "rgba(30,64,175,0.08)", "borderWidth": 3, "tension": 0.3, "pointRadius": 6, "pointHoverRadius": 9, "fill": true, "order": 1}, {"label": "Team average", "data": [88.0, 0.0], "borderColor": "#0e7c7c", "backgroundColor": "rgba(14,124,124,0.04)", "borderWidth": 1.5, "borderDash": [3, 3], "tension": 0.3, "pointRadius": 3, "pointHoverRadius": 5, "fill": false, "order": 2}, {"label": "Global average", "data": [98.8, 0.0], "borderColor": "rgba(0,0,0,0.28)", "backgroundColor": "rgba(0,0,0,0.02)", "borderWidth": 1.5, "borderDash": [5, 5], "tension": 0.3, "pointRadius": 3, "pointHoverRadius": 5, "fill": false, "order": 3}]};
var hl=null;
data.datasets.forEach(function(ds){ds._c=ds.borderColor;ds._b=ds.backgroundColor;ds._w=ds.borderWidth||2;});
new Chart(el,{
  type:"line",data:data,
  options:{
    responsive:true,maintainAspectRatio:false,
    interaction:{mode:"index",intersect:false},
    plugins:{
      legend:{
        position:"right",labels:{boxWidth:12,padding:12,usePointStyle:true},
        onClick:function(e,item,legend){
          var chart=legend.chart;var idx=item.datasetIndex;
          if(hl===idx){
            data.datasets.forEach(function(ds){ds.borderWidth=ds._w;ds.borderColor=ds._c;ds.backgroundColor=ds._b;});
            hl=null;
          } else {
            data.datasets.forEach(function(ds,i){
              if(i===idx){ds.borderWidth=ds._w+1;ds.borderColor=ds._c;ds.backgroundColor=ds._b;}
              else{ds.borderWidth=1;ds.borderColor="rgba(0,0,0,0.1)";ds.backgroundColor="rgba(0,0,0,0.02)";}
            });
            hl=idx;
          }
          chart.update();
        }
      },
      tooltip:{callbacks:{label:function(c){return c.dataset.label+": "+Math.round(c.raw)+" pts";}}}
    },
    scales:{
      x:{grid:{color:"rgba(0,0,0,0.05)"},ticks:{maxTicksLimit:10}},
      y:{beginAtZero:true,title:{display:true,text:"Points"},grid:{color:"rgba(0,0,0,0.05)"}}
    }
  }
});
})()
</script>

## Your predictions

<div class="pred-table">
<div class="pred-breakdown">Group matches: <strong>0 pts</strong> &nbsp;&middot;&nbsp; Group winners: <strong>0 pts</strong> &nbsp;&middot;&nbsp; Special predictions: <strong>0 pts</strong></div>
<div class="pred-total">Total &nbsp;<span class="pred-total-pts">0 pts</span></div>
<div class="pred-col-header"><span>Match</span><span>Your pick</span><span>Result</span><span>Pts</span></div>
<div class="pred-section">
<div class="pred-section-header">Group A</div>
<div class="pred-row pts-unplayed"><span class="pred-match">Mexico vs South Africa</span><span class="pred-guess">1-2</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match">South Korea vs Czechia</span><span class="pred-guess">1-0</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match">Czechia vs South Africa</span><span class="pred-guess">2-1</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match">Mexico vs South Korea</span><span class="pred-guess">2-1</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match">Czechia vs Mexico</span><span class="pred-guess">2-1</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match">South Africa vs South Korea</span><span class="pred-guess">2-1</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-divider">Group winners</div>
<div class="pred-row pts-unplayed"><span class="pred-match">1st &amp; 2nd place</span><span class="pred-guess">Mexico / South Korea</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
</div>
<div class="pred-section">
<div class="pred-section-header">Group B</div>
<div class="pred-row pts-unplayed"><span class="pred-match">Canada vs Bosnia-Herzegovina</span><span class="pred-guess">1-0</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match">Qatar vs Switzerland</span><span class="pred-guess">0-1</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match">Switzerland vs Bosnia-Herzegovina</span><span class="pred-guess">2-1</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match">Canada vs Qatar</span><span class="pred-guess">2-1</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match">Switzerland vs Canada</span><span class="pred-guess">2-1</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match">Bosnia-Herzegovina vs Qatar</span><span class="pred-guess">2-1</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-divider">Group winners</div>
<div class="pred-row pts-unplayed"><span class="pred-match">1st &amp; 2nd place</span><span class="pred-guess">Canada / Switzerland</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
</div>
<div class="pred-section">
<div class="pred-section-header">Group C</div>
<div class="pred-row pts-unplayed"><span class="pred-match">Brazil vs Morocco</span><span class="pred-guess">1-1</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match">Haiti vs Scotland</span><span class="pred-guess">2-1</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match">Scotland vs Morocco</span><span class="pred-guess">2-1</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match">Brazil vs Haiti</span><span class="pred-guess">2-1</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match">Morocco vs Haiti</span><span class="pred-guess">2-1</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match">Scotland vs Brazil</span><span class="pred-guess">2-1</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-divider">Group winners</div>
<div class="pred-row pts-unplayed"><span class="pred-match">1st &amp; 2nd place</span><span class="pred-guess">Brazil / Scotland</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
</div>
<div class="pred-section">
<div class="pred-section-header">Group D</div>
<div class="pred-row pts-unplayed"><span class="pred-match">United States vs Paraguay</span><span class="pred-guess">0-1</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match">Australia vs Turkey</span><span class="pred-guess">2-1</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match">United States vs Australia</span><span class="pred-guess">2-1</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match">Turkey vs Paraguay</span><span class="pred-guess">2-1</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match">Turkey vs United States</span><span class="pred-guess">2-1</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match">Paraguay vs Australia</span><span class="pred-guess">2-1</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-divider">Group winners</div>
<div class="pred-row pts-unplayed"><span class="pred-match">1st &amp; 2nd place</span><span class="pred-guess">United States / Turkey</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
</div>
<div class="pred-section">
<div class="pred-section-header">Group E</div>
<div class="pred-row pts-unplayed"><span class="pred-match">Germany vs Curaçao</span><span class="pred-guess">1-0</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match">Ivory Coast vs Ecuador</span><span class="pred-guess">2-1</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match">Germany vs Ivory Coast</span><span class="pred-guess">2-1</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match">Ecuador vs Curaçao</span><span class="pred-guess">2-1</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match">Ecuador vs Germany</span><span class="pred-guess">2-1</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match">Curaçao vs Ivory Coast</span><span class="pred-guess">2-1</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-divider">Group winners</div>
<div class="pred-row pts-unplayed"><span class="pred-match">1st &amp; 2nd place</span><span class="pred-guess">Germany / Ivory Coast</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
</div>
<div class="pred-section">
<div class="pred-section-header">Group F</div>
<div class="pred-row pts-unplayed"><span class="pred-match">Netherlands vs Japan</span><span class="pred-guess">0-1</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match">Sweden vs Tunisia</span><span class="pred-guess">2-1</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match">Netherlands vs Sweden</span><span class="pred-guess">2-1</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match">Tunisia vs Japan</span><span class="pred-guess">2-1</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match">Tunisia vs Netherlands</span><span class="pred-guess">2-1</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match">Japan vs Sweden</span><span class="pred-guess">2-1</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-divider">Group winners</div>
<div class="pred-row pts-unplayed"><span class="pred-match">1st &amp; 2nd place</span><span class="pred-guess">Netherlands / Sweden</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
</div>
<div class="pred-section">
<div class="pred-section-header">Group G</div>
<div class="pred-row pts-unplayed"><span class="pred-match">Belgium vs Egypt</span><span class="pred-guess">0-0</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match">Iran vs New Zealand</span><span class="pred-guess">1-0</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match">Belgium vs Iran</span><span class="pred-guess">2-1</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match">New Zealand vs Egypt</span><span class="pred-guess">0-2</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match">New Zealand vs Belgium</span><span class="pred-guess">1-0</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match">Egypt vs Iran</span><span class="pred-guess">0-0</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-divider">Group winners</div>
<div class="pred-row pts-unplayed"><span class="pred-match">1st &amp; 2nd place</span><span class="pred-guess">Belgium / New Zealand</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
</div>
<div class="pred-section">
<div class="pred-section-header">Group H</div>
<div class="pred-row pts-unplayed"><span class="pred-match">Spain vs Cape Verde Islands</span><span class="pred-guess">2-1</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match">Saudi Arabia vs Uruguay</span><span class="pred-guess">2-1</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match">Spain vs Saudi Arabia</span><span class="pred-guess">2-1</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match">Uruguay vs Cape Verde Islands</span><span class="pred-guess">2-1</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match">Uruguay vs Spain</span><span class="pred-guess">2-1</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match">Cape Verde Islands vs Saudi Arabia</span><span class="pred-guess">2-1</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-divider">Group winners</div>
<div class="pred-row pts-unplayed"><span class="pred-match">1st &amp; 2nd place</span><span class="pred-guess">Spain / Uruguay</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
</div>
<div class="pred-section">
<div class="pred-section-header">Group I</div>
<div class="pred-row pts-unplayed"><span class="pred-match">France vs Senegal</span><span class="pred-guess">2-1</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match">Iraq vs Norway</span><span class="pred-guess">2-1</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match">France vs Iraq</span><span class="pred-guess">2-1</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match">Norway vs Senegal</span><span class="pred-guess">2-1</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match">Norway vs France</span><span class="pred-guess">2-1</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match">Senegal vs Iraq</span><span class="pred-guess">2-1</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-divider">Group winners</div>
<div class="pred-row pts-unplayed"><span class="pred-match">1st &amp; 2nd place</span><span class="pred-guess">France / Norway</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
</div>
<div class="pred-section">
<div class="pred-section-header">Group J</div>
<div class="pred-row pts-unplayed"><span class="pred-match">Argentina vs Algeria</span><span class="pred-guess">2-1</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match">Austria vs Jordan</span><span class="pred-guess">2-1</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match">Argentina vs Austria</span><span class="pred-guess">2-1</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match">Jordan vs Algeria</span><span class="pred-guess">2-1</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match">Jordan vs Argentina</span><span class="pred-guess">2-1</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match">Algeria vs Austria</span><span class="pred-guess">2-1</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-divider">Group winners</div>
<div class="pred-row pts-unplayed"><span class="pred-match">1st &amp; 2nd place</span><span class="pred-guess">Argentina / Austria</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
</div>
<div class="pred-section">
<div class="pred-section-header">Group K</div>
<div class="pred-row pts-unplayed"><span class="pred-match">Portugal vs Congo DR</span><span class="pred-guess">2-1</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match">Uzbekistan vs Colombia</span><span class="pred-guess">2-1</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match">Portugal vs Uzbekistan</span><span class="pred-guess">2-1</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match">Colombia vs Congo DR</span><span class="pred-guess">2-1</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match">Colombia vs Portugal</span><span class="pred-guess">2-1</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match">Congo DR vs Uzbekistan</span><span class="pred-guess">2-1</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-divider">Group winners</div>
<div class="pred-row pts-unplayed"><span class="pred-match">1st &amp; 2nd place</span><span class="pred-guess">Portugal / Colombia</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
</div>
<div class="pred-section">
<div class="pred-section-header">Group L</div>
<div class="pred-row pts-unplayed"><span class="pred-match">England vs Croatia</span><span class="pred-guess">2-1</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match">Ghana vs Panama</span><span class="pred-guess">2-1</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match">England vs Ghana</span><span class="pred-guess">2-1</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match">Panama vs Croatia</span><span class="pred-guess">2-1</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match">Panama vs England</span><span class="pred-guess">2-1</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match">Croatia vs Ghana</span><span class="pred-guess">2-1</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-divider">Group winners</div>
<div class="pred-row pts-unplayed"><span class="pred-match">1st &amp; 2nd place</span><span class="pred-guess">England / Croatia</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
</div>
<div class="pred-section">
<div class="pred-section-header">Special Predictions</div>
<div class="pred-row pts-unplayed"><span class="pred-match">Final winner</span><span class="pred-guess">Spain</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match">Final loser</span><span class="pred-guess">France</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match">Top scorer</span><span class="pred-guess">Pedri</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match">Scorer goals</span><span class="pred-guess">4</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
</div>
</div>

[Back](https://christianbanggribsvad.github.io/wc-predictions.github.io/)